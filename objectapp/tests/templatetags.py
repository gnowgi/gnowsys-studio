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


"""Test cases for Objectapp's templatetags"""
from datetime import datetime

from django.test import TestCase
from django.template import Context
from django.template import Template
from django.template import TemplateSyntaxError
from django.contrib import comments
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.models import CommentFlag

from tagging.models import Tag

from objectapp.models import Gbobject
from objectapp.models import Author
from objectapp.models import Objecttype
from objectapp.managers import DRAFT
from objectapp.managers import PUBLISHED
from objectapp.templatetags.objectapp_tags import get_authors
from objectapp.templatetags.objectapp_tags import get_gravatar
from objectapp.templatetags.objectapp_tags import get_tag_cloud
from objectapp.templatetags.objectapp_tags import get_objecttypes
from objectapp.templatetags.objectapp_tags import objectapp_pagination
from objectapp.templatetags.objectapp_tags import get_recent_gbobjects
from objectapp.templatetags.objectapp_tags import get_random_gbobjects
from objectapp.templatetags.objectapp_tags import objectapp_breadcrumbs
from objectapp.templatetags.objectapp_tags import get_popular_gbobjects
from objectapp.templatetags.objectapp_tags import get_similar_gbobjects
from objectapp.templatetags.objectapp_tags import get_recent_comments
from objectapp.templatetags.objectapp_tags import get_recent_linkbacks
from objectapp.templatetags.objectapp_tags import get_calendar_gbobjects
from objectapp.templatetags.objectapp_tags import get_archives_gbobjects
from objectapp.templatetags.objectapp_tags import get_featured_gbobjects
from objectapp.templatetags.objectapp_tags import get_archives_gbobjects_tree


