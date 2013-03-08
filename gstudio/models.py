
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



"""Storage models of gnowsys-studio, all types, relations  """

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
from gstudio.settings import GSTUDIO_VERSIONING
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
if GSTUDIO_VERSIONING:
    import reversion
from reversion.models import Version
from django.core import serializers
from reversion.models import *
from reversion.helpers import *
import ast


NODETYPE_CHOICES = (
    ('ND', 'Nodes'),
    ('OB' ,'Objects'),
    ('ED', 'Edges'),
    ('NT', 'Node types'),
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


counter = 1
attr_counter = -1

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
    nodemodel = models.CharField(_('nodemodel'),max_length=255)

    @property
    def get_revisioncount(self):
        """
        Returns Number of Version
        """
        i=0
        ver=Version.objects.get_for_object(self)
        for each in ver:
            i=i+1
        return i

    @property
    def get_version_list(self):
        """
        Returns  Version list
        """
        ver=Version.objects.get_for_object(self)
        return ver

    @property
    def get_ssid(self):
        """
        return snapshot ids (revision id).
        returns a list.
        """
        slist=[]
        vlist=self.get_version_list
        for each in vlist:
            slist.append(each.id)
        return slist

    def version_info(self,ssid):
        version_object=Version.objects.get(id=ssid)
        return version_object.field_dict


    def get_version_nbh(self,ssid):
        """
        Returns Version nbh
        """
        ver_dict=self.version_info(ssid)
        ver_nbh_list=[]
        ver_nbh_dict={}
        for item in self.get_nbh.keys():
            if item in ver_dict.keys():
                ver_nbh_list.append(item)
        for each in ver_nbh_list:
            ver_nbh_dict[each]=ver_dict[each]
        return ver_nbh_dict

    def get_serialized_dict(self):
        """
        return the fields in a serialized form of the current object using the __dict__ function.
        """
        return self.__dict__

    @models.permalink
    def get_absolute_url(self):
        """Return nodetype's URL"""
        if self.ref.__class__.__name__=='Gbobject' or self.ref.__class__.__name__=='Process' or self.ref.__class__.__name__=='System':
            return('objectapp_gbobject_detail',(),{
                    'year':self.creation_date.strftime('%Y'),
                    'month':self.creation_date.strftime('%m'),
                    'day':self.creation_date.strftime('%d'),
                    'slug':self.slug})
        else:
            return ('gstudio_nodetype_detail', (), {
                    'year': self.creation_date.strftime('%Y'),
                    'month': self.creation_date.strftime('%m'),
                    'day': self.creation_date.strftime('%d'),
                    'slug': self.slug})

    @property
    def ref(self):
        from objectapp.models import *
        return eval(self.nodemodel).objects.get(id=self.id)

        # """
        # Returns the object reference the id belongs to.
        # """
        # try:
        #     """
        #     ALGO:     get object id, go to version model, return for the given id.
        #     """

        #     # Retrieving only the relevant tupleset for the versioned objects
        #     # vrs = Version.objects.filter(type=0 , object_id=self.id)
        #     # Returned value is a list, so splice it.
        #     vrs =  vrs[0]
        # except:
        #     return None
        # return vrs.object


    @property
    def reftype(self):
        """
        Returns the type the id belongs to.
        """
        try:
            """
            ALGO: simple wrapper for the __class__.__name__ so that it can be used in templates

            """
            # return self.__class__.__name__
            obj = self.ref
            return obj.__class__.__name__

        except:
            return None

    @property
    def getat(self):

        """This is will give the possible attributetypes """
        try:
            pt = []
            attributetype = []
            returndict = {}

            pt.append(self.ref)
            obj = self.ref
            while obj.parent:
                pt.append((obj.parent).ref)
                obj=obj.parent

            for each in pt:
                attributetype.append(each.subjecttype_of.all())

            attributetype = [num for elem in attributetype for num in elem]

            for i in attributetype:
                if str(i.applicable_nodetypes) == 'OT':
                    returndict.update({str(i.title):i.id})

            return returndict.keys()
        except:
            return None

    @property
    def getrt(self):
        """pt =[] contains parenttype
        reltype =[] contains relationtype
        titledict = {} contains relationtype's title
        inverselist = [] contains relationtype's inverse
        finaldict = {} contains either title of relationtype or inverse of relationtype
        listval=[] contains keys of titledict to check whether parenttype id is equals to listval's left or right subjecttypeid"""

        pt =[]
        reltype =[]
        titledict = {}
        inverselist = []
        finaldict = {}
        listval=[]

        pt.append(self.ref)
        obj = self.ref
        while obj.parent:
            pt.append((obj.parent).ref)
            obj=obj.parent

        for i in range(len(pt)):
            if Relationtype.objects.filter(left_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.filter(left_subjecttype = pt[i].id))
            if Relationtype.objects.filter(right_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.filter(right_subjecttype = pt[i].id))
        reltype = [num for elem in reltype for num in elem] #this rqud for filtering

        for i in reltype:
            titledict.update({i.title:i.id})


        for i in range(len(titledict)):
            listval.append(Relationtype.objects.get(title = titledict.keys()[i]))
            obj=Relationtype.objects.get(title=titledict.keys()[i])
            inverselist.append(str(obj.inverse))

        for j in range(len(pt)):
            for i in range(len(listval)):
                if pt[j].id == listval[i].left_subjecttype_id and str(listval[i].left_applicable_nodetypes) == 'OT' :
                    finaldict.update({titledict.keys()[i]:titledict.values()[i]})
                if pt[j].id == listval[i].right_subjecttype_id and str(listval[i].right_applicable_nodetypes)=='OT':
                    finaldict.update({inverselist[i]:titledict.values()[i]})


        return finaldict.keys()


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
    nbhood = models.TextField(help_text="The rendered neighbourhood of the model.")
    # nbh = models.TextField(help_text="The neighbourhood of the model.")

    published = NodePublishedManager()
    def __unicode__(self):
        title=self.title
        modelname=self.nodemodel
        displayname=modelname+": "+title
        return displayname

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
        nbh['contains_members'] = self.nodetypes_published()
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
        history=[]
        version_list=self.get_ssid
        if version_list:
            length=len(version_list)
            history_ssid=version_list[length-1]
            history_dict=self.version_info(history_ssid)
            history_nbh_dict=ast.literal_eval(history_dict['nbhood'])
            #ssid_current.append(history_ssid)
            history=history_nbh_dict['history']
            history.append(history_ssid)
        else:
            history.append(0)
        nbh = {}
        history_list=self.get_ssid
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames
        nbh['plural'] = self.plural

        if self.parent:
            obj=NID.objects.get(id=self.parent)
            typeof[parent] = obj.ref.get_absolute_url()
            #nbh['typeof'] = self.parent
        # generate ids and names of children
            nbh['contains_subtypes'] = self.children.get_query_set()
        contains_members_list = []
        for each in self.nodetypes_published():
            contains_members_list.append('<a href="%s">%s</a>' % (each.get_absolute_url(), each.title))
        nbh['contains_members'] = contains_members_list
        nbh['left_subjecttype_of'] = Relationtype.objects.filter(left_subjecttype=self.id)
        nbh['right_subjecttype_of'] = Relationtype.objects.filter(right_subjecttype=self.id)
        nbh['attributetypes'] = Attributetype.objects.filter(subjecttype=self.id)
        nbh['history']=history

        return nbh


    @property
    def tree_path(self):
        """Return metatype's tree path, by its ancestors"""
        if self.parent:
            return u'%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    def __unicode__(self):
        displayname="MT: "+self.title
        return displayname

    @property
    def composed_sentence(self):
        "composes the relation as a sentence in triple format."
        if self.parent:
            return u'%s is a kind of %s' % (self.title, self.parent.tree_path)
        return u'%s is a root node'  % (self.slug)


    @models.permalink
    def get_absolute_url(self):
        """Return metatype's URL"""
        return ('gstudio_metatype_detail', (self.tree_path,))


    class Meta:
        """Metatype's Meta"""
        ordering = ['title']
        verbose_name = _('metatype')
        verbose_name_plural = _('metatypes')

    # Save for metatype

    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        super(Metatype, self).save(*args, **kwargs) # Call the "real" save() method.
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Metatype, self).save(*args, **kwargs) # Call the "real" save() method.

