 # Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


# This project incorporates work covered by the following copyright and permission notice:  

#    Copyright (c) 2009, Julien Fache
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:

#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of the author nor the names of other
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE.
"""XML-RPC methods of Gstudio metaWeblog API"""
import os
from datetime import datetime
from xmlrpclib import Fault
from xmlrpclib import DateTime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify

from gstudio.models import Nodetype
from gstudio.models import Metatype
from gstudio.models import NID
from objectapp.models import Gbobject
from objectapp.models import Gbobject, System, Process
from gstudio.settings import PROTOCOL
from gstudio.settings import UPLOAD_TO
from gstudio.managers import DRAFT, PUBLISHED
from django_xmlrpc.decorators import xmlrpc_func
from django.utils.datastructures import SortedDict
from gstudio.models import *
from django.contrib.auth.models import User



# http://docs.nucleuscms.org/blog/12#errorcodes
LOGIN_ERROR = 801
PERMISSION_DENIED = 803


def authenticate(username, password, permission=None):
    """Authenticate staff_user with permission"""
    try:
        user = User.objects.get(username__exact=username)
    except User.DoesNotExist:
        raise Fault(LOGIN_ERROR, _('Username is incorrect.'))
    if not user.check_password(password):
        raise Fault(LOGIN_ERROR, _('Password is invalid.'))
    if not user.is_staff or not user.is_active:
        raise Fault(PERMISSION_DENIED, _('User account unavailable.'))
    if permission:
        if not user.has_perm(permission):
            raise Fault(PERMISSION_DENIED, _('User cannot %s.') % permission)
    return user


def blog_structure(site):
    """A blog structure"""
    return {'url': '%s://%s%s' % (
        PROTOCOL, site.domain, reverse('gstudio_nodetype_archive_index')),
            'blogid': settings.SITE_ID,
            'blogName': site.name}


def user_structure(user, site):
    """An user structure"""
    return {'userid': user.pk,
            'email': user.email,
            'nickname': user.username,
            'lastname': user.last_name,
            'firstname': user.first_name,
            'url': '%s://%s%s' % (
                PROTOCOL, site.domain,
                reverse('gstudio_author_detail', args=[user.username]))}


def author_structure(user):
    """An author structure"""
    return {'user_id': user.pk,
            'user_login': user.username,
            'display_name': user.username,
            'user_email': user.email}


def metatype_structure(metatype, site):
    """A metatype structure"""
    return {'description': metatype.title,
            'htmlUrl': '%s://%s%s' % (
                PROTOCOL, site.domain,
                metatype.get_absolute_url()),
            'rssUrl': '%s://%s%s' % (
                PROTOCOL, site.domain,
                reverse('gstudio_metatype_feed', args=[metatype.tree_path])),
            # Useful Wordpress Extensions
            'metatypeId': metatype.pk,
            'parentId': metatype.parent and metatype.parent.pk or 0,
            'metatypeDescription': metatype.description,
            'metatypeName': metatype.title}


def post_structure(nodetype, site):
    """A post structure with extensions"""
    author = nodetype.authors.all()[0]
    return {'title': nodetype.title,
            'description': unicode(nodetype.html_content),
            'link': '%s://%s%s' % (PROTOCOL, site.domain,
                                   nodetype.get_absolute_url()),
            # Basic Extensions
            'permaLink': '%s://%s%s' % (PROTOCOL, site.domain,
                                        nodetype.get_absolute_url()),
            'metatypes': [cat.title for cat in nodetype.metatypes.all()],
            'dateCreated': DateTime(nodetype.creation_date.isoformat()),
            'postid': nodetype.pk,
            'userid': author.username,
            # Useful Movable Type Extensions
            'mt_excerpt': nodetype.excerpt,
            'mt_allow_comments': int(nodetype.comment_enabled),
            'mt_allow_pings': int(nodetype.pingback_enabled),
            'mt_keywords': nodetype.tags,
            # Useful Wordpress Extensions
            'wp_author': author.username,
            'wp_author_id': author.pk,
            'wp_author_display_name': author.username,
            'wp_password': nodetype.password,
            'wp_slug': nodetype.slug,
            'sticky': nodetype.featured}


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_users_blogs(apikey, username, password):
    """blogger.getUsersBlogs(api_key, username, password)
    => blog structure[]"""
    authenticate(username, password)
    site = Site.objects.get_current()
    return [blog_structure(site)]


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_user_info(apikey, username, password):
    """blogger.getUserInfo(api_key, username, password)
    => user structure"""
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return user_structure(user, site)


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_authors(apikey, username, password):
    """wp.getAuthors(api_key, username, password)
    => author structure[]"""
    authenticate(username, password)
    return [author_structure(author)
            for author in User.objects.filter(is_staff=True)]


