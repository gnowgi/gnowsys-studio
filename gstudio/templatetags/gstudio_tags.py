
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


"""Template tags and filters for Gstudio"""
from hashlib import md5
from random import sample
from urllib import urlencode
from datetime import datetime

from django.db.models import Q
from django.db import connection
from django.template import Node as nd
from django.template import Library
from django.template import TemplateSyntaxError
from django.contrib.comments.models import CommentFlag
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.contrib.comments import get_model as get_comment_model

from tagging.models import Tag
from tagging.utils import calculate_cloud

from gstudio.models import Nodetype
from gstudio.models import Author
from gstudio.models import Metatype

from gstudio.gnowql import get_node

from gstudio.managers import tags_published
from gstudio.comparison import VectorBuilder
from gstudio.comparison import pearson_score
from gstudio.templatetags.zcalendar import GstudioCalendar
from gstudio.templatetags.zbreadcrumbs import retrieve_breadcrumbs
from django.http import HttpResponseRedirect

from gstudio.CNL import *
from gstudio.methods import check_release_or_not
import os
from settings import STATIC_URL
from gstudio.methods import *
register = Library()

VECTORS = None
VECTORS_FACTORY = lambda: VectorBuilder(Nodetype.published.all(),
                                        ['title', 'excerpt', 'content'])
CACHE_NODETYPES_RELATED = {}





@register.inclusion_tag('gstudio/tags/dummy.html')
def get_metatypes(template='gstudio/tags/metatypes.html'):
    """Return the metatypes"""
    return {'template': template,
            'metatypes': Metatype.tree.all()}

#@register.inclusion_tag('gstudio/tags/dummy.html')
#def get_subtypes(template='gstudio/tags/nodetypes.html'):
#    """Return the subtypes"""
#    return {'template': template,
#            'subtypes': Nodetype.tree.all()}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_authors(number=5, template='gstudio/tags/authors.html'):
    """Return the published authors"""
    return {'template': template,
            'authors': Author.published.all()[:number]}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_recent_nodetypes(number=5, template='gstudio/tags/recent_nodetypes.html'):
    """Return the most recent nodetypes"""
    return {'template': template,
            'nodetypes': Nodetype.published.all()[:number]}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_featured_nodetypes(number=5,
                         template='gstudio/tags/featured_nodetypes.html'):
    """Return the featured nodetypes"""
    return {'template': template,
            'nodetypes': Nodetype.published.filter(featured=True)[:number]}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_random_nodetypes(number=5, template='gstudio/tags/random_nodetypes.html'):
    """Return random nodetypes"""
    nodetypes = Nodetype.published.all()
    if number > len(nodetypes):
        number = len(nodetypes)
    return {'template': template,
            'nodetypes': sample(nodetypes, number)}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_popular_nodetypes(number=5, template='gstudio/tags/popular_nodetypes.html'):
    """Return popular  nodetypes"""
    ctype = ContentType.objects.get_for_model(Nodetype)
    query = """SELECT object_pk, COUNT(*) AS score
    FROM %s
    WHERE content_type_id = %%s
    AND is_public = '1'
    GROUP BY object_pk
    ORDER BY score DESC""" % get_comment_model()._meta.db_table

    cursor = connection.cursor()
    cursor.execute(query, [ctype.id])
    object_ids = [int(row[0]) for row in cursor.fetchall()]

    # Use ``in_bulk`` here instead of an ``id__in`` filter, because ``id__in``
    # would clobber the ordering.
    object_dict = Nodetype.published.in_bulk(object_ids)

    return {'template': template,
            'nodetypes': [object_dict[object_id]
                        for object_id in object_ids
                        if object_id in object_dict][:number]}