class Edge(NID):
    
    metatypes = models.ManyToManyField(Metatype, verbose_name=_('member of metatypes'),
                                       related_name='member_edges',
                                       blank=True, null=True)
    
    def __unicode__(self):
        displayname="ED: " + self.title
        return displayname

    class Meta:
        """ Meta class for Edge """

    def save(self, *args, **kwargs):
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Edge, self).save(*args, **kwargs) # Call the "real" save() method.

        super(Edge, self).save(*args, **kwargs) # Call the "real" save() method.



class Nodetype(Node):
    """
    Model design for publishing nodetypes.  Other nodetypes inherit this class.
    """



    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    content = models.TextField(_('content'), null=True, blank=True)
    content_org = models.TextField(_('content_org'), null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               verbose_name=_('is a kind of'),
                               related_name='children')

    prior_nodes = models.ManyToManyField('self', symmetrical=False,null=True, blank=True,
                               verbose_name=_('its meaning depends on '),
                               related_name='nodetype_prior_nodes')

    posterior_nodes = models.ManyToManyField('self', symmetrical=False,null=True, blank=True,
                               verbose_name=_('required for the meaning of '),
                               related_name='nodetype_posterior_nodes')

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
    def get_edit_url_for_ats(self):
        '''
        Get all the attributes from get_rendered_nbh and return their URLs
        '''
        retdict={}
        for key,value in self.get_rendered_nbh.items():
            if key:
                if key=='attributes':
                    for akey,avalue in value.items():
                        ats=Attributetype.objects.filter(title=akey)
                        if ats:
                            ats=Attributetype.objects.get(title=akey)
                            for atrbs in Attribute.objects.all():
                                if  atrbs.attributetype_id==ats.id:
                                    gid=NID.objects.get(id=atrbs.id).ref.get_edit_url
                                    retdict[gid]=atrbs.svalue

        return retdict
    @property
    def get_at_url_add(self):
        """
        Gets all the ATs(excluding those for which the Attributes are already added) with their urls for adding attributes
        Get all ATs of NT. Get the attribute-model-name from its 'dataType'. Check whether entry exists in Attribute table for this AT.
        Else return it along with its admin-add-form-url.
        """
        retats={}
        ats=self.subjecttype_of.all()
        if ats:
            for each in ats:

                if each.applicable_nodetypes=='OT':
                    atdatatype=each.dataType
                    if atdatatype=='1':
                        model= 'CharField'
                    if atdatatype=='2':
                        model='TextField'
                    if atdatatype=='3':
                        model='IntegerField'
                    if atdatatype=='4':
                        model='CommaSeparatedIntegerField'
                    if atdatatype=='5':
                        model='BigIntegerField'
                    if atdatatype=='6':
                        model='PositiveIntegerField'
                    if atdatatype=='7':
                        model='DecimalField'
                    if atdatatype=='8':
                        model='FloatField'
                    if atdatatype=='9':
                        model='BooleanField'
                    if atdatatype=='10':
                        model='NullBooleanField'
                    if atdatatype=='11':
                        model='DateField'
                    if atdatatype=='12':
                        model='DateTimeField'
                    if atdatatype=='13':
                        model='TimeField'
                    if atdatatype=='14':
                        model= 'EmailField'
                    if atdatatype=='15':
                        model='FileField'
                    if atdatatype=='16':
                        model='FilePathField'
                    if atdatatype=='17':
                        model='ImageField'
                    if atdatatype=='18':
                        model='URLField'
                    if atdatatype=='19':
                        model='IPAddressField'
                    aturl="admin/gstudio/attribute"+model.lower()+"/add/?attributetype="+str(each.id)+"&subject="+str(self.id)
                    atsubject=self.subject_of.all()
                    """
                    check whether Attribute for the current AT is already added or not
                    """
                    fl=0
                    for eachs in atsubject:
                        if eachs.attributetype_id==each.id and eachs.subject_id==each.subjecttype.id:
                            fl=1
                    """
                    fl=0 means, Attribute for AT is not added, now show it as to be added
                    """
                    if fl==0:
                        retats[each.title]=aturl

            return retats


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


    def get_graph_json(self):
        
        
        
	g_json = {}
	g_json["node_metadata"]= [] 
	g_json["relations"]=[]
	

	global counter 
	global attr_counter
	nbh = self.get_nbh
	predicate_id = {}
        
        for key in nbh.keys():
            val = str(counter) + "b"
            predicate_id[key] = val
            counter = counter + 1
        #print predicate_id

       

        this_node = {"_id":str(self.id),"title":self.title,"screen_name":self.title, "url":self.get_absolute_url(),"refType":self.reftype}
        g_json["node_metadata"].append(this_node)      
	

	for key in predicate_id.keys():
		if nbh[key]:
                    try:
				
                        g_json["node_metadata"].append({"_id":str(predicate_id[key]),"screen_name":key})
                        
                        g_json["relations"].append({"from":self.id ,"type":str(key),"value":1,"to":predicate_id[key] })

                        if not isinstance(nbh[key],basestring) and len(nbh[key])<=10:
                            for item in nbh[key]:
                                if isinstance(item,unicode):
                                    g_json["node_metadata"].append({"_id":(str(attr_counter)+"b"),"screen_name":str(item)})
                                    g_json["relations"].append({"from":predicate_id[key] ,"type":str(key) ,"value":1,"to":(str(attr_counter)+"b") })
                                    attr_counter-=1
                                    
                                elif item.reftype!="Relation":
                                    # create nodes
                                    g_json["node_metadata"].append({"_id":str(item.id),"screen_name":item.title,"title":self.title, "url":item.get_absolute_url(),"refType":item.reftype})
                                    g_json["relations"].append({"from":predicate_id[key] ,"type":str(key), "value":1,"to":item.id  })
                                    
                                else:
                                    
                                    if item.left_subject.id==self.id:
                                        item1=item.right_subject
                                        flag=1
                                        
                                    elif item.right_subject.id==self.id:
                                        item1=item.left_subject
                                        flag=0						
                                        
                                    g_json["node_metadata"].append({"_id":str(item1.id),"screen_name":item1.title,"title":self.title, "url":item1.get_absolute_url(),"refType":item.reftype,"inverse":item.relationtype.inverse,"flag":flag})
                                        
                                        
                                    g_json["relations"].append({"from":predicate_id[key] ,"type":str(key), "value":1,"to":item1.id  })
                        else:
                            if not isinstance(nbh[key],basestring):
                                g_json["node_metadata"].append({"_id":(str(attr_counter))+"a","screen_name":str(len(nbh[key]))+" nodes...","title":str(key),"url":"/nodetypes/graphs/graph_label/"+str(self.id)+"/"+str(key)})
					#g_json["relations"].append({"from":predicate_id[key] ,"type":str(key) ,"value":1,"to":(str(attr_counter))})
                            else:
                                g_json["node_metadata"].append({"_id":(str(attr_counter)+"a"),"screen_name":nbh[key]})
    
                            g_json["relations"].append({"from":predicate_id[key] ,"type":str(key) ,"value":1,"to":(str(attr_counter)+"a")})

                            attr_counter-=1

                    except:
                            pass
                            
        #print g_json
        return json.dumps(g_json)   


    def get_label(self,key):
        nbh=self.get_nbh
        list_of_nodes=[]
        for item in nbh[key]:
            node=NID.objects.get(id=item.id)
            node=node.ref
            list_of_nodes.append(node)
        return list_of_nodes

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
    def tree_path(self):
        """Return nodetype's tree path, by its ancestors"""
        if self.parent:
            return u'%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    @property
    def tree_path_sentence(self):
        """ Return the parent of the nodetype in a triple form """
        if self.parent:
            return u'%s is a kind of %s' % (self.title, self.parent.tree_path)
        return u'%s is a root node' % (self.title)


    @property
    def html_content(self):
        """Return the content correctly formatted"""
        if MARKUP_LANGUAGE == 'markdown':
            return markdown(self.content, MARKDOWN_EXTENSIONS)
        elif MARKUP_LANGUAGE == 'textile':
            return textile(self.content)
        elif MARKUP_LANGUAGE == 'restructuredtext':
            return restructuredtext(self.content)
        # elif not '</p>' in self.content:
        #     return linebreaks(self.content)
        return self.content
    @property
    def get_relations(self):
        relation_set = {}
        # ALGO to find the relations and their left-subjecttypes and right_subjecttypes
        # 1. Get the relations containing a reference to the object. Retrieve where it occurs (left or right)
        # 2. Find out which RT they come from.
        # 3. For each RT, create a dict key and a value as a dict. And add the relation as a new key-value pair (rid:subject).
        # 4. If self is in right value, then add inverse relation as RT and add the relation as a new key-value pair (rid:subject).

        left_relset = Relation.objects.filter(left_subject=self.id) 
        right_relset = Relation.objects.filter(right_subject=self.id) 
        
        #return left_relset + right_relset

        # RT dictionary to store a single relation
        rel_dict ={}
        rel_dict['left-subjecttypes'] = {}
        rel_dict['right_subjecttypes'] ={}

               
        for relation in left_relset:
            # check if relation already exists
            if relation.relationtype.title not in rel_dict['left-subjecttypes'].keys():
                # create a new list field and add to it
                rel_dict['left-subjecttypes'][str(relation.relationtype.title)] = []
            # add 
            rel_dict['left-subjecttypes'][str(relation.relationtype.title)].append(relation) 

        for relation in right_relset:
            # check if relation exists
            if relation.relationtype.inverse not in rel_dict['right_subjecttypes'].keys():
                # create a new list key field and add to it
                rel_dict['right_subjecttypes'][str(relation.relationtype.inverse)] = []
                # add to the existing key
            rel_dict['right_subjecttypes'][str(relation.relationtype.inverse)].append(relation)

        relation_set.update(rel_dict['left-subjecttypes'])
        relation_set.update(rel_dict['right_subjecttypes'])
        
        return relation_set

    @property
    def get_rendered_relations(self):
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
        objref=str(self.ref)
        reftitle=str(self.ref.title)
        objref=objref.replace(reftitle,"")
        objtype=objref.strip()
        return objtype + " " + self.title
    

    @property
    def memberof_sentence(self):
        """Return the metatype of which the nodetype is a member of"""

        if self.metatypes.count:
            for each in self.metatypes.all():
                return u'%s is a member of metatype %s' % (self.title, each)
        return u'%s is not a fully defined name, consider making it a member of a suitable metatype' % (self.title)


    @property
    def subtypeof_sentence(self):
        "composes the relation as a sentence in triple format."
        if self.parent:
            return u'%s is a subtype of %s' % (self.title, self.parent.tree_path)
        return u'%s is a root node' % (self.title)
    composed_sentence = property(subtypeof_sentence)

    def subtypeof(self):
        "retuns the parent nodetype."
        if self.parent:
            return u'%s' % (self.parent.tree_path)
        return None

    @models.permalink
    def get_absolute_url(self):
        """Return nodetype's URL"""
        return ('gstudio_nodetype_detail', (), {
            'year': self.creation_date.strftime('%Y'),
            'month': self.creation_date.strftime('%m'),
            'day': self.creation_date.strftime('%d'),
            'slug': self.slug})
    def get_version_url(self):
        """Return nodetype's URL"""
        return "/nodetypes/display/viewhistory/"

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
        displayname="OT: "+self.title
        return displayname


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
        # Looks like somebody forgot relations !
        nbh.update(self.get_relations)
        if self.parent:
            nbh['type_of'] = [self.parent]

        nbh['contains_subtypes'] = Nodetype.objects.filter(parent=self.id)
        # get all the objects inheriting this OT
        nbh['contains_members'] = self.member_objects.all()

        nbh['prior_nodes'] = self.prior_nodes.all()

        nbh['posterior_nodes'] = self.posterior_nodes.all()

        #nbh['authors'] = self.authors.all()

        return nbh
    @property
    def get_rendered_nbh(self):
        """
        Returns the neighbourhood of the nodetype
        """
        history=[]
        version_list=self.get_ssid
        if version_list:
            length=len(version_list)
            history_ssid=version_list[length-1]
            history_dict=self.version_info(history_ssid)
            # history_nbh_dict=ast.literal_eval(history_dict['nbhood'])
            #ssid_current.append(history_ssid)
            # history=history_nbh_dict['history']
            history.append(history_ssid)
        else:
            history.append(0)
        nbh = {}
        nbh['title'] = self.title
        nbh['count_title'] = len(nbh['title'])
        nbh['altnames'] = self.altnames
        nbh['count_altnames'] = len(nbh['altnames'])
        nbh['plural'] = self.plural
        #nbh['count_plural'] = len(nbh['plural'])
        #get all MTs
        member_of_dict = {}
        for each in self.metatypes.all():
            member_of_dict[each.title]= each.get_absolute_url()
        nbh['member_of_metatypes']=member_of_dict
        nbh['count_member_of_metatypes'] = len(nbh['member_of_metatypes'])
        typeof={}
        parentid=self.parent_id
        if parentid:
            parent=Nodetype.objects.get(id=parentid)
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
        if self.get_rendered_relations:
            NTrelns=self.get_rendered_relations
            for key,value in NTrelns.items():
                if key=="rrelations":
                    relrgt={}
                    for rgtkey,rgtvalue in value.items():
                        relnvalue={}
                        if isinstance(rgtvalue,list):
                            for items in rgtvalue:
                                relnvalue[items.title]=items.get_absolute_url()
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
                                relnvalue[items.title]=items.get_absolute_url()
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
        nbh['history']=history
        return nbh

    def get_Version_graph_json(self,ssid):


        # # predicate_id={"plural":"a1","altnames":"a2","contains_members":"a3","contains_subtypes":"a4","prior_nodes":"a5", "posterior_nodes":"a6"}
        # slist=self.get_ssid
        ver_dict=self.version_info(ssid)
        ver_dict1=self.version_info(ssid)
        #ver_dict=str(ver['nbhood'])
        ver_dict=ast.literal_eval(ver_dict['nbhood'])
        g_json = {}
        g_json["node_metadata"]= []
        g_json["relations"]=[]
        predicate_id = {}
        counter=1
        attr_counter=-1
        for key in ver_dict.keys():
            val = "a" + str(counter)
            predicate_id[key] = val
            counter = counter + 1
        #print predicate_id


        this_node = {"_id":str(self.id),"title":self.title,"screen_name":self.title, "url":self.get_absolute_url(),"refType":self.reftype}
        g_json["node_metadata"].append(this_node)


        for key in predicate_id.keys():
            if (ver_dict[key] and (ver_dict[key])!=0 and not(isinstance(ver_dict[key],int ) )
) :
                try:
                    g_json["node_metadata"].append({"_id":str(predicate_id[key]),"screen_name":key})
                    g_json["relations"].append({"from":self.id , "to":predicate_id[key],"value":1, "type":str(key) })
                    if not isinstance(ver_dict[key],basestring):
                        for item in ver_dict[key]:
                            # user
                            g_json["node_metadata"].append({"_id":(str(attr_counter)+"aa"),"screen_name":item })
                                    #create links
                            g_json["relations"].append({"from":predicate_id[key] ,"type":str(key), "value":1,"to":(str(attr_counter)+"aa")  })
                            attr_counter-=1

                    else:
                        g_json["node_metadata"].append({"_id":(str(attr_counter)+"a"),"screen_name":ver_dict[key]})
                        g_json["relations"].append({"from":predicate_id[key] , "to":(str(attr_counter)+"a") ,"value":1, "type":str(key) })
                        attr_counter-=1

                except:
                    pass
        # print g_json



        return json.dumps(g_json)


    class Meta:
        """
        object type's meta class
        """
        verbose_name = _('object type')
        verbose_name_plural = _('object types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # Save for Objecttype
    # @reversion.create_revision()
    def save(self,*args, **kwargs):
        self.nodemodel = self.__class__.__name__
        super(Objecttype, self).save(*args, **kwargs) # Call the "real" save() method.
        self.nbhood=self.get_rendered_nbh
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                self.nodemodel = self.__class__.__name__
                if self.parent:
                    ot=NID.objects.get(id=self.parent.id)
                    ot.ref.save()
                super(Objecttype, self).save(*args, **kwargs) # Call the "real" save() method.

    def save_revert_or_merge(self,*args, **kwargs):
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Objecttype, self).save(*args, **kwargs) # Call the "real" save() method.