@xmlrpc_func(returns='boolean', args=['string', 'string',
                                      'string', 'string', 'string'])
def delete_post(apikey, post_id, username, password, publish):
    """blogger.deletePost(api_key, post_id, username, password, 'publish')
    => boolean"""
    user = authenticate(username, password, 'gstudio.delete_nodetype')
    nodetype = Nodetype.objects.get(id=post_id, authors=user)
    nodetype.delete()
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_post(post_id, username, password):
    """metaWeblog.getPost(post_id, username, password)
    => post structure"""
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return post_structure(Nodetype.objects.get(id=post_id, authors=user), site)


@xmlrpc_func(returns='struct[]',
             args=['string', 'string', 'string', 'integer'])
def get_recent_posts(blog_id, username, password, number):
    """metaWeblog.getRecentPosts(blog_id, username, password, number)
    => post structure[]"""
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return [post_structure(nodetype, site) \
            for nodetype in Nodetype.objects.filter(authors=user)[:number]]


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_metatypes(blog_id, username, password):
    """metaWeblog.getMetatypes(blog_id, username, password)
    => metatype structure[]"""
    authenticate(username, password)
    site = Site.objects.get_current()
    return [metatype_structure(metatype, site) \
            for metatype in Metatype.objects.all()]


@xmlrpc_func(returns='string', args=['string', 'string', 'string', 'struct'])
def new_metatype(blog_id, username, password, metatype_struct):
    """wp.newMetatype(blog_id, username, password, metatype)
    => metatype_id"""
    authenticate(username, password, 'gstudio.add_metatype')
    metatype_dict = {'title': metatype_struct['name'],
                     'description': metatype_struct['description'],
                     'slug': metatype_struct['slug']}
    if int(metatype_struct['parent_id']):
        metatype_dict['parent'] = Metatype.objects.get(
            pk=metatype_struct['parent_id'])
    metatype = Metatype.objects.create(**metatype_dict)

    return metatype.pk


@xmlrpc_func(returns='struct', args=['string', 'string'])
def add_nums(num1, num2):
    """metaWeblog.add("num1","num2")
    => sum"""
    num1= int(num1)
    num2= int(num2)
    return dict({'sum':[num1 + num2]})

@xmlrpc_func(returns='string', args=['string', 'string'])
def get_nbh(name, of_type=""):
    """metaWeblog.get_nbh("object_name", "type of: [OT, O, MT]")
    => nbh"""
    # this should be extended to identifying an object with other criteria instead of title as it can be ambiguous
    try:        
        # retrieve the first matching object, (this should be changed to id or an additional specifiers like of_type="OT")
        n = NID.objects.filter(title=name)[0]
        if not n:
            return str({'error':'NOT FOUND'})

        if n.ref._meta.module_name == 'objecttype' or 'gbobject' or 'metatype':
            nbh =  n.ref.get_nbh
            if nbh:
                return str(nbh)
            else:
                return str({'error':'Error!'})
        else:
            return str({'error':'Not applicable as node is not OT, O or MT'})
    except:
        return str({'error':'Error!'})

@xmlrpc_func(returns='string', args=['string', 'string', 'string',
                                     'struct', 'boolean'])
