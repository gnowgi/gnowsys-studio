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
"""Test cases for Objectapp's PingBack API"""
import cStringIO
from datetime import datetime
from urlparse import urlsplit
from urllib2 import HTTPError
from xmlrpclib import ServerProxy

from django.test import TestCase
from django.contrib import comments
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from BeautifulSoup import BeautifulSoup

from objectapp.models import Gbobject
from objectapp.models import Objecttype
from objectapp.managers import PUBLISHED
from objectapp.tests.utils import TestTransport
from objectapp.xmlrpc.pingback import generate_pingback_content
from objectapp import url_shortener as shortener_settings


class PingBackTestCase(TestCase):
    """Test cases for pingbacks"""
    urls = 'objectapp.tests.urls'

    def fake_urlopen(self, url):
        """Fake urlopen using client if domain
        correspond to current_site else HTTPError"""
        scheme, netloc, path, query, fragment = urlsplit(url)
        if not netloc:
            raise
        if self.site.domain == netloc:
            response = cStringIO.StringIO(self.client.get(url).content)
            return response
        raise HTTPError(url, 404, 'unavailable url', {}, None)

    def setUp(self):
        # Use default URL shortener backend, to avoid networks errors
        self.original_shortener = shortener_settings.URL_SHORTENER_BACKEND
        shortener_settings.URL_SHORTENER_BACKEND = 'objectapp.url_shortener.'\
                                                   'backends.default'
        # Set up a stub around urlopen
        import objectapp.xmlrpc.pingback
        self.original_urlopen = objectapp.xmlrpc.pingback.urlopen
        objectapp.xmlrpc.pingback.urlopen = self.fake_urlopen
        # Preparing site
        self.site = Site.objects.get_current()
        self.site.domain = 'localhost:8000'
        self.site.save()
        # Creating tests gbobjects
        self.author = User.objects.create_user(username='webmaster',
                                               email='webmaster@example.com')
        self.Objecttype = Objecttype.objects.create(title='test', slug='test')
        params = {'title': 'My first gbobject',
                  'content': 'My first content',
                  'slug': 'my-first-gbobject',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        self.first_gbobject = Gbobject.objects.create(**params)
        self.first_gbobject.sites.add(self.site)
        self.first_gbobject.objecttypes.add(self.Objecttype)
        self.first_gbobject.authors.add(self.author)

        params = {'title': 'My second gbobject',
                  'content': 'My second content with link '
                  'to <a href="http://%s%s">first gbobject</a>'
                  ' and other links : %s %s.' % (
                      self.site.domain,
                      self.first_gbobject.get_absolute_url(),
                      'http://localhost:8000/error-404/',
                      'http://example.com/'),
                  'slug': 'my-second-gbobject',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        self.second_gbobject = Gbobject.objects.create(**params)
        self.second_gbobject.sites.add(self.site)
        self.second_gbobject.objecttypes.add(self.Objecttype)
        self.second_gbobject.authors.add(self.author)
        # Instanciating the server proxy
        self.server = ServerProxy('http://localhost:8000/xmlrpc/',
                                  transport=TestTransport())

    def tearDown(self):
        import objectapp.xmlrpc.pingback
        objectapp.xmlrpc.pingback.urlopen = self.original_urlopen
        shortener_settings.URL_SHORTENER_BACKEND = self.original_shortener

    def test_generate_pingback_content(self):
        soup = BeautifulSoup(self.second_gbobject.content)
        target = 'http://%s%s' % (self.site.domain,
                                  self.first_gbobject.get_absolute_url())

        self.assertEquals(
            generate_pingback_content(soup, target, 1000),
            'My second content with link to first gbobject and other links : '
            'http://localhost:8000/error-404/ http://example.com/.')
        self.assertEquals(
            generate_pingback_content(soup, target, 50),
            '...ond content with link to first gbobject and other lin...')

        soup = BeautifulSoup('<a href="%s">test link</a>' % target)
        self.assertEquals(
            generate_pingback_content(soup, target, 6), 'test l...')

        soup = BeautifulSoup('test <a href="%s">link</a>' % target)
        self.assertEquals(
            generate_pingback_content(soup, target, 8), '...est link')
        self.assertEquals(
            generate_pingback_content(soup, target, 9), 'test link')

    def test_pingback_ping(self):
        target = 'http://%s%s' % (
            self.site.domain, self.first_gbobject.get_absolute_url())
        source = 'http://%s%s' % (
            self.site.domain, self.second_gbobject.get_absolute_url())

        # Error code 0 : A generic fault code
        response = self.server.pingback.ping('toto', 'titi')
        self.assertEquals(response, 0)
        response = self.server.pingback.ping('http://%s/' % self.site.domain,
                                             'http://%s/' % self.site.domain)
        self.assertEquals(response, 0)

        # Error code 16 : The source URI does not exist.
        response = self.server.pingback.ping('http://example.com/', target)
        self.assertEquals(response, 16)

        # Error code 17 : The source URI does not contain a link to
        # the target URI and so cannot be used as a source.
        response = self.server.pingback.ping(source, 'toto')
        self.assertEquals(response, 17)

        # Error code 32 : The target URI does not exist.
        response = self.server.pingback.ping(
            source, 'http://localhost:8000/error-404/')
        self.assertEquals(response, 32)
        response = self.server.pingback.ping(source, 'http://example.com/')
        self.assertEquals(response, 32)

        # Error code 33 : The target URI cannot be used as a target.
        response = self.server.pingback.ping(source, 'http://localhost:8000/')
        self.assertEquals(response, 33)
        self.first_gbobject.pingback_enabled = False
        self.first_gbobject.save()
        response = self.server.pingback.ping(source, target)
        self.assertEquals(response, 33)

        # Validate pingback
        self.assertEquals(self.first_gbobject.comments.count(), 0)
        self.first_gbobject.pingback_enabled = True
        self.first_gbobject.save()
        response = self.server.pingback.ping(source, target)
        self.assertEquals(
            response,
            'Pingback from %s to %s registered.' % (source, target))
        self.assertEquals(self.first_gbobject.pingbacks.count(), 1)
        self.assertTrue(self.second_gbobject.title in \
                        self.first_gbobject.pingbacks[0].user_name)

        # Error code 48 : The pingback has already been registered.
        response = self.server.pingback.ping(source, target)
        self.assertEquals(response, 48)

    def test_pingback_extensions_get_pingbacks(self):
        target = 'http://%s%s' % (
            self.site.domain, self.first_gbobject.get_absolute_url())
        source = 'http://%s%s' % (
            self.site.domain, self.second_gbobject.get_absolute_url())

        response = self.server.pingback.ping(source, target)
        self.assertEquals(
            response, 'Pingback from %s to %s registered.' % (source, target))

        response = self.server.pingback.extensions.getPingbacks(
            'http://example.com/')
        self.assertEquals(response, 32)

        response = self.server.pingback.extensions.getPingbacks(
            'http://localhost:8000/error-404/')
        self.assertEquals(response, 32)

        response = self.server.pingback.extensions.getPingbacks(
            'http://localhost:8000/2010/')
        self.assertEquals(response, 33)

        response = self.server.pingback.extensions.getPingbacks(source)
        self.assertEquals(response, [])

        response = self.server.pingback.extensions.getPingbacks(target)
        self.assertEquals(response, [
            'http://localhost:8000/2010/01/01/my-second-gbobject/'])

        comment = comments.get_model().objects.create(
            content_type=ContentType.objects.get_for_model(Gbobject),
            object_pk=self.first_gbobject.pk,
            site=self.site, comment='Test pingback',
            user_url='http://example.com/blog/1/',
            user_name='Test pingback')
        comment.flags.create(user=self.author, flag='pingback')

        response = self.server.pingback.extensions.getPingbacks(target)
        self.assertEquals(response, [
            'http://localhost:8000/2010/01/01/my-second-gbobject/',
            'http://example.com/blog/1/'])
