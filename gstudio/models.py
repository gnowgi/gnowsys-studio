
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




"""Super models of Gstudio  """
import warnings
from datetime import datetime
from django.db import models
from django.db.models import Q
from django.utils.html import strip_tags
from django.utils.html import linebreaks
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.utils.importlib import import_module
from django.contrib import comments
from django.contrib.comments.models import CommentFlag
from django.contrib.comments.moderation import moderator
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags.markup import markdown
from django.contrib.markup.templatetags.markup import textile
from django.contrib.markup.templatetags.markup import restructuredtext
import mptt

from djangoratings.fields import RatingField
from tagging.fields import TagField
from gstudio.settings import UPLOAD_TO
from gstudio.settings import MARKUP_LANGUAGE
from gstudio.settings import NODETYPE_TEMPLATES
from gstudio.settings import NODETYPE_BASE_MODEL
from gstudio.settings import MARKDOWN_EXTENSIONS
from gstudio.settings import AUTO_CLOSE_COMMENTS_AFTER
from gstudio.managers import nodetypes_published
from gstudio.managers import NodetypePublishedManager
from gstudio.managers import NodePublishedManager
from gstudio.managers import AuthorPublishedManager
from gstudio.managers import DRAFT, HIDDEN, PUBLISHED
from gstudio.moderator import NodetypeCommentModerator
from gstudio.url_shortener import get_url_shortener
from gstudio.signals import ping_directories_handler
from gstudio.signals import ping_external_urls_handler
import json
import reversion
from reversion.models import Version
from django.core import serializers

NODETYPE_CHOICES = (
    ('ND', 'Nodes'),
    ( 'OB' ,'Objects'),
    ('ED', 'Edges'),
    ('NT', 'Node types'),
    ('ET', 'Edge types'),
    ('OT', 'Object types'),
    ('RT', 'Relation types'),
    ('MT', 'Metatypes'),
    ('AT', 'Attribute types'),
    ('RN', 'Relations'),
    ('AS', 'Attributes'),
    ('ST', 'System type'),
    ('SY', 'System'),
    ('NS', 'Node specification'),
    ('AS', 'Attribute specification'),
    ('RS', 'Relation specification'),
    ('IN', 'Intersection'),
    ('CP', 'Complement'),
    ('UN', 'Union'),
   )

DEPTYPE_CHOICES = (
    ('0', 'Concept-Concept'),
    ('1', 'Activity-Activity'),
    ('2', 'Question-Question'),
    ('3', 'Concept-Activity'),
    ('4', 'Activity-Concept'),
    ('5', 'Question-Concept'),
    ('6', 'Concept-Question'),
    ('7', 'Question-Activity'),
    ('8', 'Activity-Question'),
   )

FIELD_TYPE_CHOICES = (
    ('1', 'CharField'),    
    ('2', 'TextField'),    
    ('3', 'IntegerField'),    
    ('4', 'CommaSeparatedIntegerField'),
    ('5', 'BigIntegerField'),    
    ('6', 'PositiveIntegerField'),    
    ('7', 'DecimalField'),
    ('8', 'FloatField'),
    ('9', 'BooleanField'),
    ('10', 'NullBooleanField'),
    ('11', 'DateField'),
    ('12', 'DateTimeField'),
    ('13', 'TimeField'),    
    ('14', 'EmailField'),
    ('15', 'FileField'),
    ('16', 'FilePathField'),
    ('17', 'ImageField'),
    ('18', 'URLField'),    
    ('19', 'IPAddressField'),
    )


STATUS_CHOICES = ((DRAFT, _('draft')),
                  (HIDDEN, _('hidden')),
                  (PUBLISHED, _('published')))

class Author(User):
    """Proxy Model around User"""
    
    objects = models.Manager()
    published = AuthorPublishedManager()

    def nodetypes_published(self):
        """Return only the nodetypes published"""
        return nodetypes_published(self.nodetypes)
    
    @property
    def title(self):
        return self.username

    @models.permalink
    def get_absolute_url(self):
        """Return author's URL"""
        #return "/authors/%s/" %(self.username) 
        return ('gstudio_author_detail', (self.username,))

    class Meta:
        """Author's Meta"""
        proxy = True

class NID(models.Model):
    """the set of all nodes.  provides node ID (NID) to all nodes in
    the network, including edges.  Edges are also first class citizens
    in the gnowledge base. """

    title = models.CharField(_('title'), help_text=_('give a name to the node'), max_length=255)
    last_update = models.DateTimeField(_('last update'), default=datetime.now)
    creation_date = models.DateTimeField(_('creation date'),
                                         default=datetime.now)
    
    slug = models.SlugField(help_text=_('used for publication'),
                            unique_for_date='creation_date',
                            max_length=255)


    def get_serialized_dict(self):
        """
        return the fields in a serialized form of the current object using the __dict__ function.
        """
        return self.__dict__

    @property
    def get_app_name(self):
        if self.ref.__class__.__name__=='Gbobject' or self.ref.__class__.__name__=='Process' or self.ref.__class__.__name__=='System' :
            return 'type'

    @models.permalink
    def get_absolute_url(self):
        """Return nodetype's URL"""
        if self.get_app_name=='type':
           return ('objectapp_gbobject_detail', (), {
            	'year': self.creation_date.strftime('%Y'),
            	'month': self.creation_date.strftime('%m'),
            	'day': self.creation_date.strftime('%d'),
            	'slug': self.slug})
        else:
           return ('gstudio_nodetype_detail', (), {
           	'year': self.creation_date.strftime('%Y'),
            	'month': self.creation_date.strftime('%m'),
            	'day': self.creation_date.strftime('%d'),
            	'slug': self.slug})

    @property
    def ref(self):
        """ 
        Returns the object reference the id belongs to.
        """
        try:
            """ 
            ALGO:     get object id, go to version model, return for the given id.
            """

            # Retrieving only the relevant tupleset for the versioned objects
            vrs = Version.objects.filter(type=0 , object_id=self.id)
            # Returned value is a list, so splice it.                                                                                                     
            vrs =  vrs[0]            
        except:
            return None
        
        return vrs.object
    
    @property
    def reftype(self):
        """ 
        Returns the type the id belongs to.
        """
        try:
            """ 
            ALGO: simple wrapper for the __class__.__name__ so that it can be used in templates  
            """
            obj = self.ref
            return obj.__class__.__name__
        
        except:
            return None
        


    @property
    def get_edit_url(self):
        return "/admin/" + self._meta.app_label + "/" + self._meta.module_name + "/" + str(self.id)
   


    def get_serialized_data(self):
        """
        return the fields in a serialized form of the current object.
        get object id, go to version model, return serialized_data for the given id
        """
        from reversion.models import Version
        version = Version.objects.get(id=self.id)
        return version.serialized_data

    def __unicode__(self):
        return self.title


    class Meta:
        """NID's Meta"""