def new_post(blog_id, username, password, post, publish):
    """metaWeblog.newPost(blog_id, username, password, post, publish)
    => post_id"""
    user = authenticate(username, password, 'gstudio.add_nodetype')
    if post.get('dateCreated'):
        creation_date = datetime.strptime(
            post['dateCreated'].value.replace('Z', '').replace('-', ''),
            '%Y%m%dT%H:%M:%S')
    else:
        creation_date = datetime.now()

    nodetype_dict = {'title': post['title'],
                  'content': post['description'],
                  'excerpt': post.get('mt_excerpt', truncate_words(
                      strip_tags(post['description']), 50)),
                  'creation_date': creation_date,
                  'last_update': creation_date,
                  'comment_enabled': post.get('mt_allow_comments', 1) == 1,
                  'pingback_enabled': post.get('mt_allow_pings', 1) == 1,
                  'featured': post.get('sticky', 0) == 1,
                  'tags': 'mt_keywords' in post and post['mt_keywords'] or '',
                  'slug': 'wp_slug' in post and post['wp_slug'] or slugify(
                      post['title']),
                  'password': post.get('wp_password', ''),
                  'status': publish and PUBLISHED or DRAFT}
    nodetype = Nodetype.objects.create(**nodetype_dict)

    author = user
    if 'wp_author_id' in post and user.has_perm('gstudio.can_change_author'):
        if int(post['wp_author_id']) != user.pk:
            author = User.objects.get(pk=post['wp_author_id'])
    nodetype.authors.add(author)

    nodetype.sites.add(Site.objects.get_current())
    if 'metatypes' in post:
        nodetype.metatypes.add(*[Metatype.objects.get_or_create(
            title=cat, slug=slugify(cat))[0]
                               for cat in post['metatypes']])

    return nodetype.pk


@xmlrpc_func(returns='boolean', args=['string', 'string', 'string',
                                      'struct', 'boolean'])
def edit_post(post_id, username, password, post, publish):
    """metaWeblog.editPost(post_id, username, password, post, publish)
    => boolean"""
    user = authenticate(username, password, 'gstudio.change_nodetype')
    nodetype = Nodetype.objects.get(id=post_id, authors=user)
    if post.get('dateCreated'):
        creation_date = datetime.strptime(
            post['dateCreated'].value.replace('Z', '').replace('-', ''),
            '%Y%m%dT%H:%M:%S')
    else:
        creation_date = nodetype.creation_date

    nodetype.title = post['title']
    nodetype.content = post['description']
    nodetype.excerpt = post.get('mt_excerpt', truncate_words(
        strip_tags(post['description']), 50))
    nodetype.creation_date = creation_date
    nodetype.last_update = datetime.now()
    nodetype.comment_enabled = post.get('mt_allow_comments', 1) == 1
    nodetype.pingback_enabled = post.get('mt_allow_pings', 1) == 1
    nodetype.featured = post.get('sticky', 0) == 1
    nodetype.tags = 'mt_keywords' in post and post['mt_keywords'] or ''
    nodetype.slug = 'wp_slug' in post and post['wp_slug'] or slugify(
        post['title'])
    nodetype.status = publish and PUBLISHED or DRAFT
    nodetype.password = post.get('wp_password', '')
    nodetype.save()

    if 'wp_author_id' in post and user.has_perm('gstudio.can_change_author'):
        if int(post['wp_author_id']) != user.pk:
            author = User.objects.get(pk=post['wp_author_id'])
            nodetype.authors.clear()
            nodetype.authors.add(author)

    if 'metatypes' in post:
        nodetype.metatypes.clear()
        nodetype.metatypes.add(*[Metatype.objects.get_or_create(
            title=cat, slug=slugify(cat))[0]
                               for cat in post['metatypes']])
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string', 'struct'])
def new_media_object(blog_id, username, password, media):
    """metaWeblog.newMediaObject(blog_id, username, password, media)
    => media structure"""
    authenticate(username, password)
    path = default_storage.save(os.path.join(UPLOAD_TO, media['name']),
                                ContentFile(media['bits'].data))
    return {'url': default_storage.url(path)}  

# Get functions start from here
@xmlrpc_func(returns='string', args=['int'])
def get_nodetype(nid):
      """Returns the nodetype of given nid 
      => metaWeblog.getNodetype(nid)"""     
      try :
       p = NID.objects.get(id = nid)
       try :
           g = Nodetype.objects.get(id=nid)
           return (g.ref._meta.module_name)
       except Nodetype.DoesNotExist :
           return "Not of Type Nodetype "
      except NID.DoesNotExist :
       return "Node Does Not Exist"