class Relationtype(Nodetype):
    '''
    Properties with left and right subjects (Binary relations) are defined in this class.
    '''
    inverse = models.CharField(_('inverse name'), help_text=_('when subjecttypes are interchanged, what should be the name of the relation type? This is mandatory field. If the relation is symmetric, same name will do.'), max_length=255,db_index=True )
    left_subjecttype = models.ForeignKey(NID,related_name="left_subjecttype_of", verbose_name='left role')
    left_applicable_nodetypes = models.CharField(max_length=2,choices=NODETYPE_CHOICES,default='OT', verbose_name='Applicable node types for left role')
    left_cardinality = models.IntegerField(null=True, blank=True, verbose_name='cardinality for the left role')
    right_subjecttype = models.ForeignKey(NID,related_name="right_subjecttype_of", verbose_name='right role')
    right_applicable_nodetypes = models.CharField(max_length=2,choices=NODETYPE_CHOICES,default='OT', verbose_name='Applicable node types for right role')
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
        displayname="RT: "+self.title
        return displayname

    @property

    def get_rendered_nbh(self):
        """
        Returns the neighbourhood of the Relationtype
        """
        history=[]
        version_list=self.get_ssid
        if version_list:
            length=len(version_list)
            history_ssid=version_list[length-1]
            history_dict=self.version_info(history_ssid)
            history_nbh_dict=ast.literal_eval(history_dict['nbhood'])
            #ssid_current.append(history_ssid)
            history=history_nbh_dict['history']
            history.append(history_ssid)
        else:
            history.append(0)
        nbh = {}
        nbh['title'] = self.title
        nbh['count_title'] = len(nbh['title'])
        nbh['altnames'] = self.altnames
        nbh['count_altnames'] = len(nbh['altnames'])
        nbh['plural'] = self.plural