class Node(NID):
    """
    Super class 
    """

    altnames = TagField(_('alternate names'), help_text=_('alternate names if any'), blank=True, null=True)
    plural = models.CharField(_('plural name'), help_text=_('plural form of the node name if any'), max_length=255, blank=True, null=True)
    rating = RatingField(range=5, can_change_vote = True, help_text=_('your rating'), blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLISHED)
    start_publication = models.DateTimeField(_('start publication'),
                                             help_text=_('date start publish'),
                                             default=datetime.now)
    end_publication = models.DateTimeField(_('end publication'),
                                           help_text=_('date end publish'),
                                           default=datetime(2042, 3, 15))

    sites = models.ManyToManyField(Site, verbose_name=_('sites publication'),
                                   related_name='nodetypes')
    published = NodePublishedManager()
    def __unicode__(self):
        return self.title

    class Meta:
        abstract=False

class Edge(NID):


    def __unicode__(self):
        return self.title

    class Meta:
        abstract=False

 
class Metatype(Node):
    """
    Metatype object for Nodetype
    """

    
    description = models.TextField(_('description'), blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent metatype'), related_name='children')


    def nodetypes_published(self):
        """
        Return only the published nodetypes 
        """
        return nodetypes_published(self.member_types)

    @property
    def get_nbh(self):
        """  
        Returns the neighbourhood of the metatype
        """
        nbh = {}
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames 
        nbh['plural'] = self.plural
	
        if self.parent:
            nbh['typeof'] = self.parent
        # generate ids and names of children/members
        nbh['contains_subtypes'] = self.children.get_query_set()
        nbh['contains_members'] = self.nodetypes.all()
        nbh['left_subjecttype_of'] = Relationtype.objects.filter(left_subjecttype=self.id)
        nbh['right_subjecttype_of'] = Relationtype.objects.filter(right_subjecttype=self.id)
        nbh['attributetypes'] = Attributetype.objects.filter(subjecttype=self.id)
        
        return nbh


    @property
    def get_possible_attributetypes(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the AT's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # recursive thru parent field and append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        attrtypes = [] 
                
        for each in ancestor_list:
            # retrieve all the AT's from each ancestor 
            attrtypes.extend(Attributetype.objects.filter(subjecttype=each.id))
                     
        return attrtypes


    @property
    def get_possible_rels(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the R's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        rels = {}
        rt_set = Relation.objects.all()
        right_subset = []
        left_subset = []
        
        for each in ancestor_list:
            # retrieve all the RT's from each ancestor 
            right_subset.extend(rt_set.filter(subject1=each.id))
            left_subset.extend(rt_set.filter(subject2=each.id))
         
        rels['possible_leftroles'] = left_subset
        rels['possible_rightroles'] = right_subset
        
        return rels



    @property
    def get_possible_attributes(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the RT's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # recursive thru parent field and append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        attrs = [] 
                
        for each in ancestor_list:
            # retrieve all the AT's from each ancestor 
            attrs.extend(Attribute.objects.filter(subject=each.id))
                     
        return attrs

    @property
    def get_rendered_nbh(self):
        """
        Returns the neighbourhood of the metatype
        """
        nbh = {}
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames
        nbh['plural'] = self.plural
	
        if self.parent:
            nbh['typeof'] = self.parent
        # generate ids and names of children
            nbh['contains_subtypes'] = self.children.get_query_set()
        contains_members_list = []
        for each in self.nodetypes.all():
            contains_members_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['contains_members'] = contains_members_list
        nbh['left_subjecttype_of'] = Relationtype.objects.filter(left_subjecttype=self.id)
        nbh['right_subjecttype_of'] = Relationtype.objects.filter(right_subjecttype=self.id)
        nbh['attributetypes'] = Attributetype.objects.filter(subjecttype=self.id)
	

        return nbh

                  
    @property
    def tree_path(self):
        """Return metatype's tree path, by its ancestors"""
        if self.parent:
            return '%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    def __unicode__(self):
        return self.title

    @property
    def composed_sentence(self):
        "composes the relation as a sentence in triple format."
        if self.parent:
            return '%s is a kind of %s' % (self.title, self.parent.tree_path)
        return '%s is a root node'  % (self.slug)
    

    @models.permalink
    def get_absolute_url(self):
        """Return metatype's URL"""
        return ('gstudio_metatype_detail', (self.tree_path,))


    class Meta:
        """Metatype's Meta"""
        ordering = ['title']
        verbose_name = _('metatype')
        verbose_name_plural = _('metatypes')





class Nodetype(Node):
    """
    Model design for publishing nodetypes.  Other nodetypes inherit this class.
    """



    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    content = models.TextField(_('content'), null=True, blank=True)
    content_org = models.TextField(_('content'), null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               verbose_name=_('is a kind of'),
                               related_name='children')

    prior_nodes = models.ManyToManyField('self', null=True, blank=True,
                               verbose_name=_('its meaning depends on '),
                               related_name='posterior_nodes')
    posterior_nodes = models.ManyToManyField('self', null=True, blank=True,
                               verbose_name=_('required for the meaning of '),
                               related_name='prior_nodes')

    image = models.ImageField(_('image'), upload_to=UPLOAD_TO,
                              blank=True, help_text=_('used for illustration'))

    excerpt = models.TextField(_('excerpt'), blank=True,
                                help_text=_('optional element'))

    tags = TagField(_('tags'))
    metatypes = models.ManyToManyField(Metatype, verbose_name=_('member of metatypes'),
                                        related_name='member_types',
                                        blank=True, null=True)

    

    authors = models.ManyToManyField(User, verbose_name=_('authors'),
                                     related_name='nodetypes',
                                     blank=True, null=False)

    featured = models.BooleanField(_('featured'), default=False)
    comment_enabled = models.BooleanField(_('comment enabled'), default=True)
    pingback_enabled = models.BooleanField(_('linkback enabled'), default=True)
    login_required = models.BooleanField(
        _('login required'), default=False,
        help_text=_('only authenticated users can view the nodetype'))
    password = models.CharField(
        _('password'), max_length=50, blank=True,
        help_text=_('protect the nodetype with a password'))

    template = models.CharField(
        _('template'), max_length=250,
        default='gstudio/nodetype_detail.html',
        choices=[('gstudio/nodetype_detail.html', _('Default template'))] + \
        NODETYPE_TEMPLATES,
        help_text=_('template used to display the nodetype'))
    rurl=models.URLField(_('rurl'),verify_exists=True,null=True, blank=True)
    objects = models.Manager()
    published = NodetypePublishedManager()


    def get_possible_reltypes(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the RT's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        reltypes = {}
        rt_set = Relationtype.objects.all()
        right_subset = []
        left_subset = []
        
        for each in ancestor_list:
            # retrieve all the RT's from each ancestor 
            right_subset.extend(rt_set.filter(subjecttypeLeft=each.id))
            left_subset.extend(rt_set.filter(subjecttypeRight=each.id))
         
        reltypes['possible_leftroles'] = left_subset
        reltypes['possible_rightroles'] = right_subset
        
        return reltypes


    @property
    def get_possible_attributetypes(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the AT's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # recursive thru parent field and append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        attrtypes = [] 
                
        for each in ancestor_list:
            # retrieve all the AT's from each ancestor 
            attrtypes.extend(Attributetype.objects.filter(subjecttype=each.id))
                     
        return attrtypes


    @property
    def get_possible_rels(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the R's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        rels = {}
        rt_set = Relation.objects.all()
        right_subset = []
        left_subset = []
        
        for each in ancestor_list:
            # retrieve all the RT's from each ancestor 
            right_subset.extend(rt_set.filter(subject1=each.id))
            left_subset.extend(rt_set.filter(subject2=each.id))
         
        rels['possible_leftroles'] = left_subset
        rels['possible_rightroles'] = right_subset
        
        return rels



    @property
    def get_possible_attributes(self):
        """
        Gets the relations possible for this metatype
        1. Recursively create a set of all the ancestors i.e. parent/subtypes of the MT. 
        2. Get all the RT's linked to each ancestor 
        """
        #Step 1. 
        ancestor_list = []
        this_parent = self.parent
        
        # recursive thru parent field and append
        while this_parent:
            ancestor_list.append(this_parent)
            this_parent = this_parent.parent
            
        #Step 2.
        attrs = [] 
                
        for each in ancestor_list:
            # retrieve all the AT's from each ancestor 
            attrs.extend(Attribute.objects.filter(subject=each.id))
                     
        return attrs

    def get_graph_json(self):
        
        
        # predicate_id={"plural":"a1","altnames":"a2","contains_members":"a3","contains_subtypes":"a4","prior_nodes":"a5", "posterior_nodes":"a6"}
	g_json = {}
	g_json["node_metadata"]= [] 
	g_json["relations"]=[]

	
	nbh = self.get_nbh
	predicate_id = {}
        counter = 1
        for key in nbh.keys():
            val = "a" + str(counter)
            predicate_id[key] = val
            counter = counter + 1
        #print predicate_id

        attr_counter = -1

        this_node = {"_id":str(self.id),"title":self.title,"screen_name":self.title, "url":self.get_absolute_url()}
        g_json["node_metadata"].append(this_node)      

	for key in predicate_id.keys():
		if nbh[key]:
			try:
				#g_json[str(key)]=[] 
				#g_json["relations"].append(key)    

				g_json["node_metadata"].append({"_id":str(predicate_id[key]),"screen_name":key})

				#g_json[str(key)].append({"from":self.id , "to":predicate_id[key],"value":1, "level":1  })

				g_json["relations"].append({"from":self.id ,"type":str(key),"value":1,"to":predicate_id[key] })
				if not isinstance(nbh[key],basestring):
                                    for item in nbh[key]:
                                        #create nodes
                                        g_json["node_metadata"].append({"_id":str(item.id),"screen_name":item.title,"title":self.title, "url":item.get_absolute_url()})

					# g_json[str(key)].append({"from":predicate_id[key] , "to":item.id ,"value":1  })
					#create links
                                        g_json["relations"].append({"from":predicate_id[key] ,"type":str(key), "value":1,"to":item.id  })
			
                                else:
				 	#value={nbh["plural"]:"a4",nbh["altnames"]:"a5"}			
		            	 	#this_node[str(key)]=nbh[key] key, nbh[key]                                     
				 	#for item in value.keys():
                                    g_json["node_metadata"].append({"_id":attr_counter,"screen_name":nbh[key]})
				    #g_json[str(key)].append({"from":predicate_id[key] , "to":attr_counter ,"value":1, "level":2 })
                                    g_json["relations"].append({"from":predicate_id[key] ,"type":str(key) ,"value":1,"to":attr_counter })
                                    attr_counter-=1
							
			except:
                            pass
        #print g_json
        return json.dumps(g_json)   

    @property
    def tree_path(self):
        """Return nodetype's tree path, by its ancestors"""
        if self.parent:
            return '%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    @property
    def tree_path_sentence(self):
        """ Return the parent of the nodetype in a triple form """
        if self.parent:
            return '%s is a kind of %s' % (self.title, self.parent.tree_path)
        return '%s is a root node' % (self.title)


    @property
    def html_content(self):
        """Return the content correctly formatted"""
        if MARKUP_LANGUAGE == 'markdown':
            return markdown(self.content, MARKDOWN_EXTENSIONS)
        elif MARKUP_LANGUAGE == 'textile':
            return textile(self.content)
        elif MARKUP_LANGUAGE == 'restructuredtext':
            return restructuredtext(self.content)
        elif not '</p>' in self.content:
            return linebreaks(self.content)
        return self.content
    @property
    def get_relations(self):
        """
        Returns all the relations of the nodetype
        """
        relations={}
        
        left_relations=Relation.objects.filter(left_subject=self.id)
        if left_relations:    
            for each in left_relations:
                relation=each.relationtype.title
                predicate=each.right_subject
                relations[relation]=predicate
        
        right_relations=Relation.objects.filter(right_subject=self.id)
        if right_relations:    
            for each in right_relations:
                relation=each.relationtype.inverse
                predicate=each.left_subject
                relations[relation]=predicate
        return relations

    @property
    def get_relations1(self):
        """
        Returns all the relations of the nodetype
        """
        relations={}
        reltype={}
        left_relations=Relation.objects.filter(left_subject=self.id)
        if left_relations:
           for each in left_relations:
           	relation=each.relationtype.title
           	predicate=each.right_subject
           	predicate_values=[]
                if reltype:
              	   fl=0
              	   for key,value in reltype.items():
                       if type(value) <> list:
                          t=[]
                          t.append(value)
                          predicate_values=t
                       else:
                          predicate_values=value
                       if each.relationtype.title==key:
                          fl=1
                          predicate_values.append(predicate)
                          reltype[key]=predicate_values             
                   if fl==0:
                       predicate_values=predicate
                       reltype[relation]=predicate_values
                else:
                    predicate_values.append(predicate)
                    reltype[relation]=predicate_values
                relations['lrelations']=reltype
        
        right_relations=Relation.objects.filter(right_subject=self.id)
        reltype={}
        if right_relations:
           for each in right_relations:
           	relation=each.relationtype.inverse
           	predicate=each.left_subject
                predicate_values=[]
                if reltype:
                   fl=0
              	   for key,value in reltype.items():
                       if type(value) <> list:
                          t=[]
                          t.append(value)
                          prdicate_values=t
                       else:
                          predicate_values=value
                       if each.relationtype.inverse==key:
                          fl=1
                          predicate_values.append(predicate)
                          reltype[key]=predicate_values
                          
                   if fl==0:
                       predicate_values=predicate
                       reltype[relation]=predicate_values
                          
                else:
                   predicate_values.append(predicate)
                   reltype[relation]=predicate_values
                relations['rrelations']=reltype
        return relations

    @property
    def get_attributes(self):
        attributes_dict =  {}
        all_attributes=self.subject_of.all()
        for attributes in all_attributes:
                val=[]
        	atr_key=attributes.attributetype.title
                val.append(attributes.svalue)
		
                if attributes_dict:
                     fl=0
                     itms=attributes_dict
                     
                     for key,value in itms.items():
                     	  if atr_key in key:
                                 fl=1
                                 if type(value) <> list:
                                      t=[]
                                      t.append(value)
                                      val.extend(t)
                                      
                                 else:
                                      val.extend(value)
                attributes_dict[atr_key]=val
        return attributes_dict

    @property
    def get_rendered_nbh(self):
        """          
        Returns the neighbourhood of the nodetype
        """
        nbh = {}
        nbh['title'] = self.title
	nbh['count_title'] = len(nbh['title'])
        nbh['altnames'] = self.altnames
	nbh['count_altnames'] = len(nbh['altnames'])
        nbh['plural'] = self.plural 
	nbh['count_plural'] = len(nbh['plural'])    
        #get all MTs 
        member_of_dict = {}
        for each in self.metatypes.all():
            member_of_dict[each.title]= each.get_absolute_url()
        nbh['member_of_metatypes']=member_of_dict
	nbh['count_member_of_metatypes'] = len(nbh['member_of_metatypes'])  
        typeof={}
        parent=self.parent_id
        if parent:
            typeof[parent] = parent.get_absolute_url()
        nbh['type_of']=typeof
	nbh['count_type_of'] = len(nbh['type_of'])    
        #get all subtypes 
        subtypes={}
        for each in Nodetype.objects.filter(parent=self.id):
            subtypes[each.title] =each.get_absolute_url()
        nbh['contains_subtypes']=subtypes  
	nbh['count_contains_subtypes'] = len(nbh['contains_subtypes'])  
        # get all the objects inheriting this OT 
        contains_members_dict = {}
        for each in self.member_objects.all():
           contains_members_dict[each.title]= each.get_absolute_url()
        nbh['contains_members'] = contains_members_dict
	nbh['count_contains_members'] = len(nbh['contains_members'])
        #get prior nodes
        priornodes_dict = {}
        for each in self.prior_nodes.all():
             priornodes_dict[each.title]= each.get_absolute_url()
        nbh['priornodes'] = priornodes_dict
	nbh['count_priornodes'] = len(nbh['priornodes'])
        #get posterior nodes
        posteriornodes_dict = {}
        for each in self.posterior_nodes.all():
             posteriornodes_dict[each.title]= each.get_absolute_url()
        nbh['posteriornodes'] = posteriornodes_dict
	nbh['count_posteriornodes'] = len(nbh['posteriornodes'])
        #get authors
        author_dict = {}
        for each in self.authors.all():
             author_dict['User'] = each.get_absolute_url()
        nbh['authors'] = author_dict
        #get siblings
        siblings={}
        for each in self.get_siblings():
            siblings[each.title]=each.get_absolute_url()
        nbh['siblings']=siblings
	nbh['count_siblings'] = len(nbh['siblings'])
        #get Relations
        relns={}
        rellft={}
        relrgt={}
        if self.get_relations1:
            NTrelns=self.get_relations1
            for key,value in NTrelns.items():
                if key=="rrelations":
                    relrgt={}
                    for rgtkey,rgtvalue in value.items():
                        relnvalue={}
                        if isinstance(rgtvalue,list):
                            for items in rgtvalue:
                                relnvalue[items]=items.get_absolute_url()
                        else:
                            relnvalue[rgtvalue]=rgtvalue.get_absolute_url()
                        
                        relrgt[rgtkey]=relnvalue
                    
                else:
                    rellft={}
                    relns['left']=rellft
                    for lftkey,lftvalue in value.items():
                        relnvalue={}
                        if isinstance(lftvalue,list):
                             for items in lftvalue:
                                 relnvalue[items]=items.get_absolute_url()
                        else:
                             relnvalue[lftvalue]=lftvalue.get_absolute_url()
                        
                        rellft[lftkey]=relnvalue
                    
        nbh['relations']=relrgt
	
        nbh['relations'].update(rellft)
	nbh['count_relations'] = len(nbh['relations'])
        #get Attributes
        attributes =self.get_attributes
        nbh['attributes']=attributes
	nbh['count_attributes'] = len(nbh['attributes'])
        #get ATs
        attributetypes={}
        for each in self.subjecttype_of.all():
            attributetypes[each.title]=each.get_absolute_url()
        nbh['ats']=attributetypes
        #get RTs as leftroles and rightroles
        leftroles = {} 
        for each in self.left_subjecttype_of.all():
            leftroles[each.title]=each.get_absolute_url()
        nbh['leftroles']=leftroles
	nbh['count_leftroles'] = len(nbh['leftroles'])
        rightroles = {} 
        for each in self.right_subjecttype_of.all():
            rightroles[each.title]=each.get_absolute_url()
        nbh['rightroles']=rightroles
	nbh['count_rightroles'] = len(nbh['rightroles'])
	
        return nbh
       
 
    @property
    def previous_nodetype(self):
        """Return the previous nodetype"""
        nodetypes = Nodetype.published.filter(
            creation_date__lt=self.creation_date)[:1]
        if nodetypes:
            return nodetypes[0]

    @property
    def next_nodetype(self):
        """Return the next nodetype"""
        nodetypes = Nodetype.published.filter(
            creation_date__gt=self.creation_date).order_by('creation_date')[:1]
        if nodetypes:
            return nodetypes[0]

    @property
    def word_count(self):
        """Count the words of a nodetype"""
        return len(strip_tags(self.html_content).split())

    @property
    def is_actual(self):
        """Check if a nodetype is within publication period"""
        now = datetime.now()
        return now >= self.start_publication and now < self.end_publication

    @property
    def is_visible(self):
        """Check if a nodetype is visible on site"""
        return self.is_actual and self.status == PUBLISHED

    @property
    def related_published(self):
        """Return only related nodetypes published"""
        return nodetypes_published(self.related)

    @property
    def discussions(self):
        """Return published discussions"""
        return comments.get_model().objects.for_model(
            self).filter(is_public=True)

    @property
    def comments(self):
        """Return published comments"""
        return self.discussions.filter(Q(flags=None) | Q(
            flags__flag=CommentFlag.MODERATOR_APPROVAL))

    @property
    def pingbacks(self):
        """Return published pingbacks"""
        return self.discussions.filter(flags__flag='pingback')

    @property
    def trackbacks(self):
        """Return published trackbacks"""
        return self.discussions.filter(flags__flag='trackback')

    @property
    def comments_are_open(self):
        """Check if comments are open"""
        if AUTO_CLOSE_COMMENTS_AFTER and self.comment_enabled:
            return (datetime.now() - self.start_publication).days < \
                   AUTO_CLOSE_COMMENTS_AFTER
        return self.comment_enabled

    @property
    def short_url(self):
        """Return the nodetype's short url"""
        return get_url_shortener()(self)

    def __unicode__(self):
        return self.title

    @property
    def memberof_sentence(self):
        """Return the metatype of which the nodetype is a member of"""
        
        if self.metatypes.count:
            for each in self.metatypes.all():
                return '%s is a member of metatype %s' % (self.title, each)
        return '%s is not a fully defined name, consider making it a member of a suitable metatype' % (self.title)

    
    @property
    def subtypeof_sentence(self):
        "composes the relation as a sentence in triple format."
        if self.parent:
            return '%s is a subtype of %s' % (self.title, self.parent.tree_path)
        return '%s is a root node' % (self.title)
    composed_sentence = property(subtypeof_sentence)

    def subtypeof(self):
        "retuns the parent nodetype."
        if self.parent:
            return '%s' % (self.parent.tree_path)
        return None 

    @models.permalink
    def get_absolute_url(self):
        """Return nodetype's URL"""
        return ('gstudio_nodetype_detail', (), {
            'year': self.creation_date.strftime('%Y'),
            'month': self.creation_date.strftime('%m'),
            'day': self.creation_date.strftime('%d'),
            'slug': self.slug})

    def get_serialized_data(self):
        """
        return the fields in a serialized form of the current object.
        get object id, go to version model, return serialized_data for the given id
        """
        from reversion.models import Version
        version = Version.objects.get(id=self.node_ptr_id)
        return version.serialized_data

    class Meta:
        """Nodetype's Meta"""
        ordering = ['-creation_date']
        verbose_name = _('node type')
        verbose_name_plural = _('node types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


class Objecttype(Nodetype):
    '''
    Object class
    '''

    def __unicode__(self):
        return self.title

    #def get_graph_json(self):
	
	

                    
    @property
    def get_attributetypes(self):        
        return self.subjecttype_of.all()

    @property
    def get_relationtypes(self):
        
        left_relset = self.left_subjecttype_of.all()  
        right_relset = self.right_subjecttype_of.all() 

        reltypes = {}
        reltypes['left_subjecttype_of']=left_relset
        reltypes['right_subjecttype_of']=right_relset
        return reltypes

    @property
    def get_left_subjecttypes(self):
        """
        for which relation types does this object become a domain of any relation type
        """
        reltypes = []
        left_relset = self.left_subjecttype_of.all()  
        for relationtype in left_relset:
	    reltypes.append(relationtype)
        return reltypes

    @property
    def get_rightroles(self):
        """
        for which relation types does this object become a domain of any relation type
        """
        reltypes = []
        right_relset = self.right_subjecttype_of.all()  
        for relationtype in right_relset:
	    reltypes.append(relationtype)
        return reltypes

    @property
    def get_subjecttypes(self):
        """
        for which relation types does this object become a domain of any relation type
        """
        subjecttypes = []
        attrset = self.subjecttype_of.all()  
        for subjecttype in attrset:
	    subjecttypes.append(subjecttype)
        return subjecttypes
        

    @property
    def member_of_metatypes(self):
        """
        returns if the objecttype is a member of the membership in a metatype class
        """
        types = []
        if self.metatypes.all():
            for metatype in self.metatypes.all():    
		types.append(metatype.title)
        return types


    @property
    def get_members(self):
        """
        get members of the object type
        """
        members = []
        if self.member_objects.all():
            for gbobject in self.member_objects.all():   
		members.append(gbobject)
        return members    

    @property
    def get_nbh(self):
        """          
        Returns the neighbourhood of the nodetype
        """
        nbh = {}
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames
        nbh['plural'] = self.plural        
        nbh['member_of_metatype'] = self.metatypes.all()
        # get all the ATs for the objecttype
        nbh['subjecttype_of']= self.subjecttype_of.all() 
        # get all the RTs for the objecttype        
        nbh.update(self.get_relationtypes) 
        if self.parent:
            nbh['type_of'] = [self.parent]

        nbh['contains_subtypes'] = Nodetype.objects.filter(parent=self.id)
        # get all the objects inheriting this OT 
        nbh['contains_members'] = self.member_objects.all()

        nbh['prior_nodes'] = self.prior_nodes.all()             

        nbh['posterior_nodes'] = self.posterior_nodes.all() 

	nbh['authors'] = self.authors.all()

	return nbh
    
    @property
    def get_rendered_nbh(self):
        """
        Returns the neighbourhood of the nodetype with the hyperlinks of nodes rendered
        """
        nbh = {}
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames
        nbh['plural'] = self.plural
        member_of_metatypes_list = []
        for each in self.metatypes.all():
            member_of_metatypes_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['member_of_metatypes'] = member_of_metatypes_list


        attributetypes_list = []
        for each in self.get_attributetypes:
           attributetypes_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['attributetypes'] = attributetypes_list


        # get all the RTs for the objecttype
        reltypes_list = []
        for each in self.get_relationtypes:
           reltypes_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['relationtypes'] = reltypes_list

        nbh['type_of'] = self.parent

        nbh['contains_subtypes'] = Nodetype.objects.filter(parent=self.id)
        # get all the objects inheriting this OT
        contains_members_list = []
        for each in self.gbobjects.all():
            contains_members_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['contains_members'] = contains_members_list
       
        prior_nodes_list = []
        for each in self.prior_nodes.all():
            prior_nodes_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['prior_nodes'] = prior_nodes_list
        
        posterior_nodes_list = []
        for each in self.posterior_nodes.all():
            posterior_nodes_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['posterior_nodes'] = posterior_nodes_list
        
        author_list = []
        for each in self.authors.all():
            author_list.append('<a href="%s"></a>' % (each.get_absolute_url()))
        nbh['authors'] = author_list
        return nbh



    class Meta:
        """
        object type's meta class
        """
        verbose_name = _('object type')
        verbose_name_plural = _('object types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )




class Relationtype(Nodetype):
    '''
    Properties with left and right subjects (Binary relations) are defined in this class.
    '''
    inverse = models.CharField(_('inverse name'), help_text=_('when subjecttypes are interchanged, what should be the name of the relation type? This is mandatory field. If the relation is symmetric, same name will do.'), max_length=255,db_index=True ) 
    left_subjecttype = models.ForeignKey(NID,related_name="left_subjecttype_of", verbose_name='left role')  
    left_applicable_nodetypes = models.CharField(max_length=2,choices=NODETYPE_CHOICES,default='OT', verbose_name='Node types for left role')
    left_cardinality = models.IntegerField(null=True, blank=True, verbose_name='cardinality for the left role')
    right_subjecttype = models.ForeignKey(NID,related_name="right_subjecttype_of", verbose_name='right role')  
    right_applicable_nodetypes = models.CharField(max_length=2,choices=NODETYPE_CHOICES,default='OT', verbose_name='Node types for right role')
    right_cardinality = models.IntegerField(null=True, blank=True, verbose_name='cardinality for the right role')
    is_symmetrical = models.NullBooleanField(verbose_name='Is symmetrical?')
    is_reflexive = models.NullBooleanField(verbose_name='Is reflexive?')
    is_transitive = models.NullBooleanField(verbose_name='Is transitive?')


    def get_serialized_data(self):
        """
        return the fields in a serialized form of the current object.
        get object id, go to version model, return serialized_data for the given id
        """
        from reversion.models import Version
        version = Version.objects.get(id=self.node_ptr_id)
        return version.serialized_data


    def __unicode__(self):
        return self.title

    class Meta:
        """
        relation type's meta class
        """
        verbose_name = _('relation type')
        verbose_name_plural = _('relation types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


class Attributetype(Nodetype):
    '''
    To define attributes of objects. First three fields are mandatory.
    The rest of the fields may be required depending on what type of
    field is selected for datatype. 
    '''
    subjecttype = models.ForeignKey(NID, related_name="subjecttype_of", verbose_name='subject type name')  
    applicable_nodetypes = models.CharField(max_length=2,choices=NODETYPE_CHOICES,default='OT', verbose_name='applicable nodetypes') 
    dataType = models.CharField(max_length=2, choices=FIELD_TYPE_CHOICES,default='01', verbose_name='data type of value') 
 
    verbose_name = models.CharField(max_length=500, null=True, blank=True, verbose_name='verbosename', help_text='verbose name')
    null = models.NullBooleanField(verbose_name='Null', help_text='can the value be null?')
    blank = models.NullBooleanField(verbose_name='Blank', help_text='can the form be left blank?')
    help_text = models.CharField(max_length=500, null=True, blank=True, verbose_name='Help text', help_text='help text for the field')
    max_digits = models.IntegerField(max_length=5, null=True, blank=True, verbose_name='Max digit', help_text='If you have selected Decimal Field for datatype, you have to specify the number of digits.')
    decimal_places = models.IntegerField(max_length=2, null=True, blank=True, verbose_name='Decimal places', help_text='If you have selected Decimal Field for datatype, you have to specify the decimal places.')
    auto_now = models.NullBooleanField(verbose_name='Auto now',  null=True, blank=True, help_text='Use this if DateTime & Time Field was chosen above for datatype') 
    auto_now_add = models.NullBooleanField(verbose_name='Auto now add',  null=True, blank=True, help_text='Use this if DateTime & Time Field was chosen above for datatype')
    upload_to = models.CharField(max_length=500,verbose_name='Upload to', null=True, blank=True, help_text='Required for FileField and ImageField')
    path=models.CharField(max_length=500,verbose_name='Path', null=True, blank=True, help_text='Required for FilePathField')
    verify_exists=models.NullBooleanField(verbose_name='Verify exits', null=True, blank=True, help_text='Required for AttributeURLField')
    min_length=models.IntegerField(max_length=10,null=True, blank=True, verbose_name='min length', help_text='minimum length')
    required=models.NullBooleanField(verbose_name='required', null=True, blank=True, help_text='Use this for setting mandatory and optional fields')
    label=models.CharField(max_length=500, null=True,blank=True,verbose_name='label',help_text='specify the "human-friendly" label')
    unique=models.NullBooleanField(verbose_name='unique', null=True, blank=True, help_text='If True, this field must be unique throughout the table')
    validators=models.ManyToManyField('self', verbose_name='validators',blank=True, null=True,help_text='A list of validators to run for this field')
    default=models.CharField(max_length=500, null=True, blank=True, verbose_name='default', help_text='The default value for the field')
    editable=models.NullBooleanField(verbose_name='required', null=True, blank=True, help_text='If False, the field will not be editable')
    

    def __unicode__(self):
        return self.title

    class Meta:
        """
        attribute type's meta class
        """
        verbose_name = _('attribute type')
        verbose_name_plural = _('attribute types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


    
class Relation(Edge):
    '''
    Relations, instances of relationtypes
    '''

    left_subject_scope = models.CharField(max_length=50, verbose_name='subject scope or qualification', null=True, blank=True)
    left_subject = models.ForeignKey(NID, related_name="left_subject_of", verbose_name='subject name') 
    relationtype_scope = models.CharField(max_length=50, verbose_name='relation scope or qualification', null=True, blank=True)
    relationtype = models.ForeignKey(Relationtype, verbose_name='relation name')
    right_subject_scope = models.CharField(max_length=50, verbose_name='object scope or qualification', null=True, blank=True)
    right_subject = models.ForeignKey(NID, related_name="right_subject_of", verbose_name='object name') 

    def ApplicableNodeTypes_filter(self,choice):

        nodeslist = []
        
        if choice == 'ED':
            nodeslist = Edge.objects.all()
	if choice == 'OB':
            nodeslist = Objects.objects.all()
        if choice == 'ND':
            nodeslist = Node.objects.all()
        if choice == 'NT':
            nodeslist = Nodetype.objects.all()
        if choice == 'OT':
            nodeslist = Objecttype.objects.all()
        if choice == 'RT':
            nodeslist = Relationtype.objects.all()
        if choice == 'MT':
            nodeslist = Metatype.objects.all()
        if choice == 'AT':
            nodeslist = Attributetype.objects.all()
        if choice == 'RN':
            nodeslist = Relation.objects.all()
        if choice == 'AS':
            nodeslist = Attribute.objects.all()
        if choice == 'ST':
            nodeslist = Systemtype.objects.all()
        if choice == 'SY':
            nodeslist = System.objects.all()
        
        return nodeslist
        

    class Meta:
        unique_together = (('left_subject_scope','left_subject','relationtype_scope', 'relationtype', 'right_subject_scope','right_subject'),)
        verbose_name = _('relation')
        verbose_name_plural = _('relations')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


    def __unicode__(self):
        return self.composed_sentence

    @property
    def composed_sentence(self):
        "composes the relation as a sentence in a triple format."
        return '%s %s %s %s %s %s' % (self.left_subject_scope, self.left_subject, self.relationtype_scope, self.relationtype, self.right_subject_scope, self.right_subject)

    @property
    def inversed_sentence(self):
        "composes the inverse relation as a sentence in a triple format."
        return '%s %s %s %s %s' % (self.objectScope, self.right_subject, self.relationtype.inverse, self.left_subject_scope, self.left_subject )

    @property
    def key_value(self):
        return dict({str(self.relationtype):str(self.right_subject)})

    @property
    def inverse_key_value(self):
        return dict({str(self.relationtype.inverse):str(self.left_subject)})


    @property
    def relation_sentence(self):
        """Return the relations of the objecttypes"""
        
        if self.relationtype:
           # for relation in self.relationtype():
                return '%s %s %s' % (self.left_subject,self.relationtype,self.right_subject )

    @property
    def partial_composition(self):
        '''
        function that composes the right_subject and relation name, as in "x as a friend", "y as a sibling"
        '''
        return '%s as a %s' % (self.right_subject, self.relationtype) 


class Attribute(Edge):
    '''
    Attribute value store for default datatype varchar. Subject can be any of the
    nodetypes. 
    '''

    subject_scope = models.CharField(max_length=50, verbose_name='subject scope or qualification', null=True, blank=True)
    subject = models.ForeignKey(NID, related_name="subject_of", verbose_name='subject name') 
    attributetype_scope = models.CharField(max_length=50, verbose_name='property scope or qualification', null=True, blank=True)
    attributetype = models.ForeignKey(Attributetype, verbose_name='property name')
    value_scope = models.CharField(max_length=50, verbose_name='value scope or qualification', null=True, blank=True)
    svalue  = models.CharField(max_length=100, verbose_name='serialized value') 
    

    
    class Meta:
        unique_together = (('subject_scope', 'subject', 'attributetype_scope', 'attributetype', 'value_scope', 'svalue'),)
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


    def subject_filter(self,attr):
        """
        returns applicaable selection of nodes for selecting as subject
        """
        subjecttype = attr.subjecttype

        for each in Objecttype.objects.all():
            if attr.subjecttype.id == each.id:
                return each.get_members
        


    def __unicode__(self):
        return self.composed_attribution

    @property
    def edge_node_dict(self):
        '''
        composes the attribution as a name:value pair sentence without the subject.
        '''
        return dict({str(self.attributetype_scope) + str(self.attributetype): str(self.value_scope)+ str(self.svalue)})

    @property
    def composed_sentence(self):
        '''
        composes the attribution as a sentence in a triple format.
        '''
        return '%s %s has %s %s %s %s' % (self.subject_scope, self.subject, self.attributetype_scope, self.attributetype, self.value_scope, self.svalue)

    @property
    def composed_attribution(self):
        '''
        composes a name to the attribute
        '''
        return 'the %s of %s is %s' % (self.attributetype, self.subject, self.svalue)
    
    @property
    def partial_composition(self):
        '''
        function that composes the value and attribute name, as in "red as color", "4 as length"
        '''
        return '%s as %s' % (self.svalue, self.attributetype) 


    def subject_filter(self,attr):
        """
        returns applicable selection of nodes for selecting objects
        """
        for each in Objecttype.objects.all():
            if attr.subjecttype.id == each.id:
                return each.get_members
                    
            
        
class AttributeCharField(Attribute):    

    value  = models.CharField(max_length=100, verbose_name='string') 

    def __unicode__(self):
        return self.title

class AttributeTextField(Attribute):
    
    value  = models.TextField(verbose_name='text') 

    def __unicode__(self):
        return self.title
    
class AttributeIntegerField(Attribute):
     value = models.IntegerField(max_length=100, verbose_name='Integer') 

     def __unicode__(self):
         return self.title

class AttributeCommaSeparatedIntegerField(Attribute):
    
    value  = models.CommaSeparatedIntegerField(max_length=100, verbose_name='integers separated by comma') 

    def __unicode__(self):
        return self.title

class AttributeBigIntegerField(Attribute):
    
    value  = models.BigIntegerField(max_length=100, verbose_name='big integer') 

    def __unicode__(self):
        return self.title

class AttributePositiveIntegerField(Attribute):
    
    value  = models.PositiveIntegerField(max_length=100, verbose_name='positive integer') 

    def __unicode__(self):
        return self.title

class AttributeDecimalField(Attribute):
    
    value  = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='decimal') 

    def __unicode__(self):
        return self.title

class AttributeFloatField(Attribute):
    
    value  = models.FloatField(max_length=100, verbose_name='number as float') 

    def __unicode__(self):
        return self.title

class AttributeBooleanField(Attribute):
    
    value  = models.BooleanField(verbose_name='boolean') 

    def __unicode__(self):
        return self.title

class AttributeNullBooleanField(Attribute):
    
    value  = models.NullBooleanField(verbose_name='true false or unknown') 

    def __unicode__(self):
        return self.title

class AttributeDateField(Attribute):
    
    value  = models.DateField(max_length=100, verbose_name='date') 

    def __unicode__(self):
        return self.title

class AttributeDateTimeField(Attribute):
    
    value  = models.DateTimeField(max_length=100, verbose_name='date time') 
    
    def __unicode__(self):
        return self.title
    
class AttributeTimeField(Attribute):
    
    value  = models.TimeField(max_length=100, verbose_name='time') 

    def __unicode__(self):
        return self.title

class AttributeEmailField(Attribute):
    
    value  = models.CharField(max_length=100,verbose_name='value') 

    def __unicode__(self):
        return self.title

class AttributeFileField(Attribute):
    
    value  = models.FileField(upload_to='/media', verbose_name='file') 

    def __unicode__(self):
        return self.title

class AttributeFilePathField(Attribute):
    
    value  = models.FilePathField(verbose_name='path of file') 

    def __unicode__(self):
        return self.title

class AttributeImageField(Attribute):
    
    value  = models.ImageField(upload_to='/media', verbose_name='image') 

    def __unicode__(self):
        return self.title

class AttributeURLField(Attribute):

    value  = models.URLField(max_length=100, verbose_name='url') 

    def __unicode__(self):
        return self.title

class AttributeIPAddressField(Attribute):

    value  = models.IPAddressField(max_length=100, verbose_name='ip address') 

    def __unicode__(self):
        return self.title


class Processtype(Nodetype):    

    """
    A kind of nodetype for defining processes or events or temporal
    objects involving change.  
    """
    changing_attributetype_set = models.ManyToManyField(Attributetype, null=True, blank=True,
                               verbose_name=_('attribute set involved in the process'),
                               related_name=' changing_attributetype_set_of')
    changing_relationtype_set = models.ManyToManyField(Relationtype, null=True, blank=True,
                               verbose_name=_('relation set involved in the process'),
                               related_name='changing_relationtype_set_of')


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('process type')
        verbose_name_plural = _('process types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )




class Systemtype(Nodetype):    

    """
    class to organize Systems
    """


    nodetype_set = models.ManyToManyField(Nodetype, related_name="nodetype_set_of", verbose_name='Possible edges in the system',    
                                           blank=True, null=False) 
    relationtype_set = models.ManyToManyField(Relationtype, related_name="relationtype_set_of", verbose_name='Possible nodetypes in the system',    
                                             blank=True, null=False) 
    attributetype_set = models.ManyToManyField(Attributetype, related_name="attributetype_set_of", verbose_name='systems to be nested in the system',
                                              blank=True, null=False)
    metatype_set = models.ManyToManyField(Metatype, related_name="metatype_set_of", verbose_name='Possible edges in the system',    
                                         blank=True, null=False) 
    processtype_set = models.ManyToManyField(Processtype, related_name="processtype_set_of", verbose_name='Possible edges in the system',    
                                            blank=True, null=False) 


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('system type')
        verbose_name_plural = _('system types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )
    

class AttributeSpecification(Node):
    """
    specifying an attribute by a subject to say for example:
    population of India, color of a flower etc.  These do not yeild a
    proposition but a description, which can be used as a subject in
    another sentence.
    """
    attributetype = models.ForeignKey(Attributetype, verbose_name='property name')
    subjects = models.ManyToManyField(NID, related_name="subjects_attrspec_of", verbose_name='subjects')


    @property
    def composed_subject(self):
        '''
        composes a name to the attribute
        '''
        subjects = u''
        for each in self.subjects.all():
            subjects = subjects + each.title + ' '
        return 'the %s of %s' % (self.attributetype, subjects)


    def __unicode__(self):
        return self.composed_subject


    class Meta:
        verbose_name = _('attribute specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


class RelationSpecification(Node):
    """
    specifying a relation with a subject 
    """
    relationtype = models.ForeignKey(Relationtype, verbose_name='relation name')
    subjects = models.ManyToManyField(NID, related_name="subjects_in_relspec", verbose_name='subjects')


    @property
    def composed_subject(self):
        '''
        composing an expression with relation name and subject
        '''
        subjects = u''
        for each in self.subjects.all():
            subjects = subjects + each.title + ' '
        return 'the %s of %s' % (self.relationtype, subjects)

    def __unicode__(self):
        return self.composed_subject


    class Meta:
        verbose_name = _('relation specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


class NodeSpecification(Node):
    """
    A node specified (described) by its relations or attributes or both.  
    """
    subject = models.ForeignKey(Node, related_name="subject_nodespec", verbose_name='subject name')
    relations = models.ManyToManyField(Relation, related_name="relations_in_nodespec", verbose_name='relations used to specify the domain')
    attributes = models.ManyToManyField(Attribute, related_name="attributes_in_nodespec", verbose_name='attributes used to specify the domain')

    @property
    def composed_subject(self):
        '''
        composing an expression subject and relations
        '''
        relations = u''
        for each in self.relations.all():
            relations = relations + each.partial_composition + ', '
        attributes = u''
        for each in self.attributes.all():
            attributes = attributes + each.partial_composition + ', '
        return 'the %s with %s, %s' % (self.subject, self.relations, self.attributes)

    def __unicode__(self):
        return self.composed_subject


    class Meta:
        verbose_name = _('Node specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )


class Expression(Node):
    """
    Expression constructor
    """

    left_term = models.ForeignKey(NID, related_name="left_term_of", verbose_name='left term name') 
    relationtype = models.ForeignKey(Relationtype, verbose_name='relation name')
    right_term = models.ForeignKey(NID, related_name="right_term_of", verbose_name='right term name') 


    def __unicode__(self):
        return self.composed_sentence

    @property
    def composed_sentence(self):
        "composes the relation as a sentence in a triple format."
        return '%s %s %s' % (self.left_term, self.relationtype, self.right_term)


    class Meta:
        unique_together = (('left_term','relationtype','right_term'),)
        verbose_name = _('expression')
        verbose_name_plural = _('expressionss')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )



class Union(Node):
    """
    union of two classes
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'union_of', verbose_name='node types for union')
        
    def __unicode__(self):
        return self.title



class Complement(Node):
    """
    complement of a  class
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'complement_of', verbose_name='complementary nodes')
        
    def __unicode__(self):
        return self.title

class Intersection(Node):
    """
    Intersection of classes
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'intersection_of', verbose_name='intersection of classes')
        
    def __unicode__(self):
        return self.title
    

reversion.register(NID)

if not reversion.is_registered(Systemtype):
    reversion.register(Systemtype)

if not reversion.is_registered(Objecttype):
    reversion.register(Objecttype , follow=["nodetype_ptr"])

if not reversion.is_registered(Node):
    reversion.register(Node , follow=["nid_ptr"])

if not reversion.is_registered(Edge):
    reversion.register(Edge , follow=["nid_ptr"])


if not reversion.is_registered(Processtype):
    reversion.register(Processtype, follow=["changing_attributetype_set", "changing_relationtype_set"])

if not reversion.is_registered(Nodetype): 
    reversion.register(Nodetype, follow=["node_ptr","parent", "metatypes","prior_nodes", "posterior_nodes"])

if not reversion.is_registered(Metatype):
    reversion.register(Metatype, follow=["node_ptr","parent"])


if not reversion.is_registered(Relationtype): 
    reversion.register(Relationtype, follow=["left_subjecttype", "right_subjecttype"])

if not reversion.is_registered(Attributetype): 
    reversion.register(Attributetype, follow=["subjecttype"])

if not reversion.is_registered(Attribute): 
    reversion.register(Attribute, follow=["subject", "attributetype"])

if not reversion.is_registered(Relation): 
    reversion.register(Relation, follow=["left_subject", "right_subject", "relationtype"])

moderator.register(Nodetype, NodetypeCommentModerator)
mptt.register(Metatype, order_insertion_by=['title'])
mptt.register(Nodetype, order_insertion_by=['title'])
mptt.register(Objecttype, order_insertion_by=['title'])
mptt.register(Relationtype, order_insertion_by=['title'])
mptt.register(Attributetype, order_insertion_by=['title'])
mptt.register(Systemtype, order_insertion_by=['title'])
mptt.register(Processtype, order_insertion_by=['title'])
post_save.connect(ping_directories_handler, sender=Nodetype,
                  dispatch_uid='gstudio.nodetype.post_save.ping_directories')
post_save.connect(ping_external_urls_handler, sender=Nodetype,
                  dispatch_uid='gstudio.nodetype.post_save.ping_external_urls')

class Peer(User):
    """Subclass for non-human users"""
    def __unicode__(self):
        return self.ip

    ip = models.IPAddressField("Peer's IP address")
    pkey = models.CharField(("Peer's public-key"), max_length=255)