@xmlrpc_func(returns='int', args=['string'])
def nid_exists(nid):
      """Returns 1 if a node with given id exists, else returns a 0 
      => metaWeblog.nidExists(nodetypetitle)"""  
      try :
       p = NID.objects.get(title = nid)
       try:
      	   p = Nodetype.objects.get(title = nid)
      	   return 1
       except Nodetype.DoesNotExist:
	   return 0
      except NID.DoesNotExist :
       return "Node Does Not Exist"

@xmlrpc_func(returns='struct',args=['struct'])
def get_info_fromSSID(ssid_list) :
   """Given a list of nids, it returns entire information of each ssid inside a dictionary with all the dictionaries contained within a list 
   => metaWeblog.getinfoFromSSID(nidlist)"""  
   lst = []
   for ssid in ssid_list :
    try :
     t = NID.objects.get(id = ssid)
     try :
      p = Nodetype.objects.get(id = ssid)
      nbh = p.ref.get_nbh
      lst.append(str(nbh))
     except Nodetype.DoesNotExist :
      lst.append('Not of type Nodetype')
    except NID.DoesNotExist :
      lst.append('Node Does Not Exist' )
   return lst 

@xmlrpc_func(returns='struct', args=['struct','string']) 
def get_neighbourhood(ssid_list, get_what): 	
     """ Given a list of nids,it returns the neighbourhood(nbh/rendered) of the Nodetype
     => metaWeblog.getNeighbourhood(nidlist,nbh/rendered_nbh)"""  
     d = {}
     for ssid in ssid_list:
      try:
 	p = NID.objects.get(id = ssid)
        try :
          t = Nodetype.objects.get(id = ssid)        
          if get_what=='rendered_nbh' :
   	     nbh = p.ref.get_rendered_nbh
             d[str(p.id)]= str(nbh)
	  elif get_what=='nbh':
             nbh = p.ref.get_nbh
       	     d[str(p.id)]= str(nbh)
        except Nodetype.DoesNotExist :
          d[str(ssid)] = "Not of type Nodetype"
      except NID.DoesNotExist :
          d[str(ssid)] = "Node Does Not Exist"
     return d

@xmlrpc_func(returns='struct', args=['struct','string']) 
def get_gbobject_neighbourhood(ssid_list, get_what): 
     """ Given a list of nids,it returns the neighbourhood(nbh/rendered) of the Gbobject
     => metaWeblog.getGbobjectNeighbourhood(nidlist,nbh/rendered_nbh)"""   	
     d = {}
     for ssid in ssid_list:
      try:
 	p = NID.objects.get(id = ssid)
        try :
          t = Gbobject.objects.get(id = ssid)        
          if get_what=='rendered_nbh' :
   	     nbh = p.ref.get_rendered_nbh
             d[str(p.id)]= str(nbh)
	  elif get_what=='nbh':
             nbh = p.ref.get_nbh
       	     d[str(p.id)]= str(nbh)
        except Gbobject.DoesNotExist :
          d[str(ssid)] = "Not of type Gboject"
      except NID.DoesNotExist :
          d[str(ssid)] = "Node Does Not Exist"
     return d



@xmlrpc_func(returns='struct', args=['struct'])

def get_attributeType(subjecttypelist):
   """given the list of subjecttype inids the method returns all the attributetypes attached.
   => metaWeblog.getAttributeType(subjecttypeidlist)"""  
   d = {}
   for s in subjecttypelist :
      try :
        l = []
        p = NID.objects.get(id = s)
        k = p.ref._meta.module_name
        y = []
        if( k == 'objecttype' or 'metatype' ) :
          y = Attributetype.objects.filter(subjecttype_id = s)
        for i in y :
          l.append(str(i.id))
        d[str(s)] = l
      except NID.DoesNotExist :
        d[str(s)] = "Node Does not Exist"
   return d

# Get all function for getting all nodetypes
@xmlrpc_func(returns='struct', args=['string'])