#       nbh['count_plural'] = len(nbh['plural'])
        #get all MTs
        member_of_dict = {}
        for each in self.metatypes.all():
            member_of_dict[each.title]= each.get_absolute_url()
        nbh['member_of_metatypes']=member_of_dict
        nbh['count_member_of_metatypes'] = len(nbh['member_of_metatypes'])
        typeof={}
        parent=self.parent_id
        if parent:
            obj=NID.objects.get(id=parent)
            typeof[parent] = obj.ref.get_absolute_url()
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
        if self.get_rendered_relations:
            NTrelns=self.get_rendered_relations
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
        nbh['history']=history
        return nbh



    def get_nbh(self):
        """
        Returns the neighbourhood of the nodetype
        """
        nbh = {}
        nbh['title'] = self.title
        nbh['altnames'] = self.altnames
        nbh['plural'] = self.plural

        nbh['contains_subtypes'] = Nodetype.objects.filter(parent=self.id)
        nbh['contains_members'] = self.member_objects.all()
        nbh['prior_nodes'] = self.prior_nodes.all()
        nbh['posterior_nodes'] = self.posterior_nodes.all()
        nbh['inverse']=self.inverse
        nbh['left_subjecttype']=self.left_subjecttype
        nbh['left_applicable_nodetypes']=self.left_applicable_nodetypes
        nbh['left_cardinality']=self.left_cardinality
        nbh['right_subjecttype']=self.right_subjecttype
        nbh['right_applicable_nodetypes']=self.right_applicable_nodetypes
        nbh['right_cardinality']=self.right_cardinality
        nbh['is_symmetrical']=self.is_symmetrical
        nbh['is_reflexive']=self.is_reflexive
        nbh['is_transitive']=self.is_transitive



        return nbh



    class Meta:
        """
        relation type's meta class
        """
        verbose_name = _('relation type')
        verbose_name_plural = _('relation types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # Save for Relationtype
    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        super(Relationtype, self).save(*args, **kwargs) # Call the "real" save() method.
        self.nbhood=self.get_rendered_nbh
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                self.nodemodel = self.__class__.__name__
                super(Relationtype, self).save(*args, **kwargs) # Call the "real" save() method.



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



    @property
    def get_rendered_nbh(self):
        """
        Returns the neighbourhood of the Attributetype
        """
        history=[]
        version_list=self.get_ssid
        if version_list:
            length=len(version_list)
            history_ssid=version_list[length-1]
            history_dict=self.version_info(history_ssid)
            history_nbh_dict=ast.literal_eval(history_dict['nbhood'])
            #ssid_current.append(history_ssid)
            history=history_nbh_dict['history']
            history.append(history_ssid)
        else:
            history.append(0)
        nbh = {}
        nbh['title'] = self.title
        nbh['count_title'] = len(nbh['title'])
        nbh['altnames'] = self.altnames
        nbh['count_altnames'] = len(nbh['altnames'])
       # nbh['plural'] = self.plural
       # nbh['count_plural'] = len(nbh['plural'])
        #get all MTs
        member_of_dict = {}
        for each in self.metatypes.all():
            member_of_dict[each.title]= each.get_absolute_url()
        nbh['member_of_metatypes']=member_of_dict
        nbh['count_member_of_metatypes'] = len(nbh['member_of_metatypes'])
        typeof={}
        parent=self.parent_id
        if parent:
            obj=NID.objects.get(id=parent)
            typeof[parent] = obj.ref.get_absolute_url()
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
        if self.get_rendered_relations:
            NTrelns=self.get_rendered_relations
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
        nbh['history']=history

        return nbh


    def __unicode__(self):
        displayname="AT: "+self.title
        return displayname


    @property
    def getdataType(self):
        at = 'attribute'+str(self.get_dataType_display())
        at = at.lower()
        return at

    class Meta:
        """
        attribute type's meta class
        """
        verbose_name = _('attribute type')
        verbose_name_plural = _('attribute types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # Save for Attributetype

    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        super(Attributetype, self).save(*args, **kwargs) # Call the "real" save() method.
        self.nbhood=self.get_rendered_nbh
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Attributetype, self).save(*args, **kwargs) # Call the "real" save() method.
    def save_revert_or_merge(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Attributetype, self).save(*args, **kwargs) # Call the "real" save() method.



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
        displayname="RN: "+self.composed_sentence
        return displayname
    @property
    def composed_sentence(self):
        "composes the relation as a sentence in a triple format."
        return u'%s %s %s %s %s %s' % (self.left_subject_scope, self.left_subject, self.relationtype_scope, self.relationtype, self.right_subject_scope, self.right_subject)

    @property
    def inversed_sentence(self):
        "composes the inverse relation as a sentence in a triple format."
        return u'%s %s %s %s %s' % (self.objectScope, self.right_subject, self.relationtype.inverse, self.left_subject_scope, self.left_subject )

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
            return u'%s %s %s' % (self.left_subject,self.relationtype,self.right_subject )

    @property
    def partial_composition(self):
        '''
        function that composes the right_subject and relation name, as in "x as a friend", "y as a sibling"
        '''
        return u'%s as a %s' % (self.right_subject, self.relationtype)


    # Save for Relation

    def save(self, *args, **kwargs):

        """
        left_subject and right_subject should be saved after creating the relation
        """
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Relation, self).save(*args, **kwargs) # Call the "real" save() method.
                left_subject = self.left_subject
                right_subject = self.right_subject
                left_subject.ref.save()
                right_subject.ref.save()
        super(Relation, self).save(*args, **kwargs) # Call the "real" save() method.


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
        displayname="AS: "+self.composed_attribution
        return displayname

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
        return u'%s %s has %s %s %s %s' % (self.subject_scope, self.subject, self.attributetype_scope, self.attributetype, self.value_scope, self.svalue)

    @property
    def composed_attribution(self):
        '''
        composes a name to the attribute
        '''
        return u'the %s of %s is %s' % (self.attributetype, self.subject, self.svalue)

    @property
    def partial_composition(self):
        '''
        function that composes the value and attribute name, as in "red as color", "4 as length"
        '''
        return u'%s as %s' % (self.svalue, self.attributetype)


    def subject_filter(self,attr):
        """
        returns applicable selection of nodes for selecting objects
        """
        for each in Objecttype.objects.all():
            if attr.subjecttype.id == each.id:
                return each.get_members

    # Save for Attribute

    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Attribute, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(Attribute, self).save(*args, **kwargs) # Call the "real" save() method.