@register.inclusion_tag('gstudio/tags/dummy.html', takes_context=True)
def get_similar_nodetypes(context, number=5,
                        template='gstudio/tags/similar_nodetypes.html',
                        flush=False):
    """Return similar nodetypes"""
    global VECTORS
    global CACHE_NODETYPES_RELATED

    if VECTORS is None or flush:
        VECTORS = VECTORS_FACTORY()
        CACHE_NODETYPES_RELATED = {}

    def compute_related(object_id, dataset):
        """Compute related nodetypes to a nodetype with a dataset"""
        object_vector = None
        for nodetype, e_vector in dataset.items():
            if nodetype.pk == object_id:
                object_vector = e_vector

        if not object_vector:
            return []

        nodetype_related = {}
        for nodetype, e_vector in dataset.items():
            if nodetype.pk != object_id:
                score = pearson_score(object_vector, e_vector)
                if score:
                    nodetype_related[nodetype] = score

        related = sorted(nodetype_related.items(), key=lambda(k, v): (v, k))
        return [rel[0] for rel in related]

    object_id = context['object'].pk
    columns, dataset = VECTORS()
    key = '%s-%s' % (object_id, VECTORS.key)
    if not key in CACHE_NODETYPES_RELATED.keys():
        CACHE_NODETYPES_RELATED[key] = compute_related(object_id, dataset)

    nodetypes = CACHE_NODETYPES_RELATED[key][:number]
    return {'template': template,
            'nodetypes': nodetypes}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_archives_nodetypes(template='gstudio/tags/archives_nodetypes.html'):
    """Return archives nodetypes"""
    return {'template': template,
            'archives': Nodetype.published.dates('creation_date', 'month',
                                              order='DESC')}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_archives_nodetypes_tree(
    template='gstudio/tags/archives_nodetypes_tree.html'):
    """Return archives nodetypes as a Tree"""
    return {'template': template,
            'archives': Nodetype.published.dates('creation_date', 'day',
                                              order='ASC')}


@register.inclusion_tag('gstudio/tags/dummy.html', takes_context=True)
def get_calendar_nodetypes(context, year=None, month=None,
                         template='gstudio/tags/calendar.html'):
    """Return an HTML calendar of nodetypes"""
    if not year or not month:
        date_month = context.get('month') or context.get('day') or \
                     getattr(context.get('object'), 'creation_date', None) or \
                     datetime.today()
        year, month = date_month.timetuple()[:2]

    calendar = GstudioCalendar()
    current_month = datetime(year, month, 1)

    dates = list(Nodetype.published.dates('creation_date', 'month'))

    if not current_month in dates:
        dates.append(current_month)
        dates.sort()
    index = dates.index(current_month)

    previous_month = index > 0 and dates[index - 1] or None
    next_month = index != len(dates) - 1 and dates[index + 1] or None

    return {'template': template,
            'next_month': next_month,
            'previous_month': previous_month,
            'calendar': calendar.formatmonth(year, month)}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_recent_comments(number=5, template='gstudio/tags/recent_comments.html'):
    """Return the most recent comments"""
    # Using map(smart_unicode... fix bug related to issue #8554
    #Modified comments to include CNL
    nodetype_published_pks = map(smart_unicode,
                              Nodetype.published.values_list('id', flat=True))
    content_type = ContentType.objects.get_for_model(Nodetype)

    comments = get_comment_model().objects.filter(
        Q(flags=None) | Q(flags__flag=CommentFlag.MODERATOR_APPROVAL),
        content_type=content_type, object_pk__in=nodetype_published_pks,
        is_public=True).order_by('-submit_date')[:number]
 

    return {'template': template,
            'comments': comments}


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_recent_oldcomments(number=5, template='gstudio/tags/recent_comments.html'):
    """Return the most recent comments"""
    # Using map(smart_unicode... fix bug related to issue #8554
    nodetype_published_pks = map(smart_unicode,
                              Nodetype.published.values_list('id', flat=True))
    content_type = ContentType.objects.get_for_model(Nodetype)

    comments = get_comment_model().objects.filter(
        Q(flags=None) | Q(flags__flag=CommentFlag.MODERATOR_APPROVAL),
        content_type=content_type, object_pk__in=nodetype_published_pks,
        is_public=True).order_by('-submit_date')[:number]

    return {'template': template,
            'comments': comments}

@register.inclusion_tag('gstudio/tags/dummy.html')
def get_recent_linkbacks(number=5,
                         template='gstudio/tags/recent_linkbacks.html'):
    """Return the most recent linkbacks"""
    nodetype_published_pks = map(smart_unicode,
                              Nodetype.published.values_list('id', flat=True))
    content_type = ContentType.objects.get_for_model(Nodetype)

    linkbacks = get_comment_model().objects.filter(
        content_type=content_type,
        object_pk__in=nodetype_published_pks,
        flags__flag__in=['pingback', 'trackback'],
        is_public=True).order_by(
        '-submit_date')[:number]

    return {'template': template,
            'linkbacks': linkbacks}