def get_all(nodetype):
   """Given a class name it returns all the nids corresponding to their class name.
   => metaWeblog.getAll(classname)"""  
   d = {}
   try :
    p = eval(nodetype)
    h = p.objects.all()
    for i in h:
       d[str(i.title)] = i.id
   except NameError :
       return "The class with the given name Does not exist"
   return d


@xmlrpc_func(returns='struct', args=['struct'])

def get_datatype(attrtype_ssid_list) :
   """Given a list of attributessids, it returns its datatypes.
   => metaWeblog.getDatatype(attrtypenidlist)"""  
   d = {}
   for l in attrtype_ssid_list :
      try :
       p = NID.objects.get(id = l)
       n = p.ref._meta.module_name 
       if  n == 'attributetype' :
         ft = FIELD_TYPE_CHOICES[int(p.ref.dataType) - 1]
         d[str(p.id)] = ft[1]
       else :
         d[str(p.id)]= "Not a attributetype"
      except NID.DoesNotExist :
         d[str(l)] = "Node Does not Exist"
   return d


@xmlrpc_func(returns='struct', args=['string'])

def get_attributevalues(Attrssidlist) :
   """Given a list of attributessid, it returns their values 
   => metaWeblog.getAttributevalues(attrnidlist)"""  
   d = {} 
   for l in Attrssidlist :
     try :
      p = NID.objects.get(id = l)
      k = p.ref._meta.module_name
      if ( k == 'attribute' ) :
         t = Attribute.objects.get(id = l)
      	 d[str(t.id)] = t.svalue
      else :
         d[str(l)] = "Not an Attribute"
     except NID.DoesNotExist :
         d[str(l)] = "Node Does Not Exist"
   return d

@xmlrpc_func(returns='struct', args=['string'])
def get_subjecttypes( AttributeTypeNid ):
    """Given an attributetypenid, it returns the subjecttype participating in the attributetype.
    => metaWeblog.getSubjecttypes(attributetypenid)"""  
    try :
      d = {}
      t = NID.objects.get(id = AttributeTypeNid)
      k = t.ref._meta.module_name
      if  k == 'attributetype' :
        p = Attributetype.objects.get(id = AttributeTypeNid)
        n = p.subjecttype_id
        d['stid'] = str(n) 
        d['applicable_nodetypes'] = p.applicable_nodetypes
      else :
        return "Not an Attributetype"
    except NID.DoesNotExist:
      return "Node does not exist" 
    return d  

@xmlrpc_func(returns='struct', args=['string'])

def get_roles(relationtypenid) :
   """given a relationtype nid this method returns the roles participating in the relationtype.
   => metaWeblog.getRoles(relationtypenid)""" 
   try :
    t = NID.objects.get(id = relationtypenid)
    k = t.ref._meta.module_name
    d = {}
    if k == 'relationtype' :
     p = Relationtype.objects.get(nodetype_ptr_id = relationtypenid)
     d['cardinality1 '] = p.left_cardinality
     d['cardinality2'] = p.right_cardinality
     d['rtid']         = p.nodetype_ptr_id
     d['applicablenodetype1'] = p.left_applicable_nodetypes
     d['applicablenodetype2'] = p.right_applicable_nodetypes
     d['subjecttype1'] = p.left_subjecttype_id
     d['subjecttype2'] = p.right_subjecttype_id
    else :
     return "Not a Relationtype"
   except NID.DoesNotExist :
     return "Node Does Not Exist "
   return  d   
   
@xmlrpc_func(returns='struct', args=['string'])

def get_subtypes(nodeid) :
    """Returns only the immediate subtype of the node specified.
    => metaWeblog.getSubtypes(Nodetypeid)""" 
    try :
      y = NID.objects.get(id = nodeid)
      try :
          p = Nodetype.objects.get(id = nodeid)
          n = p.get_children()
          l = []
          for i in n:
              l.append(str(i.id))
      except Nodetype.DoesNotExist :
          return "Not of type nodetype"
    except NID.DoesNotExist :
      return " Node Does not exist"
    return l 

@xmlrpc_func(returns='struct', args=['string'])
    