class AttributeCharField(Attribute):

    value  = models.CharField(max_length=100, verbose_name='string')

    def __unicode__(self):
        displayname="ACF: "+ self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeCharField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeCharField, self).save(*args, **kwargs) # Call the "real" save() method.



class AttributeTextField(Attribute):

    value  = models.TextField(verbose_name='text')

    def __unicode__(self):
        displayname="ATF: "+ self.title
        return displayname

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeTextField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeTextField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeIntegerField(Attribute):
    value = models.IntegerField(max_length=100, verbose_name='Integer')

    def __unicode__(self):
        displayname="AIF: "+self.title
        return displayname

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.



class AttributeCommaSeparatedIntegerField(Attribute):

    value  = models.CommaSeparatedIntegerField(max_length=100, verbose_name='integers separated by comma')

    def __unicode__(self):
        displayname="ACSIF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeCommaSeparatedIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeCommaSeparatedIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.

class AttributeBigIntegerField(Attribute):

    value  = models.BigIntegerField(max_length=100, verbose_name='big integer')

    def __unicode__(self):
        displayname="ABIF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeBigIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeBigIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributePositiveIntegerField(Attribute):

    value  = models.PositiveIntegerField(max_length=100, verbose_name='positive integer')

    def __unicode__(self):
        displayname="APIF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributePositiveIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributePositiveIntegerField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeDecimalField(Attribute):

    value  = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='decimal')

    def __unicode__(self):
        displayname="ADF: "+self.title
        return displayname

    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeDecimalField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeDecimalField, self).save(*args, **kwargs) # Call the "real" save() method.

