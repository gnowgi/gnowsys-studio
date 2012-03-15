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
"""Test cases for Objectapp's feeds"""
from datetime import datetime

from django.test import TestCase
from django.conf import settings
from django.contrib import comments
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import DefaultFeed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from tagging.models import Tag

from objectapp.models import Gbobject
from objectapp.models import Objecttype
from objectapp.managers import PUBLISHED
from objectapp import feeds
from objectapp.feeds import GbobjectFeed
from objectapp.feeds import LatestGbobjects
from objectapp.feeds import ObjecttypeGbobjects
from objectapp.feeds import AuthorGbobjects
from objectapp.feeds import TagGbobjects
from objectapp.feeds import SearchGbobjects
from objectapp.feeds import GbobjectDiscussions
from objectapp.feeds import GbobjectComments
from objectapp.feeds import GbobjectPingbacks
from objectapp.feeds import GbobjectTrackbacks


class ObjectappFeedsTestCase(TestCase):
    """Test cases for the Feed classes provided"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.Objecttype = Objecttype.objects.create(title='Tests', slug='tests')
        self.gbobject_ct_id = ContentType.objects.get_for_model(Gbobject).pk

    def create_published_gbobject(self):
        params = {'title': 'My test gbobject',
                  'content': 'My test content with image '
                  '<img src="/image.jpg" />',
                  'slug': 'my-test-gbobject',
                  'tags': 'tests',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        gbobject = Gbobject.objects.create(**params)
        gbobject.sites.add(self.site)
        gbobject.objecttypes.add(self.Objecttype)
        gbobject.authors.add(self.author)
        return gbobject

    def create_discussions(self, gbobject):
        comment = comments.get_model().objects.create(comment='My Comment',
                                                      user=self.author,
                                                      content_object=gbobject,
                                                      site=self.site)
        pingback = comments.get_model().objects.create(comment='My Pingback',
                                                       user=self.author,
                                                       content_object=gbobject,
                                                       site=self.site)
        pingback.flags.create(user=self.author, flag='pingback')
        trackback = comments.get_model().objects.create(comment='My Trackback',
                                                        user=self.author,
                                                        content_object=gbobject,
                                                        site=self.site)
        trackback.flags.create(user=self.author, flag='trackback')
        return [comment, pingback, trackback]

    def test_gbobject_feed(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        gbobject = self.create_published_gbobject()
        feed = GbobjectFeed()
        self.assertEquals(feed.item_pubdate(gbobject), gbobject.creation_date)
        self.assertEquals(feed.item_objecttypes(gbobject), [self.Objecttype.title])
        self.assertEquals(feed.item_author_name(gbobject), self.author.username)
        self.assertEquals(feed.item_author_email(gbobject), self.author.email)
        self.assertEquals(
            feed.item_author_link(gbobject),
            'http://example.com/authors/%s/' % self.author.username)
        # Test a NoReverseMatch for item_author_link
        self.author.username = '[]'
        self.author.save()
        feed.item_author_name(gbobject)
        self.assertEquals(feed.item_author_link(gbobject), 'http://example.com')
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_gbobject_feed_enclosure(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        gbobject = self.create_published_gbobject()
        feed = GbobjectFeed()
        self.assertEquals(
            feed.item_enclosure_url(gbobject), 'http://example.com/image.jpg')
        gbobject.content = 'My test content with image <img src="image.jpg" />',
        gbobject.save()
        self.assertEquals(
            feed.item_enclosure_url(gbobject), 'http://example.com/image.jpg')
        gbobject.content = 'My test content with image ' \
                        '<img src="http://test.com/image.jpg" />'
        gbobject.save()
        self.assertEquals(
            feed.item_enclosure_url(gbobject), 'http://test.com/image.jpg')
        gbobject.image = 'image_field.jpg'
        gbobject.save()
        self.assertEquals(feed.item_enclosure_url(gbobject),
                          '%simage_field.jpg' % settings.MEDIA_URL)
        self.assertEquals(feed.item_enclosure_length(gbobject), '100000')
        self.assertEquals(feed.item_enclosure_mime_type(gbobject), 'image/jpeg')
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_latest_gbobjects(self):
        self.create_published_gbobject()
        feed = LatestGbobjects()
        self.assertEquals(feed.link(), '/')
        self.assertEquals(len(feed.items()), 1)
        self.assertEquals(feed.title(),
                          'example.com - %s' % _('Latest gbobjects'))
        self.assertEquals(
            feed.description(),
            _('The latest gbobjects for the site %s') % 'example.com')

    def test_Objecttype_gbobjects(self):
        self.create_published_gbobject()
        feed = ObjecttypeGbobjects()
        self.assertEquals(feed.get_object('request', '/tests/'), self.Objecttype)
        self.assertEquals(len(feed.items(self.Objecttype)), 1)
        self.assertEquals(feed.link(self.Objecttype), '/objecttypes/tests/')
        self.assertEquals(
            feed.title(self.Objecttype),
            _('Gbobjects for the Objecttype %s') % self.Objecttype.title)
        self.assertEquals(
            feed.description(self.Objecttype),
            _('The latest gbobjects for the Objecttype %s') % self.Objecttype.title)

    def test_author_gbobjects(self):
        self.create_published_gbobject()
        feed = AuthorGbobjects()
        self.assertEquals(feed.get_object('request', 'admin'), self.author)
        self.assertEquals(len(feed.items(self.author)), 1)
        self.assertEquals(feed.link(self.author), '/authors/admin/')
        self.assertEquals(feed.title(self.author),
                          _('Gbobjects for author %s') % self.author.username)
        self.assertEquals(feed.description(self.author),
                          _('The latest gbobjects by %s') % self.author.username)

    def test_tag_gbobjects(self):
        self.create_published_gbobject()
        feed = TagGbobjects()
        tag = Tag(name='tests')
        self.assertEquals(feed.get_object('request', 'tests').name, 'tests')
        self.assertEquals(len(feed.items('tests')), 1)
        self.assertEquals(feed.link(tag), '/tags/tests/')
        self.assertEquals(feed.title(tag),
                          _('Gbobjects for the tag %s') % tag.name)
        self.assertEquals(feed.description(tag),
                          _('The latest gbobjects for the tag %s') % tag.name)

    def test_search_gbobjects(self):
        class FakeRequest:
            def __init__(self, val):
                self.GET = {'pattern': val}
        self.create_published_gbobject()
        feed = SearchGbobjects()
        self.assertRaises(ObjectDoesNotExist,
                          feed.get_object, FakeRequest('te'))
        self.assertEquals(feed.get_object(FakeRequest('test')), 'test')
        self.assertEquals(len(feed.items('test')), 1)
        self.assertEquals(feed.link('test'), '/search/?pattern=test')
        self.assertEquals(feed.title('test'),
                          _("Results of the search for '%s'") % 'test')
        self.assertEquals(
            feed.description('test'),
            _("The gbobjects containing the pattern '%s'") % 'test')

    def test_gbobject_discussions(self):
        gbobject = self.create_published_gbobject()
        comments = self.create_discussions(gbobject)
        feed = GbobjectDiscussions()
        self.assertEquals(feed.get_object(
            'request', 2010, 1, 1, gbobject.slug), gbobject)
        self.assertEquals(feed.link(gbobject), '/2010/01/01/my-test-gbobject/')
        self.assertEquals(len(feed.items(gbobject)), 3)
        self.assertEquals(feed.item_pubdate(comments[0]),
                          comments[0].submit_date)
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#c1' % self.gbobject_ct_id)
        self.assertEquals(feed.item_author_name(comments[0]), 'admin')
        self.assertEquals(feed.item_author_email(comments[0]),
                          'admin@example.com')
        self.assertEquals(feed.item_author_link(comments[0]), '')
        self.assertEquals(feed.title(gbobject),
                          _('Discussions on %s') % gbobject.title)
        self.assertEquals(
            feed.description(gbobject),
            _('The latest discussions for the gbobject %s') % gbobject.title)

    def test_gbobject_comments(self):
        gbobject = self.create_published_gbobject()
        comments = self.create_discussions(gbobject)
        feed = GbobjectComments()
        self.assertEquals(list(feed.items(gbobject)), [comments[0]])
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#comment_1' % self.gbobject_ct_id)
        self.assertEquals(feed.title(gbobject),
                          _('Comments on %s') % gbobject.title)
        self.assertEquals(
            feed.description(gbobject),
            _('The latest comments for the gbobject %s') % gbobject.title)
        self.assertEquals(
            feed.item_enclosure_url(comments[0]),
            'http://www.gravatar.com/avatar/e64c7d89f26b'
            'd1972efa854d13d7dd61.jpg?s=80&amp;r=g')
        self.assertEquals(feed.item_enclosure_length(gbobject), '100000')
        self.assertEquals(feed.item_enclosure_mime_type(gbobject), 'image/jpeg')

    def test_gbobject_pingbacks(self):
        gbobject = self.create_published_gbobject()
        comments = self.create_discussions(gbobject)
        feed = GbobjectPingbacks()
        self.assertEquals(list(feed.items(gbobject)), [comments[1]])
        self.assertEquals(feed.item_link(comments[1]),
                          '/comments/cr/%i/1/#pingback_2' % self.gbobject_ct_id)
        self.assertEquals(feed.title(gbobject),
                          _('Pingbacks on %s') % gbobject.title)
        self.assertEquals(
            feed.description(gbobject),
            _('The latest pingbacks for the gbobject %s') % gbobject.title)

    def test_gbobject_trackbacks(self):
        gbobject = self.create_published_gbobject()
        comments = self.create_discussions(gbobject)
        feed = GbobjectTrackbacks()
        self.assertEquals(list(feed.items(gbobject)), [comments[2]])
        self.assertEquals(feed.item_link(comments[2]),
                          '/comments/cr/%i/1/#trackback_3' % self.gbobject_ct_id)
        self.assertEquals(feed.title(gbobject),
                          _('Trackbacks on %s') % gbobject.title)
        self.assertEquals(
            feed.description(gbobject),
            _('The latest trackbacks for the gbobject %s') % gbobject.title)

    def test_gbobject_feed_no_authors(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        gbobject = self.create_published_gbobject()
        gbobject.authors.clear()
        feed = GbobjectFeed()
        self.assertEquals(feed.item_author_name(gbobject), None)
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_gbobject_feed_rss_or_atom(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        feed = LatestGbobjects()
        self.assertEquals(feed.feed_type, DefaultFeed)
        feeds.FEEDS_FORMAT = 'atom'
        feed = LatestGbobjects()
        self.assertEquals(feed.feed_type, Atom1Feed)
        self.assertEquals(feed.subtitle, feed.description)
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_discussion_feed_with_same_slugs(self):
        """
        https://github.com/Fantomas42/django-blog-objectapp/issues/104

        OK, Here I will reproduce the original case: getting a discussion
        type feed, with a same slug.

        The correction of this case, will need some changes in the
        get_object method.
        """
        gbobject = self.create_published_gbobject()

        feed = GbobjectDiscussions()
        self.assertEquals(feed.get_object(
            'request', 2010, 1, 1, gbobject.slug), gbobject)

        params = {'title': 'My test gbobject, part II',
                  'content': 'My content ',
                  'slug': 'my-test-gbobject',
                  'tags': 'tests',
                  'creation_date': datetime(2010, 2, 1),
                  'status': PUBLISHED}
        gbobject_same_slug = Gbobject.objects.create(**params)
        gbobject_same_slug.sites.add(self.site)
        gbobject_same_slug.authors.add(self.author)

        self.assertEquals(feed.get_object(
            'request', 2010, 2, 1, gbobject_same_slug.slug), gbobject_same_slug)
