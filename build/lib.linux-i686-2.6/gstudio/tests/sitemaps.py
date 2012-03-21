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
"""Test cases for Gstudio's sitemaps"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tagging.models import Tag

from gstudio.models import Nodetype
from gstudio.models import Author
from gstudio.models import Metatype
from gstudio.managers import PUBLISHED
from gstudio.sitemaps import NodetypeSitemap
from gstudio.sitemaps import MetatypeSitemap
from gstudio.sitemaps import AuthorSitemap
from gstudio.sitemaps import TagSitemap


class GstudioSitemapsTestCase(TestCase):
    """Test cases for Sitemaps classes provided"""
    urls = 'gstudio.tests.urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.metatype = Metatype.objects.create(title='Tests', slug='tests')
        params = {'title': 'My nodetype 1', 'content': 'My content 1',
                  'tags': 'gstudio, test', 'slug': 'my-nodetype-1',
                  'status': PUBLISHED}
        self.nodetype_1 = Nodetype.objects.create(**params)
        self.nodetype_1.authors.add(self.author)
        self.nodetype_1.metatypes.add(self.metatype)
        self.nodetype_1.sites.add(self.site)

        params = {'title': 'My nodetype 2', 'content': 'My content 2',
                  'tags': 'gstudio', 'slug': 'my-nodetype-2',
                  'status': PUBLISHED}
        self.nodetype_2 = Nodetype.objects.create(**params)
        self.nodetype_2.authors.add(self.author)
        self.nodetype_2.metatypes.add(self.metatype)
        self.nodetype_2.sites.add(self.site)

    def test_nodetype_sitemap(self):
        sitemap = NodetypeSitemap()
        self.assertEquals(len(sitemap.items()), 2)
        self.assertEquals(sitemap.lastmod(self.nodetype_1),
                          self.nodetype_1.last_update)

    def test_metatype_sitemap(self):
        sitemap = MetatypeSitemap()
        self.assertEquals(len(sitemap.items()), 1)
        self.assertEquals(sitemap.lastmod(self.metatype),
                          self.nodetype_2.creation_date)
        self.assertEquals(sitemap.lastmod(Metatype.objects.create(
            title='New', slug='new')), None)
        self.assertEquals(sitemap.priority(self.metatype), '1.0')

    def test_author_sitemap(self):
        sitemap = AuthorSitemap()
        authors = sitemap.items()
        self.assertEquals(len(authors), 1)
        self.assertEquals(sitemap.lastmod(authors[0]),
                          self.nodetype_2.creation_date)
        self.assertEquals(sitemap.lastmod(Author.objects.create(
            username='New', email='new@example.com')), None)
        self.assertEquals(sitemap.location(self.author), '/authors/admin/')

    def test_tag_sitemap(self):
        sitemap = TagSitemap()
        gstudio_tag = Tag.objects.get(name='gstudio')
        self.assertEquals(len(sitemap.items()), 2)
        self.assertEquals(sitemap.lastmod(gstudio_tag),
                          self.nodetype_2.creation_date)
        self.assertEquals(sitemap.priority(gstudio_tag), '1.0')
        self.assertEquals(sitemap.location(gstudio_tag), '/tags/gstudio/')

    def test_metatype_sitemap_zero_division_error(self):
        Nodetype.objects.all().delete()
        metatype_sitemap = MetatypeSitemap()
        metatype_sitemap.items()
        self.assertEquals(metatype_sitemap.priority(self.metatype), '0.5')
