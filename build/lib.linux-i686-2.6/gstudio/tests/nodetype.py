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


"""Test cases for Gstudio's Nodetype"""
from __future__ import with_statement
import warnings
from datetime import datetime
from datetime import timedelta

from django.test import TestCase
from django.conf import settings
from django.contrib import comments
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.comments.models import CommentFlag

from gstudio import models
from gstudio.models import Nodetype
from gstudio.managers import PUBLISHED
from gstudio.models import get_base_model
from gstudio.models import Nodetype
from gstudio import models as models_settings
from gstudio import url_shortener as shortener_settings


class NodetypeTestCase(TestCase):

    def setUp(self):
        params = {'title': 'My nodetype',
                  'content': 'My content',
                  'slug': 'my-nodetype'}
        self.nodetype = Nodetype.objects.create(**params)

    def test_discussions(self):
        site = Site.objects.get_current()
        self.assertEquals(self.nodetype.discussions.count(), 0)
        self.assertEquals(self.nodetype.comments.count(), 0)
        self.assertEquals(self.nodetype.pingbacks.count(), 0)
        self.assertEquals(self.nodetype.trackbacks.count(), 0)

        comments.get_model().objects.create(comment='My Comment 1',
                                            content_object=self.nodetype,
                                            site=site)
        self.assertEquals(self.nodetype.discussions.count(), 1)
        self.assertEquals(self.nodetype.comments.count(), 1)
        self.assertEquals(self.nodetype.pingbacks.count(), 0)
        self.assertEquals(self.nodetype.trackbacks.count(), 0)

        comments.get_model().objects.create(comment='My Comment 2',
                                            content_object=self.nodetype,
                                            site=site, is_public=False)
        self.assertEquals(self.nodetype.discussions.count(), 1)
        self.assertEquals(self.nodetype.comments.count(), 1)
        self.assertEquals(self.nodetype.pingbacks.count(), 0)
        self.assertEquals(self.nodetype.trackbacks.count(), 0)

        author = User.objects.create_user(username='webmaster',
                                          email='webmaster@example.com')

        comment = comments.get_model().objects.create(
            comment='My Comment 3',
            content_object=self.nodetype,
            site=Site.objects.create(domain='http://toto.com',
                                     name='Toto.com'))
        comment.flags.create(user=author, flag=CommentFlag.MODERATOR_APPROVAL)
        self.assertEquals(self.nodetype.discussions.count(), 2)
        self.assertEquals(self.nodetype.comments.count(), 2)
        self.assertEquals(self.nodetype.pingbacks.count(), 0)
        self.assertEquals(self.nodetype.trackbacks.count(), 0)

        comment = comments.get_model().objects.create(
            comment='My Pingback 1', content_object=self.nodetype, site=site)
        comment.flags.create(user=author, flag='pingback')
        self.assertEquals(self.nodetype.discussions.count(), 3)
        self.assertEquals(self.nodetype.comments.count(), 2)
        self.assertEquals(self.nodetype.pingbacks.count(), 1)
        self.assertEquals(self.nodetype.trackbacks.count(), 0)

        comment = comments.get_model().objects.create(
            comment='My Trackback 1', content_object=self.nodetype, site=site)
        comment.flags.create(user=author, flag='trackback')
        self.assertEquals(self.nodetype.discussions.count(), 4)
        self.assertEquals(self.nodetype.comments.count(), 2)
        self.assertEquals(self.nodetype.pingbacks.count(), 1)
        self.assertEquals(self.nodetype.trackbacks.count(), 1)

    def test_str(self):
        self.assertEquals(str(self.nodetype), 'My nodetype: draft')

    def test_word_count(self):
        self.assertEquals(self.nodetype.word_count, 2)

    def test_comments_are_open(self):
        original_auto_close = models.AUTO_CLOSE_COMMENTS_AFTER
        models.AUTO_CLOSE_COMMENTS_AFTER = None
        self.assertEquals(self.nodetype.comments_are_open, True)
        models.AUTO_CLOSE_COMMENTS_AFTER = 5
        self.nodetype.start_publication = datetime.now() - timedelta(days=7)
        self.nodetype.save()
        self.assertEquals(self.nodetype.comments_are_open, False)

        models.AUTO_CLOSE_COMMENTS_AFTER = original_auto_close

    def test_is_actual(self):
        self.assertTrue(self.nodetype.is_actual)
        self.nodetype.start_publication = datetime(2020, 3, 15)
        self.assertFalse(self.nodetype.is_actual)
        self.nodetype.start_publication = datetime.now()
        self.assertTrue(self.nodetype.is_actual)
        self.nodetype.end_publication = datetime(2000, 3, 15)
        self.assertFalse(self.nodetype.is_actual)

    def test_is_visible(self):
        self.assertFalse(self.nodetype.is_visible)
        self.nodetype.status = PUBLISHED
        self.assertTrue(self.nodetype.is_visible)
        self.nodetype.start_publication = datetime(2020, 3, 15)
        self.assertFalse(self.nodetype.is_visible)

    def test_short_url(self):
        original_shortener = shortener_settings.URL_SHORTENER_BACKEND
        shortener_settings.URL_SHORTENER_BACKEND = 'gstudio.url_shortener.'\
                                                   'backends.default'
        self.assertEquals(self.nodetype.short_url,
                          'http://example.com' +
                          reverse('gstudio_nodetype_shortlink',
                                  args=[self.nodetype.pk]))
        shortener_settings.URL_SHORTENER_BACKEND = original_shortener

    def test_previous_nodetype(self):
        site = Site.objects.get_current()
        self.assertFalse(self.nodetype.previous_nodetype)
        params = {'title': 'My second nodetype',
                  'content': 'My second content',
                  'slug': 'my-second-nodetype',
                  'creation_date': datetime(2000, 1, 1),
                  'status': PUBLISHED}
        self.second_nodetype = Nodetype.objects.create(**params)
        self.second_nodetype.sites.add(site)
        self.assertEquals(self.nodetype.previous_nodetype, self.second_nodetype)
        params = {'title': 'My third nodetype',
                  'content': 'My third content',
                  'slug': 'my-third-nodetype',
                  'creation_date': datetime(2001, 1, 1),
                  'status': PUBLISHED}
        self.third_nodetype = Nodetype.objects.create(**params)
        self.third_nodetype.sites.add(site)
        self.assertEquals(self.nodetype.previous_nodetype, self.third_nodetype)
        self.assertEquals(self.third_nodetype.previous_nodetype, self.second_nodetype)

    def test_next_nodetype(self):
        site = Site.objects.get_current()
        self.assertFalse(self.nodetype.next_nodetype)
        params = {'title': 'My second nodetype',
                  'content': 'My second content',
                  'slug': 'my-second-nodetype',
                  'creation_date': datetime(2100, 1, 1),
                  'status': PUBLISHED}
        self.second_nodetype = Nodetype.objects.create(**params)
        self.second_nodetype.sites.add(site)
        self.assertEquals(self.nodetype.next_nodetype, self.second_nodetype)
        params = {'title': 'My third nodetype',
                  'content': 'My third content',
                  'slug': 'my-third-nodetype',
                  'creation_date': datetime(2050, 1, 1),
                  'status': PUBLISHED}
        self.third_nodetype = Nodetype.objects.create(**params)
        self.third_nodetype.sites.add(site)
        self.assertEquals(self.nodetype.next_nodetype, self.third_nodetype)
        self.assertEquals(self.third_nodetype.next_nodetype, self.second_nodetype)

    def test_related_published(self):
        site = Site.objects.get_current()
        self.assertFalse(self.nodetype.related_published)
        params = {'title': 'My second nodetype',
                  'content': 'My second content',
                  'slug': 'my-second-nodetype',
                  'status': PUBLISHED}
        self.second_nodetype = Nodetype.objects.create(**params)
        self.second_nodetype.related.add(self.nodetype)
        self.assertEquals(len(self.nodetype.related_published), 0)

        self.second_nodetype.sites.add(site)
        self.assertEquals(len(self.nodetype.related_published), 1)
        self.assertEquals(len(self.second_nodetype.related_published), 0)

        self.nodetype.status = PUBLISHED
        self.nodetype.save()
        self.nodetype.sites.add(site)
        self.assertEquals(len(self.nodetype.related_published), 1)
        self.assertEquals(len(self.second_nodetype.related_published), 1)


