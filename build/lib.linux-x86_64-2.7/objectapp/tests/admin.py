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
"""Test cases for Objectapp's admin"""
from django.test import TestCase
from django.contrib.auth.models import User

from objectapp import settings
from objectapp.models import Gbobject
from objectapp.models import Objecttype


class GbobjectAdminTestCase(TestCase):
    """Test case for Gbobject Admin"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        self.original_wysiwyg = settings.WYSIWYG
        settings.WYSIWYG = None
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        Objecttype_1 = Objecttype.objects.create(title='Objecttype 1', slug='cat-1')
        Objecttype.objects.create(title='Objecttype 2', slug='cat-2',
                                parent=Objecttype_1)

        self.client.login(username='admin', password='password')

    def tearDown(self):
        settings.WYSIWYG = self.original_wysiwyg

    def test_gbobject_add_and_change(self):
        """Test the insertion of an Gbobject"""
        self.assertEquals(Gbobject.objects.count(), 0)
        post_data = {'title': u'New gbobject',
                     'template': u'objectapp/gbobject_detail.html',
                     'creation_date_0': u'2011-01-01',
                     'creation_date_1': u'12:00:00',
                     'start_publication_0': u'2011-01-01',
                     'start_publication_1': u'12:00:00',
                     'end_publication_0': u'2042-03-15',
                     'end_publication_1': u'00:00:00',
                     'status': u'2',
                     'sites': u'1',
                     'content': u'My content'}

        response = self.client.post('/admin/objectapp/gbobject/add/', post_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Gbobject.objects.count(), 0)

        post_data.update({'slug': u'new-gbobject'})
        response = self.client.post('/admin/objectapp/gbobject/add/',
                                    post_data, follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/objectapp/gbobject/', 302)])
        self.assertEquals(Gbobject.objects.count(), 1)


class ObjecttypeAdminTestCase(TestCase):
    """Test cases for Objecttype Admin"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def test_Objecttype_add_and_change(self):
        """Test the insertion of a Objecttype, change error, and new insert"""
        self.assertEquals(Objecttype.objects.count(), 0)
        post_data = {'title': u'New Objecttype',
                     'slug': u'new-Objecttype'}
        response = self.client.post('/admin/objectapp/Objecttype/add/',
                                    post_data, follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/objectapp/Objecttype/', 302)])
        self.assertEquals(Objecttype.objects.count(), 1)

        post_data.update({'parent': u'1'})
        response = self.client.post('/admin/objectapp/Objecttype/1/', post_data)
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/objectapp/Objecttype/add/', post_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Objecttype.objects.count(), 1)

        post_data.update({'slug': u'new-Objecttype-2'})
        response = self.client.post('/admin/objectapp/Objecttype/add/',
                                    post_data, follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/objectapp/Objecttype/', 302)])
        self.assertEquals(Objecttype.objects.count(), 2)
