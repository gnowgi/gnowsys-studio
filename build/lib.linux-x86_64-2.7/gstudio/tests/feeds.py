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


"""Test cases for Gstudio's feeds"""
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

from gstudio.models import Nodetype
from gstudio.models import Metatype
from gstudio.managers import PUBLISHED
from gstudio import feeds
from gstudio.feeds import NodetypeFeed
from gstudio.feeds import LatestNodetypes
from gstudio.feeds import MetatypeNodetypes
from gstudio.feeds import AuthorNodetypes
from gstudio.feeds import TagNodetypes
from gstudio.feeds import SearchNodetypes
from gstudio.feeds import NodetypeDiscussions
from gstudio.feeds import NodetypeComments
from gstudio.feeds import NodetypePingbacks
from gstudio.feeds import NodetypeTrackbacks


class GstudioFeedsTestCase(TestCase):
    """Test cases for the Feed classes provided"""
    urls = 'gstudio.tests.urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.metatype = Metatype.objects.create(title='Tests', slug='tests')
        self.nodetype_ct_id = ContentType.objects.get_for_model(Nodetype).pk

    def create_published_nodetype(self):
        params = {'title': 'My test nodetype',
                  'content': 'My test content with image '
                  '<img src="/image.jpg" />',
                  'slug': 'my-test-nodetype',
                  'tags': 'tests',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        nodetype = Nodetype.objects.create(**params)
        nodetype.sites.add(self.site)
        nodetype.metatypes.add(self.metatype)
        nodetype.authors.add(self.author)
        return nodetype

    def create_discussions(self, nodetype):
        comment = comments.get_model().objects.create(comment='My Comment',
                                                      user=self.author,
                                                      content_object=nodetype,
                                                      site=self.site)
        pingback = comments.get_model().objects.create(comment='My Pingback',
                                                       user=self.author,
                                                       content_object=nodetype,
                                                       site=self.site)
        pingback.flags.create(user=self.author, flag='pingback')
        trackback = comments.get_model().objects.create(comment='My Trackback',
                                                        user=self.author,
                                                        content_object=nodetype,
                                                        site=self.site)
        trackback.flags.create(user=self.author, flag='trackback')
        return [comment, pingback, trackback]

    def test_nodetype_feed(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        nodetype = self.create_published_nodetype()
        feed = NodetypeFeed()
        self.assertEquals(feed.item_pubdate(nodetype), nodetype.creation_date)
        self.assertEquals(feed.item_metatypes(nodetype), [self.metatype.title])
        self.assertEquals(feed.item_author_name(nodetype), self.author.username)
        self.assertEquals(feed.item_author_email(nodetype), self.author.email)
        self.assertEquals(
            feed.item_author_link(nodetype),
            'http://example.com/authors/%s/' % self.author.username)
        # Test a NoReverseMatch for item_author_link
        self.author.username = '[]'
        self.author.save()
        feed.item_author_name(nodetype)
        self.assertEquals(feed.item_author_link(nodetype), 'http://example.com')
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_nodetype_feed_enclosure(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        nodetype = self.create_published_nodetype()
        feed = NodetypeFeed()
        self.assertEquals(
            feed.item_enclosure_url(nodetype), 'http://example.com/image.jpg')
        nodetype.content = 'My test content with image <img src="image.jpg" />',
        nodetype.save()
        self.assertEquals(
            feed.item_enclosure_url(nodetype), 'http://example.com/image.jpg')
        nodetype.content = 'My test content with image ' \
                        '<img src="http://test.com/image.jpg" />'
        nodetype.save()
        self.assertEquals(
            feed.item_enclosure_url(nodetype), 'http://test.com/image.jpg')
        nodetype.image = 'image_field.jpg'
        nodetype.save()
        self.assertEquals(feed.item_enclosure_url(nodetype),
                          '%simage_field.jpg' % settings.MEDIA_URL)
        self.assertEquals(feed.item_enclosure_length(nodetype), '100000')
        self.assertEquals(feed.item_enclosure_mime_type(nodetype), 'image/jpeg')
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_latest_nodetypes(self):
        self.create_published_nodetype()
        feed = LatestNodetypes()
        self.assertEquals(feed.link(), '/')
        self.assertEquals(len(feed.items()), 1)
        self.assertEquals(feed.title(),
                          'example.com - %s' % _('Latest nodetypes'))
        self.assertEquals(
            feed.description(),
            _('The latest nodetypes for the site %s') % 'example.com')

    def test_metatype_nodetypes(self):
        self.create_published_nodetype()
        feed = MetatypeNodetypes()
        self.assertEquals(feed.get_object('request', '/tests/'), self.metatype)
        self.assertEquals(len(feed.items(self.metatype)), 1)
        self.assertEquals(feed.link(self.metatype), '/metatypes/tests/')
        self.assertEquals(
            feed.title(self.metatype),
            _('Nodetypes for the metatype %s') % self.metatype.title)
        self.assertEquals(
            feed.description(self.metatype),
            _('The latest nodetypes for the metatype %s') % self.metatype.title)

    def test_author_nodetypes(self):
        self.create_published_nodetype()
        feed = AuthorNodetypes()
        self.assertEquals(feed.get_object('request', 'admin'), self.author)
        self.assertEquals(len(feed.items(self.author)), 1)
        self.assertEquals(feed.link(self.author), '/authors/admin/')
        self.assertEquals(feed.title(self.author),
                          _('Nodetypes for author %s') % self.author.username)
        self.assertEquals(feed.description(self.author),
                          _('The latest nodetypes by %s') % self.author.username)

    def test_tag_nodetypes(self):
        self.create_published_nodetype()
        feed = TagNodetypes()
        tag = Tag(name='tests')
        self.assertEquals(feed.get_object('request', 'tests').name, 'tests')
        self.assertEquals(len(feed.items('tests')), 1)
        self.assertEquals(feed.link(tag), '/tags/tests/')
        self.assertEquals(feed.title(tag),
                          _('Nodetypes for the tag %s') % tag.name)
        self.assertEquals(feed.description(tag),
                          _('The latest nodetypes for the tag %s') % tag.name)

    def test_search_nodetypes(self):
        class FakeRequest:
            def __init__(self, val):
                self.GET = {'pattern': val}
        self.create_published_nodetype()
        feed = SearchNodetypes()
        self.assertRaises(ObjectDoesNotExist,
                          feed.get_object, FakeRequest('te'))
        self.assertEquals(feed.get_object(FakeRequest('test')), 'test')
        self.assertEquals(len(feed.items('test')), 1)
        self.assertEquals(feed.link('test'), '/search/?pattern=test')
        self.assertEquals(feed.title('test'),
                          _("Results of the search for '%s'") % 'test')
        self.assertEquals(
            feed.description('test'),
            _("The nodetypes containing the pattern '%s'") % 'test')

    def test_nodetype_discussions(self):
        nodetype = self.create_published_nodetype()
        comments = self.create_discussions(nodetype)
        feed = NodetypeDiscussions()
        self.assertEquals(feed.get_object(
            'request', 2010, 1, 1, nodetype.slug), nodetype)
        self.assertEquals(feed.link(nodetype), '/2010/01/01/my-test-nodetype/')
        self.assertEquals(len(feed.items(nodetype)), 3)
        self.assertEquals(feed.item_pubdate(comments[0]),
                          comments[0].submit_date)
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#c1' % self.nodetype_ct_id)
        self.assertEquals(feed.item_author_name(comments[0]), 'admin')
        self.assertEquals(feed.item_author_email(comments[0]),
                          'admin@example.com')
        self.assertEquals(feed.item_author_link(comments[0]), '')
        self.assertEquals(feed.title(nodetype),
                          _('Discussions on %s') % nodetype.title)
        self.assertEquals(
            feed.description(nodetype),
            _('The latest discussions for the nodetype %s') % nodetype.title)

    def test_nodetype_comments(self):
        nodetype = self.create_published_nodetype()
        comments = self.create_discussions(nodetype)
        feed = NodetypeComments()
        self.assertEquals(list(feed.items(nodetype)), [comments[0]])
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#comment_1' % self.nodetype_ct_id)
        self.assertEquals(feed.title(nodetype),
                          _('Comments on %s') % nodetype.title)
        self.assertEquals(
            feed.description(nodetype),
            _('The latest comments for the nodetype %s') % nodetype.title)
        self.assertEquals(
            feed.item_enclosure_url(comments[0]),
            'http://www.gravatar.com/avatar/e64c7d89f26b'
            'd1972efa854d13d7dd61.jpg?s=80&amp;r=g')
        self.assertEquals(feed.item_enclosure_length(nodetype), '100000')
        self.assertEquals(feed.item_enclosure_mime_type(nodetype), 'image/jpeg')

    def test_nodetype_pingbacks(self):
        nodetype = self.create_published_nodetype()
        comments = self.create_discussions(nodetype)
        feed = NodetypePingbacks()
        self.assertEquals(list(feed.items(nodetype)), [comments[1]])
        self.assertEquals(feed.item_link(comments[1]),
                          '/comments/cr/%i/1/#pingback_2' % self.nodetype_ct_id)
        self.assertEquals(feed.title(nodetype),
                          _('Pingbacks on %s') % nodetype.title)
        self.assertEquals(
            feed.description(nodetype),
            _('The latest pingbacks for the nodetype %s') % nodetype.title)

    def test_nodetype_trackbacks(self):
        nodetype = self.create_published_nodetype()
        comments = self.create_discussions(nodetype)
        feed = NodetypeTrackbacks()
        self.assertEquals(list(feed.items(nodetype)), [comments[2]])
        self.assertEquals(feed.item_link(comments[2]),
                          '/comments/cr/%i/1/#trackback_3' % self.nodetype_ct_id)
        self.assertEquals(feed.title(nodetype),
                          _('Trackbacks on %s') % nodetype.title)
        self.assertEquals(
            feed.description(nodetype),
            _('The latest trackbacks for the nodetype %s') % nodetype.title)

    def test_nodetype_feed_no_authors(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        nodetype = self.create_published_nodetype()
        nodetype.authors.clear()
        feed = NodetypeFeed()
        self.assertEquals(feed.item_author_name(nodetype), None)
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_nodetype_feed_rss_or_atom(self):
        original_feeds_format = feeds.FEEDS_FORMAT
        feeds.FEEDS_FORMAT = ''
        feed = LatestNodetypes()
        self.assertEquals(feed.feed_type, DefaultFeed)
        feeds.FEEDS_FORMAT = 'atom'
        feed = LatestNodetypes()
        self.assertEquals(feed.feed_type, Atom1Feed)
        self.assertEquals(feed.subtitle, feed.description)
        feeds.FEEDS_FORMAT = original_feeds_format

    def test_discussion_feed_with_same_slugs(self):
        """
        https://github.com/gnowgi/django-gstudio/issues/104

        OK, Here I will reproduce the original case: getting a discussion
        type feed, with a same slug.

        The correction of this case, will need some changes in the
        get_object method.
        """
        nodetype = self.create_published_nodetype()

        feed = NodetypeDiscussions()
        self.assertEquals(feed.get_object(
            'request', 2010, 1, 1, nodetype.slug), nodetype)

        params = {'title': 'My test nodetype, part II',
                  'content': 'My content ',
                  'slug': 'my-test-nodetype',
                  'tags': 'tests',
                  'creation_date': datetime(2010, 2, 1),
                  'status': PUBLISHED}
        nodetype_same_slug = Nodetype.objects.create(**params)
        nodetype_same_slug.sites.add(self.site)
        nodetype_same_slug.authors.add(self.author)

        self.assertEquals(feed.get_object(
            'request', 2010, 2, 1, nodetype_same_slug.slug), nodetype_same_slug)