class NodetypeHtmlContentTestCase(TestCase):

    def setUp(self):
        params = {'title': 'My nodetype',
                  'content': 'My content',
                  'slug': 'my-nodetype'}
        self.nodetype = Nodetype(**params)
        self.original_debug = settings.DEBUG
        self.original_rendering = models_settings.MARKUP_LANGUAGE
        settings.DEBUG = False

    def tearDown(self):
        settings.DEBUG = self.original_debug
        models_settings.MARKUP_LANGUAGE = self.original_rendering

    def test_html_content_default(self):
        models_settings.MARKUP_LANGUAGE = None
        self.assertEquals(self.nodetype.html_content, '<p>My content</p>')

        self.nodetype.content = 'Hello world !\n' \
                             ' this is my content'
        self.assertEquals(self.nodetype.html_content,
                          '<p>Hello world !<br /> this is my content</p>')

    def test_html_content_textitle(self):
        models_settings.MARKUP_LANGUAGE = 'textile'
        self.nodetype.content = 'Hello world !\n\n' \
                             'this is my content :\n\n' \
                             '* Item 1\n* Item 2'
        html_content = self.nodetype.html_content
        try:
            self.assertEquals(html_content,
                              '\t<p>Hello world !</p>\n\n\t' \
                              '<p>this is my content :</p>\n\n\t' \
                              '<ul>\n\t\t<li>Item 1</li>\n\t\t' \
                              '<li>Item 2</li>\n\t</ul>')
        except AssertionError:
            self.assertEquals(html_content, self.nodetype.content)

    def test_html_content_markdown(self):
        models_settings.MARKUP_LANGUAGE = 'markdown'
        self.nodetype.content = 'Hello world !\n\n' \
                             'this is my content :\n\n' \
                             '* Item 1\n* Item 2'
        html_content = self.nodetype.html_content
        try:
            self.assertEquals(html_content,
                              '<p>Hello world !</p>\n' \
                              '<p>this is my content :</p>'\
                              '\n<ul>\n<li>Item 1</li>\n' \
                              '<li>Item 2</li>\n</ul>')
        except AssertionError:
            self.assertEquals(html_content, self.nodetype.content)

    def test_html_content_restructuredtext(self):
        models_settings.MARKUP_LANGUAGE = 'restructuredtext'
        self.nodetype.content = 'Hello world !\n\n' \
                             'this is my content :\n\n' \
                             '* Item 1\n* Item 2'
        html_content = self.nodetype.html_content
        try:
            self.assertEquals(html_content,
                              '<p>Hello world !</p>\n' \
                              '<p>this is my content :</p>'\
                              '\n<ul class="simple">\n<li>Item 1</li>\n' \
                              '<li>Item 2</li>\n</ul>\n')
        except AssertionError:
            self.assertEquals(html_content, self.nodetype.content)

# this class can be removed since the base abstract class is no longer present.
class NodetypeGetBaseModelTestCase(TestCase):

    def setUp(self):
        self.original_nodetype_base_model = models_settings.NODETYPE_BASE_MODEL

    def tearDown(self):
        models_settings.NODETYPE_BASE_MODEL = self.original_nodetype_base_model

    def test_get_base_model(self):
        models_settings.NODETYPE_BASE_MODEL = ''
        self.assertEquals(get_base_model(), Nodetype)

        models_settings.NODETYPE_BASE_MODEL = 'mymodule.myclass'
        try:
            with warnings.catch_warnings(record=True) as w:
                self.assertEquals(get_base_model(), Nodetype)
                self.assertTrue(issubclass(w[-1].metatype, RuntimeWarning))
        except AttributeError:
            # Fail under Python2.5, because of'warnings.catch_warnings'
            pass

        models_settings.NODETYPE_BASE_MODEL = 'gstudio.models.Nodetype'
        self.assertEquals(get_base_model(), Nodetype)