def get_all_subtypes(nodeid) :
    """Returns all the 'subtypes' of the node specified
    => metaWeblog.getAllSubtypes(Nodetypenid)""" 
    try :
       l = []
       p = NID.objects.get(id = nodeid)
       try :
        k = Nodetype.objects.get(id = nodeid)
        h = k.get_descendants()
        for i in h :
           l.append(str(i.id))
       except  Nodetype.DoesNotExist :
        return "Not of type Nodetype"
    except NID.DoesNotExist :
        return "Node Does not Exist"
    return l

@xmlrpc_func(returns=['struct'], args=['struct'])

def get_restrictions(ATlist) :
  """Given a list of attributetype nids, this method returns all the restrictions that the attributetypes have.
  => metaWeblog.getRestrictions(Attributetypenids)""" 
  d = {}
  ft = []   
  for a in ATlist :
    try :
      k = NID.objects.get(id = a)
      t = k.ref._meta.module_name
      u = {}
      if t == 'attributetype' :
        p = Attributetype.objects.get(id = a)
        ft = FIELD_TYPE_CHOICES[int(p.dataType)-1]
        u['datatype'] = ft[1]
        u['length'] = p.max_digits
        u['precision'] = p.decimal_places
        d[str(p.id)] = u
      else :
        d[str(a)] = "Not a Attributetype"
    except NID.DoesNotExist :
       d[str(a)] = "Node Does Not Exist"   
  return d

@xmlrpc_func(returns='int', args=['string'])

def get_latest_SSID(nid) :
  """Given the nid, this method will return the latest ssid of the given id 
  => metaWeblog.getlatestSSID(nid)""" 
  try :
   p = NID.objects.get(id = nid)
   n = p.get_ssid
   u = len(n)
   if u == 0 :
     return "No Snapshots created"
   else :
     r = n[u-1]
     return r
  except NID.DoesNotExist:
   return "Node Does Not exist"

@xmlrpc_func(returns='struct', args=['int'])
def get_all_snapshots(nid) :
  """Given the id, this method will return all the ssids of the given id.
  => metaWeblog.getAllSnapshots(nid)""" 
  try :
   p = NID.objects.get(id = nid)
   n = p.get_ssid
  except NID.DoesNotExist :
   return "Node Does Not Exist"
  return n

# Set functions begin from here
@xmlrpc_func(returns='string', args=['struct','string'])
def set_attributetype(d,objid) :
   """ Given a dictionary of title,slug,applicable_nodetype,objectid,it creates an Attributetype for that Objecttypeid
   => metaWeblog.setAttributetype(d['title' = '',slug = '',applicable_nodetype = ''],objecttypeid)"""   
   try :
     p = NID.objects.get(id = objid)
     t = p.ref._meta.module_name
     w = []
     if  t == 'objecttype' or t == 'metatype' :
       u = Attributetype.objects.filter(subjecttype_id = objid)
       y = len(u)
       r = 0
       for i in u :
          if str(i.title) == d['title'] :
             return "Attributetype:",d['title']," already exists" 
          else :
             r = r + 1
       if r == y :
          w = Attributetype(title = d['title'],applicable_nodetypes = d['applicable_nodetype'],subjecttype_id = objid,slug = d['slug'])
          w.save()
          return w.id
     else :
        return "Not a objecttype"    
   except NID.DoesNotExist :
      return "Node Does Not Exist"
  


@xmlrpc_func(returns='int', args=['struct','string'])

def set_relationtype(d,uid) :
   """ Given a objecttypeid and a dictionary of title,slug,inverse,right_subjecttype_id,it creates an Relationtype for that Objecttype
   => metaWeblog.setRelationtype(d['title' = '', slug = '', right_subjecttype_id = '', inverse = ''],objecttypeid)""" 
 
   try :
     k = NID.objects.get(id = uid)
     f = k.ref._meta.module_name
     r = 0
     t = []
     if ( f == 'objecttype' or f == 'metatype') :
       p = Relationtype.objects.filter(left_subjecttype_id = uid)
       u = len(p)
       for n in p :
         if (str(n.title) == d['title']) :
           return "Relationtype :",d['title'],"already exists for",n.title
         else :
           r = r + 1
       if r == u :
          t = Relationtype(title = d['title'],left_subjecttype_id = uid,right_subjecttype_id = d['right_subjecttype_id'], 
                          slug = d['slug'],inverse = d['inverse'])
          t.save()
          return t.id
     else :
       return " Not of type Objecttype or Metatype"
   except NID.DoesNotExist :
      return " Node does not Exist"