class AttributeFloatField(Attribute):

    value  = models.FloatField(max_length=100, verbose_name='number as float')

    def __unicode__(self):
        displayname="AFF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeFloatField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeFloatField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeBooleanField(Attribute):

    value  = models.BooleanField(verbose_name='boolean')

    def __unicode__(self):
        displayname="ABF: "+self.title
        return displayname
        
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeBooleanField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeBooleanField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeNullBooleanField(Attribute):

    value  = models.NullBooleanField(verbose_name='true false or unknown')

    def __unicode__(self):
        displayname="ANBF: "+self.title
        return displayname



    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeNullBooleanField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeNullBooleanField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeDateField(Attribute):

    value  = models.DateField(max_length=100, verbose_name='date')

    def __unicode__(self):
        displayname="ADF: "+self.title
        return displayname



    def save(self, *args, **kwargs):
        self.nodemodel=self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeDateField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeDateField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeDateTimeField(Attribute):

    value  = models.DateTimeField(max_length=100, verbose_name='date time')

    def __unicode__(self):
        displayname="ADTF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeDateTimeField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeDateTimeField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeTimeField(Attribute):

    value  = models.TimeField(max_length=100, verbose_name='time')

    def __unicode__(self):
        displayname="ATIF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeTimeField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeTimeField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeEmailField(Attribute):

    value  = models.EmailField(max_length=100,verbose_name='value')

    def __unicode__(self):
        displayname="AEF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel=self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeEmailField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeEmailField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeFileField(Attribute):

    value  = models.FileField(upload_to='media/'+UPLOAD_TO, verbose_name='file')

    def __unicode__(self):
        displayname="AFIF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeFileField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeFileField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeFilePathField(Attribute):

    value  = models.FilePathField(verbose_name='path of file')

    def __unicode__(self):
        displayname="AFPF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeFilePathField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeFilePathField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeImageField(Attribute):

    value  = models.ImageField(upload_to = UPLOAD_TO, verbose_name='image')

    def __unicode__(self):
        displayname="AIMF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeImageField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeImageField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeURLField(Attribute):

    value  = models.URLField(max_length=100, verbose_name='url')

    def __unicode__(self):
        displayname="AURLF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeURLField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeURLField, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeIPAddressField(Attribute):

    value  = models.IPAddressField(max_length=100, verbose_name='ip address')

    def __unicode__(self):
        displayname="AIPF: "+self.title
        return displayname


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeIPAddressField, self).save(*args, **kwargs) # Call the "real" save() method.
                subject=self.subject
                subject.ref.save()
        super(AttributeIPAddressField, self).save(*args, **kwargs) # Call the "real" save() method.



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
        displayname="PT: "+self.title
        return displayname


    class Meta:
        verbose_name = _('process type')
        verbose_name_plural = _('process types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )
    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        super(Processtype, self).save(*args, **kwargs) # Call the "real" save() method.
        self.nbhood=self.get_rendered_nbh
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Processtype, self).save(*args, **kwargs) # Call the "real" save() method.







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
    author_set = models.ManyToManyField(User, related_name="author_set_of", verbose_name='Possible authors in the system',
                                            blank=True, null=False)



    def __unicode__(self):
        displayname="ST: "+self.title
        return displayname


    class Meta:
        verbose_name = _('system type')
        verbose_name_plural = _('system types')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        super(Systemtype, self).save(*args, **kwargs) # Call the "real" save() method.