class TemplateTagsTestCase(TestCase):
    """Test cases for Template tags"""

    def setUp(self):
        params = {'title': 'My gbobject',
                  'content': 'My content',
                  'tags': 'objectapp, test',
                  'creation_date': datetime(2010, 1, 1),
                  'slug': 'my-gbobject'}
        self.gbobject = Gbobject.objects.create(**params)

    def publish_gbobject(self):
        self.gbobject.status = PUBLISHED
        self.gbobject.featured = True
        self.gbobject.sites.add(Site.objects.get_current())
        self.gbobject.save()

    def test_get_objecttypes(self):
        context = get_objecttypes()
        self.assertEquals(len(context['objecttypes']), 0)
        self.assertEquals(context['template'], 'objectapp/tags/objecttypes.html')

        Objecttype.objects.create(title='Objecttype 1', slug='Objecttype-1')
        context = get_objecttypes('custom_template.html')
        self.assertEquals(len(context['objecttypes']), 1)
        self.assertEquals(context['template'], 'custom_template.html')

    def test_get_authors(self):
        context = get_authors()
        self.assertEquals(len(context['authors']), 0)
        self.assertEquals(context['template'], 'objectapp/tags/authors.html')

        user = User.objects.create_user(username='webmaster',
                                        email='webmaster@example.com')
        self.gbobject.authors.add(user)
        self.publish_gbobject()
        context = get_authors('custom_template.html')
        self.assertEquals(len(context['authors']), 1)
        self.assertEquals(context['template'], 'custom_template.html')

    def test_get_recent_gbobjects(self):
        context = get_recent_gbobjects()
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/recent_gbobjects.html')

        self.publish_gbobject()
        context = get_recent_gbobjects(3, 'custom_template.html')
        self.assertEquals(len(context['gbobjects']), 1)
        self.assertEquals(context['template'], 'custom_template.html')
        context = get_recent_gbobjects(0)
        self.assertEquals(len(context['gbobjects']), 0)

    def test_get_featured_gbobjects(self):
        context = get_featured_gbobjects()
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/featured_gbobjects.html')

        self.publish_gbobject()
        context = get_featured_gbobjects(3, 'custom_template.html')
        self.assertEquals(len(context['gbobjects']), 1)
        self.assertEquals(context['template'], 'custom_template.html')
        context = get_featured_gbobjects(0)
        self.assertEquals(len(context['gbobjects']), 0)

    def test_get_random_gbobjects(self):
        context = get_random_gbobjects()
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/random_gbobjects.html')

        self.publish_gbobject()
        context = get_random_gbobjects(3, 'custom_template.html')
        self.assertEquals(len(context['gbobjects']), 1)
        self.assertEquals(context['template'], 'custom_template.html')
        context = get_random_gbobjects(0)
        self.assertEquals(len(context['gbobjects']), 0)

    def test_get_popular_gbobjects(self):
        context = get_popular_gbobjects()
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/popular_gbobjects.html')

        self.publish_gbobject()
        context = get_popular_gbobjects(3, 'custom_template.html')
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'], 'custom_template.html')

        params = {'title': 'My second gbobject',
                  'content': 'My second content',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'slug': 'my-second-gbobject'}
        site = Site.objects.get_current()
        second_gbobject = Gbobject.objects.create(**params)
        second_gbobject.sites.add(site)

        comments.get_model().objects.create(comment='My Comment 1', site=site,
                                            content_object=self.gbobject)
        comments.get_model().objects.create(comment='My Comment 2', site=site,
                                            content_object=self.gbobject)
        comments.get_model().objects.create(comment='My Comment 3', site=site,
                                            content_object=second_gbobject)
        context = get_popular_gbobjects(3)
        self.assertEquals(context['gbobjects'], [self.gbobject, second_gbobject])
        self.gbobject.status = DRAFT
        self.gbobject.save()
        context = get_popular_gbobjects(3)
        self.assertEquals(context['gbobjects'], [second_gbobject])

    def test_get_similar_gbobjects(self):
        self.publish_gbobject()
        source_context = Context({'object': self.gbobject})
        context = get_similar_gbobjects(source_context)
        self.assertEquals(len(context['gbobjects']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/similar_gbobjects.html')

        params = {'title': 'My second gbobject',
                  'content': 'This is the second gbobject of my tests.',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'slug': 'my-second-gbobject'}
        site = Site.objects.get_current()
        second_gbobject = Gbobject.objects.create(**params)
        second_gbobject.sites.add(site)

        source_context = Context({'object': second_gbobject})
        context = get_similar_gbobjects(source_context, 3,
                                      'custom_template.html',
                                      flush=True)
        self.assertEquals(len(context['gbobjects']), 1)
        self.assertEquals(context['template'], 'custom_template.html')

    def test_get_archives_gbobjects(self):
        context = get_archives_gbobjects()
        self.assertEquals(len(context['archives']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/archives_gbobjects.html')

        self.publish_gbobject()
        params = {'title': 'My second gbobject',
                  'content': 'My second content',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'creation_date': datetime(2009, 1, 1),
                  'slug': 'my-second-gbobject'}
        site = Site.objects.get_current()
        second_gbobject = Gbobject.objects.create(**params)
        second_gbobject.sites.add(site)

        context = get_archives_gbobjects('custom_template.html')
        self.assertEquals(len(context['archives']), 2)
        self.assertEquals(context['archives'][0], datetime(2010, 1, 1))
        self.assertEquals(context['archives'][1], datetime(2009, 1, 1))
        self.assertEquals(context['template'], 'custom_template.html')

    def test_get_archives_tree(self):
        context = get_archives_gbobjects_tree()
        self.assertEquals(len(context['archives']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/archives_gbobjects_tree.html')

        self.publish_gbobject()
        params = {'title': 'My second gbobject',
                  'content': 'My second content',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'creation_date': datetime(2009, 1, 10),
                  'slug': 'my-second-gbobject'}
        site = Site.objects.get_current()
        second_gbobject = Gbobject.objects.create(**params)
        second_gbobject.sites.add(site)

        context = get_archives_gbobjects_tree('custom_template.html')
        self.assertEquals(len(context['archives']), 2)
        self.assertEquals(context['archives'][0], datetime(2009, 1, 10))
        self.assertEquals(context['archives'][1], datetime(2010, 1, 1))
        self.assertEquals(context['template'], 'custom_template.html')

    def test_get_calendar_gbobjects(self):
        source_context = Context()
        context = get_calendar_gbobjects(source_context)
        self.assertEquals(context['previous_month'], None)
        self.assertEquals(context['next_month'], None)
        self.assertEquals(context['template'], 'objectapp/tags/calendar.html')

        self.publish_gbobject()
        context = get_calendar_gbobjects(source_context,
                                       template='custom_template.html')
        self.assertEquals(context['previous_month'], datetime(2010, 1, 1))
        self.assertEquals(context['next_month'], None)
        self.assertEquals(context['template'], 'custom_template.html')

        context = get_calendar_gbobjects(source_context, 2009, 1)
        self.assertEquals(context['previous_month'], None)
        self.assertEquals(context['next_month'], datetime(2010, 1, 1))

        source_context = Context({'month': datetime(2009, 1, 1)})
        context = get_calendar_gbobjects(source_context)
        self.assertEquals(context['previous_month'], None)
        self.assertEquals(context['next_month'], datetime(2010, 1, 1))

        source_context = Context({'month': datetime(2010, 1, 1)})
        context = get_calendar_gbobjects(source_context)
        self.assertEquals(context['previous_month'], None)
        self.assertEquals(context['next_month'], None)

        params = {'title': 'My second gbobject',
                  'content': 'My second content',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'creation_date': datetime(2008, 1, 1),
                  'slug': 'my-second-gbobject'}
        site = Site.objects.get_current()
        second_gbobject = Gbobject.objects.create(**params)
        second_gbobject.sites.add(site)

        source_context = Context()
        context = get_calendar_gbobjects(source_context, 2009, 1)
        self.assertEquals(context['previous_month'], datetime(2008, 1, 1))
        self.assertEquals(context['next_month'], datetime(2010, 1, 1))
        context = get_calendar_gbobjects(source_context)
        self.assertEquals(context['previous_month'], datetime(2010, 1, 1))
        self.assertEquals(context['next_month'], None)

    def test_get_recent_comments(self):
        site = Site.objects.get_current()
        context = get_recent_comments()
        self.assertEquals(len(context['comments']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/recent_comments.html')

        comment_1 = comments.get_model().objects.create(
            comment='My Comment 1', site=site,
            content_object=self.gbobject)
        context = get_recent_comments(3, 'custom_template.html')
        self.assertEquals(len(context['comments']), 0)
        self.assertEquals(context['template'], 'custom_template.html')

        self.publish_gbobject()
        context = get_recent_comments()
        self.assertEquals(len(context['comments']), 1)

        author = User.objects.create_user(username='webmaster',
                                          email='webmaster@example.com')
        comment_2 = comments.get_model().objects.create(
            comment='My Comment 2', site=site,
            content_object=self.gbobject)
        comment_2.flags.create(user=author,
                               flag=CommentFlag.MODERATOR_APPROVAL)
        context = get_recent_comments()
        self.assertEquals(list(context['comments']), [comment_2, comment_1])

    def test_get_recent_linkbacks(self):
        user = User.objects.create_user(username='webmaster',
                                        email='webmaster@example.com')
        site = Site.objects.get_current()
        context = get_recent_linkbacks()
        self.assertEquals(len(context['linkbacks']), 0)
        self.assertEquals(context['template'],
                          'objectapp/tags/recent_linkbacks.html')

        linkback_1 = comments.get_model().objects.create(
            comment='My Linkback 1', site=site,
            content_object=self.gbobject)
        linkback_1.flags.create(user=user, flag='pingback')
        context = get_recent_linkbacks(3, 'custom_template.html')
        self.assertEquals(len(context['linkbacks']), 0)
        self.assertEquals(context['template'], 'custom_template.html')

        self.publish_gbobject()
        context = get_recent_linkbacks()
        self.assertEquals(len(context['linkbacks']), 1)

        linkback_2 = comments.get_model().objects.create(
            comment='My Linkback 2', site=site,
            content_object=self.gbobject)
        linkback_2.flags.create(user=user, flag='trackback')
        context = get_recent_linkbacks()
        self.assertEquals(list(context['linkbacks']), [linkback_2, linkback_1])

    def test_objectapp_pagination(self):
        class FakeRequest(object):
            def __init__(self, get_dict):
                self.GET = get_dict

        source_context = Context({'request': FakeRequest(
            {'page': '1', 'key': 'val'})})
        paginator = Paginator(range(200), 10)

        context = objectapp_pagination(source_context, paginator.page(1))
        self.assertEquals(context['page'].number, 1)
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [18, 19, 20])
        self.assertEquals(context['GET_string'], '&key=val')
        self.assertEquals(context['template'], 'objectapp/tags/pagination.html')

        source_context = Context({'request': FakeRequest({})})
        context = objectapp_pagination(source_context, paginator.page(2))
        self.assertEquals(context['page'].number, 2)
        self.assertEquals(context['begin'], [1, 2, 3, 4])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [18, 19, 20])
        self.assertEquals(context['GET_string'], '')

        context = objectapp_pagination(source_context, paginator.page(3))
        self.assertEquals(context['begin'], [1, 2, 3, 4, 5])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(6))
        self.assertEquals(context['begin'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(11))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [9, 10, 11, 12, 13])
        self.assertEquals(context['end'], [18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(15))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [13, 14, 15, 16, 17, 18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(18))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [16, 17, 18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(19))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [17, 18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(20))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [18, 19, 20])

        context = objectapp_pagination(source_context, paginator.page(10),
                                    begin_pages=1, end_pages=3,
                                    before_pages=4, after_pages=3,
                                    template='custom_template.html')
        self.assertEquals(context['begin'], [1])
        self.assertEquals(context['middle'], [6, 7, 8, 9, 10, 11, 12, 13])
        self.assertEquals(context['end'], [18, 19, 20])
        self.assertEquals(context['template'], 'custom_template.html')

        paginator = Paginator(range(50), 10)
        context = objectapp_pagination(source_context, paginator.page(1))
        self.assertEquals(context['begin'], [1, 2, 3, 4, 5])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [])

        paginator = Paginator(range(60), 10)
        context = objectapp_pagination(source_context, paginator.page(1))
        self.assertEquals(context['begin'], [1, 2, 3, 4, 5, 6])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [])

        paginator = Paginator(range(70), 10)
        context = objectapp_pagination(source_context, paginator.page(1))
        self.assertEquals(context['begin'], [1, 2, 3])
        self.assertEquals(context['middle'], [])
        self.assertEquals(context['end'], [5, 6, 7])

    def test_objectapp_breadcrumbs(self):
        class FakeRequest(object):
            def __init__(self, path):
                self.path = path

        source_context = Context({'request': FakeRequest('/')})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 1)
        self.assertEquals(context['breadcrumbs'][0].name, 'Blog')
        self.assertEquals(context['breadcrumbs'][0].url,
                          reverse('objectapp_gbobject_archive_index'))
        self.assertEquals(context['separator'], '/')
        self.assertEquals(context['template'], 'objectapp/tags/breadcrumbs.html')

        context = objectapp_breadcrumbs(source_context,
                                     '>', 'Weblog', 'custom_template.html')
        self.assertEquals(len(context['breadcrumbs']), 1)
        self.assertEquals(context['breadcrumbs'][0].name, 'Weblog')
        self.assertEquals(context['separator'], '>')
        self.assertEquals(context['template'], 'custom_template.html')

        source_context = Context(
            {'request': FakeRequest(self.gbobject.get_absolute_url()),
             'object': self.gbobject})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 5)

        cat_1 = Objecttype.objects.create(title='Objecttype 1', slug='Objecttype-1')
        source_context = Context(
            {'request': FakeRequest(cat_1.get_absolute_url()),
             'object': cat_1})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 3)
        cat_2 = Objecttype.objects.create(title='Objecttype 2', slug='Objecttype-2',
                                        parent=cat_1)
        source_context = Context(
            {'request': FakeRequest(cat_2.get_absolute_url()),
             'object': cat_2})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 4)

        tag = Tag.objects.get(name='test')
        source_context = Context(
            {'request': FakeRequest(reverse('objectapp_tag_detail',
                                            args=['test'])),
             'object': tag})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 3)

        User.objects.create_user(username='webmaster',
                                 email='webmaster@example.com')
        author = Author.objects.get(username='webmaster')
        source_context = Context(
            {'request': FakeRequest(author.get_absolute_url()),
             'object': author})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 3)

        source_context = Context(
            {'request': FakeRequest(reverse(
                'objectapp_gbobject_archive_year', args=[2011]))})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 2)

        source_context = Context({'request': FakeRequest(reverse(
            'objectapp_gbobject_archive_month', args=[2011, '03']))})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 3)

        source_context = Context({'request': FakeRequest(reverse(
            'objectapp_gbobject_archive_day', args=[2011, '03', 15]))})
        context = objectapp_breadcrumbs(source_context)
        self.assertEquals(len(context['breadcrumbs']), 4)
        # More tests can be done here, for testing path and objects in context

    def test_get_gravatar(self):
        self.assertEquals(
            get_gravatar('webmaster@example.com'),
            'http://www.gravatar.com/avatar/86d4fd4a22de452'
            'a9228298731a0b592.jpg?s=80&amp;r=g')
        self.assertEquals(
            get_gravatar('  WEBMASTER@example.com  ', 15, 'x', '404'),
            'http://www.gravatar.com/avatar/86d4fd4a22de452'
            'a9228298731a0b592.jpg?s=15&amp;r=x&amp;d=404')

    def test_get_tags(self):
        Tag.objects.create(name='tag')
        t = Template("""
        {% load objectapp_tags %}
        {% get_tags as gbobject_tags %}
        {{ gbobject_tags|join:", " }}
        """)
        html = t.render(Context())
        self.assertEquals(html.strip(), '')
        self.publish_gbobject()
        html = t.render(Context())
        self.assertEquals(html.strip(), 'test, objectapp')

        template_error_as = """
        {% load objectapp_tags %}
        {% get_tags a_s gbobject_tags %}"""
        self.assertRaises(TemplateSyntaxError, Template, template_error_as)

        template_error_args = """
        {% load objectapp_tags %}
        {% get_tags as gbobject tags %}"""
        self.assertRaises(TemplateSyntaxError, Template, template_error_args)

    def test_get_tag_cloud(self):
        context = get_tag_cloud()
        self.assertEquals(len(context['tags']), 0)
        self.assertEquals(context['template'], 'objectapp/tags/tag_cloud.html')
        self.publish_gbobject()
        context = get_tag_cloud(6, 'custom_template.html')
        self.assertEquals(len(context['tags']), 2)
        self.assertEquals(context['template'], 'custom_template.html')
