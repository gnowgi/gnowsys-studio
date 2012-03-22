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


"""Test cases for Objectapp's sitemaps"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tagging.models import Tag

from objectapp.models import Gbobject
from objectapp.models import Author
from objectapp.models import Objecttype
from objectapp.managers import PUBLISHED
from objectapp.sitemaps import GbobjectSitemap
from objectapp.sitemaps import ObjecttypeSitemap
from objectapp.sitemaps import AuthorSitemap
from objectapp.sitemaps import TagSitemap


class ObjectappSitemapsTestCase(TestCase):
    """Test cases for Sitemaps classes provided"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.Objecttype = Objecttype.objects.create(title='Tests', slug='tests')
        params = {'title': 'My gbobject 1', 'content': 'My content 1',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-1',
                  'status': PUBLISHED}
        self.gbobject_1 = Gbobject.objects.create(**params)
        self.gbobject_1.authors.add(self.author)
        self.gbobject_1.objecttypes.add(self.Objecttype)
        self.gbobject_1.sites.add(self.site)

        params = {'title': 'My gbobject 2', 'content': 'My content 2',
                  'tags': 'objectapp', 'slug': 'my-gbobject-2',
                  'status': PUBLISHED}
        self.gbobject_2 = Gbobject.objects.create(**params)
        self.gbobject_2.authors.add(self.author)
        self.gbobject_2.objecttypes.add(self.Objecttype)
        self.gbobject_2.sites.add(self.site)

    def test_gbobject_sitemap(self):
        sitemap = GbobjectSitemap()
        self.assertEquals(len(sitemap.items()), 2)
        self.assertEquals(sitemap.lastmod(self.gbobject_1),
                          self.gbobject_1.last_update)

    def test_Objecttype_sitemap(self):
        sitemap = ObjecttypeSitemap()
        self.assertEquals(len(sitemap.items()), 1)
        self.assertEquals(sitemap.lastmod(self.Objecttype),
                          self.gbobject_2.creation_date)
        self.assertEquals(sitemap.lastmod(Objecttype.objects.create(
            title='New', slug='new')), None)
        self.assertEquals(sitemap.priority(self.Objecttype), '1.0')

    def test_author_sitemap(self):
        sitemap = AuthorSitemap()
        authors = sitemap.items()
        self.assertEquals(len(authors), 1)
        self.assertEquals(sitemap.lastmod(authors[0]),
                          self.gbobject_2.creation_date)
        self.assertEquals(sitemap.lastmod(Author.objects.create(
            username='New', email='new@example.com')), None)
        self.assertEquals(sitemap.location(self.author), '/authors/admin/')

    def test_tag_sitemap(self):
        sitemap = TagSitemap()
        objectapp_tag = Tag.objects.get(name='objectapp')
        self.assertEquals(len(sitemap.items()), 2)
        self.assertEquals(sitemap.lastmod(objectapp_tag),
                          self.gbobject_2.creation_date)
        self.assertEquals(sitemap.priority(objectapp_tag), '1.0')
        self.assertEquals(sitemap.location(objectapp_tag), '/tags/objectapp/')

    def test_Objecttype_sitemap_zero_division_error(self):
        Gbobject.objects.all().delete()
        Objecttype_sitemap = ObjecttypeSitemap()
        Objecttype_sitemap.items()
        self.assertEquals(Objecttype_sitemap.priority(self.Objecttype), '0.5')