#        self.nbhood=self.get_rendered_nbh
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Systemtype, self).save(*args, **kwargs) # Call the "real" save() method.


class AttributeSpecification(Node):
    """
    specifying an attribute by a subject to say for example:
    population of India, color of a flower etc.  These do not yeild a
    proposition but a description, which can be used as a subject in
    another sentence.
    """
    attributetype = models.ForeignKey(Attributetype, verbose_name='property name')
    subjects = models.ManyToManyField(NID, related_name="subjects_attrspec_of", verbose_name='subjects')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_attspecns',
                                     blank=True, null=True)

    @property
    def composed_subject(self):
        '''
        composes a name to the attribute
        '''
        subjects = u''
        for each in self.subjects.all():
            subjects = subjects + each.title + ' '
        return u'the %s of %s' % (self.attributetype, subjects)


    def __unicode__(self):
        displayname="ASN: "+self.composed_subject
        return displayname



    class Meta:
        verbose_name = _('attribute specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(AttributeSpecification, self).save(*args, **kwargs) # Call the "real" save() method.

        super(AttributeSpecification, self).save(*args, **kwargs) # Call the "real" save() method.




class RelationSpecification(Node):
    """
    specifying a relation with a subject
    """
    relationtype = models.ForeignKey(Relationtype, verbose_name='relation name')
    subjects = models.ManyToManyField(NID, related_name="subjects_in_relspec", verbose_name='subjects')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_relnspecns',
                                     blank=True, null=True)


    @property
    def composed_subject(self):
        '''
        composing an expression with relation name and subject
        '''
        subjects = u''
        for each in self.subjects.all():
            subjects = subjects + each.title + ' '
        return u'the %s of %s' % (self.relationtype, subjects)

    def __unicode__(self):
        dispalyname="RSN: "+ self.composed_subject
        return displayname


    class Meta:
        verbose_name = _('relation specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(RelationSpecification, self).save(*args, **kwargs) # Call the "real" save() method.

        super(RelationSpecification, self).save(*args, **kwargs) # Call the "real" save() method.



class NodeSpecification(Node):
    """
    A node specified (described) by its relations or attributes or both.
    """
    subject = models.ForeignKey(Node, related_name="subject_nodespec", verbose_name='subject name')
    relations = models.ManyToManyField(Relation, related_name="relations_in_nodespec", verbose_name='relations used to specify the domain')
    attributes = models.ManyToManyField(Attribute, related_name="attributes_in_nodespec", verbose_name='attributes used to specify the domain')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_nodespecns',
                                     blank=True, null=True)


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
        return u'the %s with %s, %s' % (self.subject, self.relations, self.attributes)

    def __unicode__(self):
        displayname="NSN: "+ self.composed_subject
        return displayname

    class Meta:
        verbose_name = _('Node specification')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(NodeSpecification, self).save(*args, **kwargs) # Call the "real" save() method.

        super(NodeSpecification, self).save(*args, **kwargs) # Call the "real" save() method.




