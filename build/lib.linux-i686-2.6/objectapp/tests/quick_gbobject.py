
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
"""Test cases for Objectapp's quick gbobject"""
from django.test import TestCase
from django.contrib.auth.models import User

from objectapp import settings
from objectapp.models import Gbobject
from objectapp.managers import DRAFT


class QuickGbobjectTestCase(TestCase):
    """Test cases for quick_gbobject view"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        self.original_wysiwyg = settings.WYSIWYG
        settings.WYSIWYG = None

    def tearDown(self):
        settings.WYSIWYG = self.original_wysiwyg

    def test_quick_gbobject(self):
        User.objects.create_user('user', 'user@example.com', 'password')
        User.objects.create_superuser('admin', 'admin@example.com', 'password')

        response = self.client.get('/quick_gbobject/', follow=True)
        self.assertEquals(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/quick_gbobject/', 302)])
        self.client.login(username='user', password='password')
        response = self.client.get('/quick_gbobject/', follow=True)
        self.assertEquals(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/quick_gbobject/', 302)])
        self.client.logout()
        self.client.login(username='admin', password='password')
        response = self.client.get('/quick_gbobject/', follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/objectapp/gbobject/add/', 302)])
        response = self.client.post('/quick_gbobject/', {'title': 'test'},
                                    follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/objectapp/gbobject/add/' \
                            '?tags=&title=test&sites=1&content=' \
                            '%3Cp%3E%3C%2Fp%3E&authors=2&slug=test', 302)])
        response = self.client.post('/quick_gbobject/',
                                    {'title': 'test', 'tags': 'test',
                                     'content': 'Test content',
                                     'save_draft': ''}, follow=True)
        gbobject = Gbobject.objects.get(title='test')
        self.assertEquals(response.redirect_chain,
                          [('http://testserver%s' % gbobject.get_absolute_url(),
                            302)])
        self.assertEquals(gbobject.status, DRAFT)
        self.assertEquals(gbobject.title, 'test')
        self.assertEquals(gbobject.tags, 'test')
        self.assertEquals(gbobject.content, '<p>Test content</p>')