@xmlrpc_func(returns='int', args=['struct','string'])

def set_objecttype(d) :
   """ Given a dictionary of title,slug,it creates a Objecttype
   => metaWeblog.setObjecttype(d['title' = '', slug = ''],objecttypeid)""" 
   k = Objecttype.objects.all()
   u = len(k)
   r = 0
   t = []
   for n in k :
       if (str(n.title) == d['title']) :
          return "Objecttype",d['title'],"already exists"
       else :
          r = r + 1
   if r == u :
       t = Objecttype(title = d['title'], slug = d['slug'])
       t.save()

   return t.id


@xmlrpc_func(returns='int', args=['struct','string'])

def set_object(d,o) :
   """ Given a objecttypeid and a dictionary of title,slug,it creates an Object for that objecttypeid
   => metaWeblog.setAttributetype(d['title' = '',slug = ''],objecttypeid)""" 
  
   try : 
    k = NID.objects.get(id = o)
    t = k.ref._meta.module_name
    u = 0
    r = 0
    y = []
    h = []
    if (t == 'objecttype' or t =='metatype') :
      p = Objecttype.objects.get(id = o)
      h = p.get_members
      u = len(h)
      for i in h :
        if(str(i.title) == d['title']) :
          return "Object",d['title'],"already exists for",p.title
        else :
          r = r + 1       
      if r == u :
       y = Gbobject(title = d['title'],slug = d['slug'])
       y.save()
       y.objecttypes.add(p)  
       return y.id
    else :
       return "Not of type Objecttype or metatype"
   except NID.DoesNotExist :
      return "Node does not exist"

@xmlrpc_func(returns='int', args=['struct','string'])

def set_attribute(d,objid) :
    """ Given a objecttypeid and dictionary of attributetypetitle,subject_id,svalue,it creates an Attribute for the Attributetype of that objecttypeid
    => metaWeblog.setAttributetype(d['attributetypetitle' = '',subject_id = '',svalue = ''],objecttypeid)""" 
    try : 
      k = NID.objects.get(id = objid)  
      t = k.ref._meta.module_name
      if  t == 'objecttype' or t == 'metatype' :
          p = Attributetype.objects.filter(subjecttype_id = objid)
          s = []
          for i in p :
              if (str(i.title) == d['attributetypetitle']) :
                 s = Attribute(attributetype_id = i.id,subject_id = d['subject_id'],svalue = d['svalue'])
                 s.save()
                 return s.id
      else :
        return " The objectid entered is not a objecttype or metatype"
    except NID.DoesNotExist:
       return "Node does not Exist"
            
     
@xmlrpc_func(returns='int', args=['struct','string','string'])

def set_relation(d,obj1,obj2) :
    """ Given  objecttype1id and objecttype2id between whose relation is to be established and dictionary of 				  		 	relationtypename,left_subject_id,right_subject_id,it creates a relation between objects of the two objecttype specfied
    => metaWeblog.setRelation(d['relationtypename' = '',left_subject_id = '',right_subject_id = ''],objecttypeid1,objecttypeid2)""" 
    try :   
      p = Relationtype.objects.filter(left_subjecttype_id = obj1,right_subjecttype_id = obj2)
      s = []
      for i in p :
         if (str(i.title) == d['relationtypename']) :
           s = Relation(relationtype_id = i.id,left_subject_id = d['left_subject_id'],right_subject_id = d['right_subject_id'])
           s.save()
           return s.id
    except Relationtype.DoesNotExist :
       return "Relationtype Does Not Exist"

@xmlrpc_func(returns='list')
def list_id():
    """Get a list of Gbobjects' ids"""
    return [id.id for id in Gbobject.objects.all()]

@xmlrpc_func(returns='struct', args=['string'])
def dict_id(id=None):
    """Get a Gbobject as a dict or as a list of dicts"""
    if id:
        return Gbobject.objects.get(id="{0}".format(id))
    else:
        return [dict_id(id) for id in list_id()]