class Expression(Node):
    """
    Expression constructor
    """

    left_term = models.ForeignKey(NID, related_name="left_term_of", verbose_name='left term name')
    relationtype = models.ForeignKey(Relationtype, verbose_name='relation name')
    right_term = models.ForeignKey(NID, related_name="right_term_of", verbose_name='right term name')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_exprn',
                                     blank=True, null=True)


    def __unicode__(self):
        displayname="EXPN: "+self.composed_sentence
        return displayname

    @property
    def composed_sentence(self):
        "composes the relation as a sentence in a triple format."
        return u'%s %s %s' % (self.left_term, self.relationtype, self.right_term)


    class Meta:
        unique_together = (('left_term','relationtype','right_term'),)
        verbose_name = _('expression')
        verbose_name_plural = _('expressions')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Expression, self).save(*args, **kwargs) # Call the "real" save() method.

        super(Expression, self).save(*args, **kwargs) # Call the "real" save() method.




class Union(Node):
    """
    union of two classes
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'union_of', verbose_name='node types for union')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_unions',
                                     blank=True, null=True)


    def __unicode__(self):
        displayname="UN: "+ self.title
        return displayname
    
    @property
    def composed_sentence(self):
        "composes the relation as a sentence in a triple format."
        return u'%s %s' % (self.nodetypes, self.metatypes)

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Union, self).save(*args, **kwargs) # Call the "real" save() method.

        super(Union, self).save(*args, **kwargs) # Call the "real" save() method.




class Complement(Node):
    """
    complement of a  class
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'complement_of', verbose_name='complementary nodes')
    metatypes=models.ManyToManyField(Metatype,related_name='meta_complement',verbose_name=_('Metanodes'),
                                     blank=True, null= True)
    
    @property
    def composed_subject(self):
        return u'Not of %s' % (self.nodetypes)

    # @property
    # def composed_sentence(self):
    #     "composes the complement as a sentence. "
    #     return u'Not of %s %s' % (self.nodetypes,self.metatypes)
    
    def __unicode__(self):
        displayname="CMP: "+self.title
        return displayname

    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Complement, self).save(*args, **kwargs) # Call the "real" save() method.

        super(Complement, self).save(*args, **kwargs) # Call the "real" save() method.


class Intersection(Node):
    """
    Intersection of classes
    """
    nodetypes = models.ManyToManyField(Nodetype, related_name = 'intersection_of', verbose_name='intersection of classes')
    metatypes=models.ManyToManyField(Metatype,verbose_name=_('member of metatypes'),
                                     related_name='member_intersectn',
                                     blank=True, null=True)


    def __unicode__(self):
        displayname="INTSN: "+self.title
        return displayname
    @property
    def composed_subject(self):
        return u'And of %s' % (self.nodetypes)


    # @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.nodemodel = self.__class__.__name__
        self.nbhood=[]
        if GSTUDIO_VERSIONING:
            with reversion.create_revision():
                super(Intersection, self).save(*args, **kwargs) # Call the "real" save() method.

        super(Intersection, self).save(*args, **kwargs) # Call the "real" save() method.


if GSTUDIO_VERSIONING == True:
    reversion.register(NID)

    if not reversion.is_registered(Systemtype):
        reversion.register(Systemtype,follow=["nodetype_ptr"] )

    if not reversion.is_registered(Objecttype):
        reversion.register(Objecttype , follow=["nodetype_ptr"])

    if not reversion.is_registered(Node):
        reversion.register(Node , follow=["nid_ptr"])

    if not reversion.is_registered(Edge):
        reversion.register(Edge , follow=["nid_ptr"])


    if not reversion.is_registered(Processtype):
        reversion.register(Processtype, follow=["nodetype_ptr","changing_attributetype_set", "changing_relationtype_set"])

    if not reversion.is_registered(Nodetype):
        reversion.register(Nodetype, follow=["node_ptr","parent", "metatypes","prior_nodes", "posterior_nodes"])

    if not reversion.is_registered(Metatype):
        reversion.register(Metatype, follow=["node_ptr","parent"])


    if not reversion.is_registered(Relationtype):
        reversion.register(Relationtype, follow=["nodetype_ptr","left_subjecttype", "right_subjecttype"])

    if not reversion.is_registered(Attributetype):
        reversion.register(Attributetype, follow=["nodetype_ptr","subjecttype"])

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
