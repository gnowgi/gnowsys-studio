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


"""Test cases for Gstudio's ping"""
import cStringIO
from urllib2 import URLError
from urllib import addinfourl
from django.test import TestCase

from gstudio.models import Nodetype
from gstudio.ping import URLRessources
from gstudio.ping import DirectoryPinger
from gstudio.ping import ExternalUrlsPinger


class DirectoryPingerTestCase(TestCase):
    """Test cases for DirectoryPinger"""
    def setUp(self):
        params = {'title': 'My nodetype',
                  'content': 'My content',
                  'tags': 'gstudio, test',
                  'slug': 'my-nodetype'}
        self.nodetype = Nodetype.objects.create(**params)
        self.pinger = DirectoryPinger('http://localhost', [self.nodetype],
                                      start_now=False)

    def test_ping_nodetype(self):
        self.assertEquals(
            self.pinger.ping_nodetype(self.nodetype),
            {'message': 'http://localhost is an invalid directory.',
             'flerror': True})


class ExternalUrlsPingerTestCase(TestCase):
    """Test cases for ExternalUrlsPinger"""

    def setUp(self):
        params = {'title': 'My nodetype',
                  'content': 'My content',
                  'tags': 'gstudio, test',
                  'slug': 'my-nodetype'}
        self.nodetype = Nodetype.objects.create(**params)
        self.pinger = ExternalUrlsPinger(self.nodetype, start_now=False)

    def test_is_external_url(self):
        r = URLRessources()
        self.assertEquals(self.pinger.is_external_url(
            'http://example.com/', 'http://google.com/'), True)
        self.assertEquals(self.pinger.is_external_url(
            'http://example.com/toto/', 'http://google.com/titi/'), True)
        self.assertEquals(self.pinger.is_external_url(
            'http://example.com/blog/', 'http://example.com/page/'), False)
        self.assertEquals(self.pinger.is_external_url(
            '%s/blog/' % r.site_url, r.site_url), False)
        self.assertEquals(self.pinger.is_external_url(
            'http://google.com/', r.site_url), True)
        self.assertEquals(self.pinger.is_external_url(
            '/blog/', r.site_url), False)

    def test_find_external_urls(self):
        r = URLRessources()
        external_urls = self.pinger.find_external_urls(self.nodetype)
        self.assertEquals(external_urls, [])
        self.nodetype.content = """
        <p>This is a <a href="http://fantomas.willbreak.it/">link</a>
        to a site.</p>
        <p>This is a <a href="%s/blog/">link</a> within my site.</p>
        <p>This is a <a href="/blog/">relative link</a> within my site.</p>
        """ % r.site_url
        self.nodetype.save()
        external_urls = self.pinger.find_external_urls(self.nodetype)
        self.assertEquals(external_urls, ['http://fantomas.willbreak.it/'])

    def test_find_pingback_href(self):
        result = self.pinger.find_pingback_href('')
        self.assertEquals(result, None)
        result = self.pinger.find_pingback_href("""
        <html><head><link rel="pingback" href="/xmlrpc/" /></head>
        <body></body></html>
        """)
        self.assertEquals(result, '/xmlrpc/')
        result = self.pinger.find_pingback_href("""
        <html><head><LINK hrEF="/xmlrpc/" REL="PingBack" /></head>
        <body></body></html>
        """)
        self.assertEquals(result, '/xmlrpc/')
        result = self.pinger.find_pingback_href("""
        <html><head><LINK REL="PingBack" /></head><body></body></html>
        """)
        self.assertEquals(result, None)

    def fake_urlopen(self, url):
        """Fake urlopen using test client"""
        if 'example' in url:
            response = cStringIO.StringIO('')
            return addinfourl(response, {'X-Pingback': '/xmlrpc.php',
                                         'Content-Type': 'text/html'}, url)
        elif 'localhost' in url:
            response = cStringIO.StringIO(
                '<link rel="pingback" href="/xmlrpc/">')
            return addinfourl(response, {'Content-Type': 'text/xhtml'}, url)
        elif 'google' in url:
            response = cStringIO.StringIO('PNG CONTENT')
            return addinfourl(response, {'content-type': 'image/png'}, url)
        elif 'error' in url:
            raise URLError('Invalid ressource')

    def test_find_pingback_urls(self):
        # Set up a stub around urlopen
        import gstudio.ping
        self.original_urlopen = gstudio.ping.urlopen
        gstudio.ping.urlopen = self.fake_urlopen

        urls = ['http://localhost/', 'http://example.com/', 'http://error',
                'http://www.google.co.uk/images/nav_logo72.png']
        self.assertEquals(
            self.pinger.find_pingback_urls(urls),
            {'http://localhost/': 'http://localhost/xmlrpc/',
             'http://example.com/': 'http://example.com/xmlrpc.php'})
        # Remove stub
        gstudio.ping.urlopen = self.original_urlopen

    def test_pingback_url(self):
        self.assertEquals(self.pinger.pingback_url('http://localhost',
                                                   'http://error.com'),
                          'http://error.com cannot be pinged.')