@register.inclusion_tag('gstudio/tags/dummy.html', takes_context=True)
def gstudio_pagination(context, page, begin_pages=3, end_pages=3,
                      before_pages=2, after_pages=2,
                      template='gstudio/tags/pagination.html'):
    """Return a Digg-like pagination, by splitting long list of page
    into 3 blocks of pages"""
    GET_string = ''
    for key, value in context['request'].GET.items():
        if key != 'page':
            GET_string += '&%s=%s' % (key, value)

    begin = page.paginator.page_range[:begin_pages]
    end = page.paginator.page_range[-end_pages:]
    middle = page.paginator.page_range[max(page.number - before_pages - 1, 0):
                                       page.number + after_pages]

    if set(begin) & set(end):  # [1, 2, 3], [...], [2, 3, 4]
        begin = sorted(set(begin + end))  # [1, 2, 3, 4]
        middle, end = [], []
    elif begin[-1] + 1 == end[0]:  # [1, 2, 3], [...], [4, 5, 6]
        begin += end  # [1, 2, 3, 4, 5, 6]
        middle, end = [], []
    elif set(begin) & set(middle):  # [1, 2, 3], [2, 3, 4], [...]
        begin = sorted(set(begin + middle))  # [1, 2, 3, 4]
        middle = []
    elif begin[-1] + 1 == middle[0]:  # [1, 2, 3], [4, 5, 6], [...]
        begin += middle  # [1, 2, 3, 4, 5, 6]
        middle = []
    elif middle[-1] + 1 == end[0]:  # [...], [15, 16, 17], [18, 19, 20]
        end = middle + end  # [15, 16, 17, 18, 19, 20]
        middle = []
    elif set(middle) & set(end):  # [...], [17, 18, 19], [18, 19, 20]
        end = sorted(set(middle + end))  # [17, 18, 19, 20]
        middle = []

    return {'template': template, 'page': page, 'GET_string': GET_string,
            'begin': begin, 'middle': middle, 'end': end}


@register.inclusion_tag('gstudio/tags/dummy.html', takes_context=True)
def gstudio_breadcrumbs(context, separator='/', root_name='Nodetype',
                       template='gstudio/tags/breadcrumbs.html',):
    """Return a breadcrumb for the application"""
    path = context['request'].path
    page_object = context.get('object') or context.get('metatype') or \
                  context.get('tag') or context.get('author')
    breadcrumbs = retrieve_breadcrumbs(path, page_object, root_name)

    return {'template': template,
            'separator': separator,
            'breadcrumbs': breadcrumbs}

@register.simple_tag
def get_gravatar(email, size=80, rating='g', default=None):
    """Return url for a Gravatar"""
    url = 'http://www.gravatar.com/avatar/%s.jpg' % \
          md5(email.strip().lower()).hexdigest()
    options = {'s': size, 'r': rating}
    if default:
        options['d'] = default

    url = '%s?%s' % (url, urlencode(options))
    return url.replace('&', '&amp;')

@register.simple_tag
def get_type(name):

    """Return the type of node"""
    return get_node(name)


class TagsNode(nd):
    def __init__(self, context_var):
        self.context_var = context_var
    def render(self, context):
        context[self.context_var] = tags_published()
        return ''
#define get_CNL function
@register.assignment_tag
def get_CNL(no, takes_context = True):
       
    l = get_CNL_list(no)
    return l
 
@register.tag
def get_tags(parser, token):
    """{% get_tags as var %}"""
    bits = token.split_contents()

    if len(bits) != 3:
        raise TemplateSyntaxError(
            'get_tags tag takes exactly two arguments')
    if bits[1] != 'as':
        raise TemplateSyntaxError(
            "first argument to get_tags tag must be 'as'")
    return TagsNode(bits[2])

@register.simple_tag
def redirect(username):
 link = "/"
 return HttpResponseRedirect(link)
 


@register.inclusion_tag('gstudio/tags/dummy.html')
def get_tag_cloud(steps=6, template='gstudio/tags/tag_cloud.html'):
    """Return a cloud of published tags"""
    tags = Tag.objects.usage_for_queryset(
        Nodetype.published.all(), counts=True)
    return {'template': template,
            'tags': calculate_cloud(tags, steps)}

@register.inclusion_tag('gstudio/tags/comment.html')
def show_comment(comment,idusr,flag,admin_id,attob):
  return {'comment':comment , 'idusr' : idusr, "flag" : flag, "admin_id" : admin_id , "attribute" : attob}

@register.inclusion_tag('gstudio/tags/commentpage.html')
def show_commentpage(comment,idusr,flag,admin_id,attob):
  return {'comment':comment , 'idusr' : idusr, "flag" : flag, "admin_id" : admin_id , "attribute" : attob}


@register.simple_tag
def show_nodesystem(object_id):
    search=object_id    
    nbh=""
    url=""
    for each in System.objects.all():
        sysid=each.id
        for eachsys in each.systemtypes.all():
            if eachsys.title=="Meeting":
                url="group/gnowsys-grp/"
		objecttitle = "TWIST"
            elif eachsys.title=="Wikipage":
                url="page/gnowsys-page/"
		objecttitle = "WIKIPAGE"
        for eachob in each.system_set.all():
            if eachob.gbobject_set.all():
                for eachgbob in eachob.gbobject_set.all():
                    if search==eachgbob.id:
                        nbh=url+str(sysid)
            	
        if search==sysid:
            nbh=url+str(sysid)
    		   
    return nbh

@register.assignment_tag
def check_release(meeting):
  var = check_release_or_not(meeting)
  return var

@register.assignment_tag
def check_subscribe(meeting,user):
  var = check_subscribe_or_not(meeting,user)
  return var

@register.assignment_tag
def check_user_admin(userid):
  var=check_usr_admin(userid)
  return var


@register.assignment_tag
def get_static_url():
   var = os.path.join(os.path.dirname(__file__),STATIC_URL)
   return var

@register.assignment_tag
def get_factory_looms():
   fs = []
   fs = get_factory_loom_OTs()
   return fs

@register.assignment_tag
def put_home_content():
   var = get_home_content()
   return var

@register.assignment_tag
def put_more_content():
   var = get_more_content()
   return var

@register.assignment_tag
def put_home_title():
   var = get_home_title()
   return var

@register.inclusion_tag('gstudio/addreln.html')
def add_res_relation(meetingob):
  template='gstudio/addreln.html'
 
  return {'template':template,'meetingob':meetingob}

@register.simple_tag
def get_available_rts():
    listrts=[]
    for each in Relationtype.objects.all():
        s=each.title
        listrts.append(str(s))
    return str(listrts)

@register.simple_tag
def get_available_objects():
    listsubjs=[]
    for each in Gbobject.objects.all():
        s=each.title
        listsubjs.append(each.__str__())
    return str(listsubjs)


@register.inclusion_tag('gstudio/edittitle.html')
def edit_title(objectid,objecttitle):
  template='gstudio/edititle.html'
  return {'template':template,'objectid':objectid,'objecttitle':objecttitle}

@register.simple_tag
def get_add_tag():
    listtag = []
    tag = Tag.objects.all()
    for each in tag:
	listtag.append(each.__str__())	
    return str(listtag)

@register.simple_tag
def get_page_drawer():
    pagedrawer = []
    #wikiset = Systemtype.objects.all()
    drawerset = Systemtype.objects.get(title="Wikipage")
    drawer= drawerset.member_systems.all()
    for each in drawer:
	pagedrawer.append(each.__str__())
    return str(pagedrawer)


@register.inclusion_tag('gstudio/priorpost.html')
def addpriorpost(objectid,user):
  template='gstudio/priorpost.html'
  gbobject = Gbobject.objects.get(id=objectid)
  priorgbobject = gbobject.prior_nodes.all()
  posteriorgbobject = gbobject.posterior_nodes.all()
  return {'template':template,'objectid':objectid,'priorgbobject':priorgbobject,'posteriorgbobject':posteriorgbobject,'user':user}

@register.inclusion_tag('gstudio/addingtag.html')
def addtag(viewtag,objectid,user):
  template='gstudio/addingtag.html'
  return {'viewtag':viewtag,'objectid':objectid,'user':user}

@register.simple_tag
def get_pri_post_page():
    listobject = []
    gbobject = Gbobject.objects.all()
    for each in gbobject:
        listobject.append(each.__str__())
    return str(listobject)
