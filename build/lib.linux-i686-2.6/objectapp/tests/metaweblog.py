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
"""Test cases for Objectapp's MetaWeblog API"""
from xmlrpclib import Binary
from xmlrpclib import Fault
from xmlrpclib import ServerProxy
from datetime import datetime
from tempfile import TemporaryFile

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage

from objectapp.models import Gbobject
from objectapp.models import Objecttype
from objectapp.managers import DRAFT
from objectapp.managers import PUBLISHED
from objectapp.settings import UPLOAD_TO
from objectapp.xmlrpc.metaweblog import authenticate
from objectapp.xmlrpc.metaweblog import post_structure
from objectapp.tests.utils import TestTransport


class MetaWeblogTestCase(TestCase):
    """Test cases for MetaWeblog"""
    urls = 'objectapp.tests.urls'

    def setUp(self):
        # Create data
        self.webmaster = User.objects.create_superuser(
            username='webmaster',
            email='webmaster@example.com',
            password='password')
        self.contributor = User.objects.create_user(
            username='contributor',
            email='contributor@example.com',
            password='password')
        self.site = Site.objects.get_current()
        self.objecttypes = [
            Objecttype.objects.create(title='Objecttype 1',
                                    slug='Objecttype-1'),
            Objecttype.objects.create(title='Objecttype 2',
                                    slug='Objecttype-2')]
        params = {'title': 'My gbobject 1', 'content': 'My content 1',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-1',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        self.gbobject_1 = Gbobject.objects.create(**params)
        self.gbobject_1.authors.add(self.webmaster)
        self.gbobject_1.objecttypes.add(*self.objecttypes)
        self.gbobject_1.sites.add(self.site)

        params = {'title': 'My gbobject 2', 'content': 'My content 2',
                  'creation_date': datetime(2010, 3, 15),
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-2'}
        self.gbobject_2 = Gbobject.objects.create(**params)
        self.gbobject_2.authors.add(self.webmaster)
        self.gbobject_2.objecttypes.add(self.objecttypes[0])
        self.gbobject_2.sites.add(self.site)
        # Instanciating the server proxy
        self.server = ServerProxy('http://localhost:8000/xmlrpc/',
                                  transport=TestTransport())

    def test_authenticate(self):
        self.assertRaises(Fault, authenticate, 'badcontributor', 'badpassword')
        self.assertRaises(Fault, authenticate, 'contributor', 'badpassword')
        self.assertRaises(Fault, authenticate, 'contributor', 'password')
        self.contributor.is_staff = True
        self.contributor.save()
        self.assertEquals(authenticate('contributor', 'password'),
                          self.contributor)
        self.assertRaises(Fault, authenticate, 'contributor',
                          'password', 'objectapp.change_gbobject')
        self.assertEquals(authenticate('webmaster', 'password'),
                          self.webmaster)
        self.assertEquals(authenticate('webmaster', 'password',
                                       'objectapp.change_gbobject'),
                          self.webmaster)

    def test_get_users_blogs(self):
        self.assertRaises(Fault, self.server.blogger.getUsersBlogs,
                          'apikey', 'contributor', 'password')
        self.assertEquals(self.server.blogger.getUsersBlogs(
            'apikey', 'webmaster', 'password'),
                          [{'url': 'http://example.com/',
                            'blogid': 1,
                            'blogName': 'example.com'}])

    def test_get_user_info(self):
        self.assertRaises(Fault, self.server.blogger.getUserInfo,
                          'apikey', 'contributor', 'password')
        self.webmaster.first_name = 'John'
        self.webmaster.last_name = 'Doe'
        self.webmaster.save()
        self.assertEquals(self.server.blogger.getUserInfo(
            'apikey', 'webmaster', 'password'),
                          {'firstname': 'John', 'lastname': 'Doe',
                           'url': 'http://example.com/authors/webmaster/',
                           'userid': self.webmaster.pk,
                           'nickname': 'webmaster',
                           'email': 'webmaster@example.com'})

    def test_get_authors(self):
        self.assertRaises(Fault, self.server.wp.getAuthors,
                          'apikey', 'contributor', 'password')
        self.assertEquals(self.server.wp.getAuthors(
            'apikey', 'webmaster', 'password'), [
                              {'user_login': 'webmaster',
                               'user_id': self.webmaster.pk,
                               'user_email': 'webmaster@example.com',
                               'display_name': 'webmaster'}])

    def test_get_objecttypes(self):
        self.assertRaises(Fault, self.server.metaWeblog.getObjecttypes,
                          1, 'contributor', 'password')
        self.assertEquals(
            self.server.metaWeblog.getObjecttypes('apikey',
                                                 'webmaster', 'password'),
            [{'rssUrl': 'http://example.com/feeds/objecttypes/Objecttype-1/',
              'description': 'Objecttype 1',
              'htmlUrl': 'http://example.com/objecttypes/Objecttype-1/',
              'ObjecttypeId': 1, 'parentId': 0,
              'ObjecttypeName': 'Objecttype 1',
              'ObjecttypeDescription': ''},
             {'rssUrl': 'http://example.com/feeds/objecttypes/Objecttype-2/',
              'description': 'Objecttype 2',
              'htmlUrl': 'http://example.com/objecttypes/Objecttype-2/',
              'ObjecttypeId': 2, 'parentId': 0,
              'ObjecttypeName': 'Objecttype 2',
              'ObjecttypeDescription': ''}])
        self.objecttypes[1].parent = self.objecttypes[0]
        self.objecttypes[1].description = 'Objecttype 2 description'
        self.objecttypes[1].save()
        self.assertEquals(
            self.server.metaWeblog.getObjecttypes('apikey',
                                                 'webmaster', 'password'),
            [{'rssUrl': 'http://example.com/feeds/objecttypes/Objecttype-1/',
              'description': 'Objecttype 1',
              'htmlUrl': 'http://example.com/objecttypes/Objecttype-1/',
              'ObjecttypeId': 1, 'parentId': 0,
              'ObjecttypeName': 'Objecttype 1',
              'ObjecttypeDescription': ''},
             {'rssUrl':
              'http://example.com/feeds/objecttypes/Objecttype-1/Objecttype-2/',
              'description': 'Objecttype 2',
              'htmlUrl':
              'http://example.com/objecttypes/Objecttype-1/Objecttype-2/',
              'ObjecttypeId': 2, 'parentId': 1,
              'ObjecttypeName': 'Objecttype 2',
              'ObjecttypeDescription': 'Objecttype 2 description'}])

    def test_new_Objecttype(self):
        Objecttype_struct = {'name': 'Objecttype 3', 'slug': 'Objecttype-3',
                           'description': 'Objecttype 3 description',
                           'parent_id': self.objecttypes[0].pk}
        self.assertRaises(Fault, self.server.wp.newObjecttype,
                          1, 'contributor', 'password', Objecttype_struct)
        self.assertEquals(Objecttype.objects.count(), 2)
        new_Objecttype_id = self.server.wp.newObjecttype(
            1, 'webmaster', 'password', Objecttype_struct)
        self.assertEquals(Objecttype.objects.count(), 3)
        Objecttype = Objecttype.objects.get(pk=new_Objecttype_id)
        self.assertEquals(Objecttype.title, 'Objecttype 3')
        self.assertEquals(Objecttype.description, 'Objecttype 3 description')
        self.assertEquals(Objecttype.slug, 'Objecttype-3')
        self.assertEquals(Objecttype.parent.pk, 1)

    def test_get_recent_posts(self):
        self.assertRaises(Fault, self.server.metaWeblog.getRecentPosts,
                          1, 'contributor', 'password', 10)
        self.assertEquals(len(self.server.metaWeblog.getRecentPosts(
            1, 'webmaster', 'password', 10)), 2)

    def test_delete_post(self):
        self.assertRaises(Fault, self.server.blogger.deletePost,
                          'apikey', 1, 'contributor', 'password', 'publish')
        self.assertEquals(Gbobject.objects.count(), 2)
        self.assertTrue(
            self.server.blogger.deletePost(
            'apikey', self.gbobject_1.pk, 'webmaster', 'password', 'publish'))
        self.assertEquals(Gbobject.objects.count(), 1)

    def test_get_post(self):
        self.assertRaises(Fault, self.server.metaWeblog.getPost,
                          1, 'contributor', 'password')
        post = self.server.metaWeblog.getPost(
            self.gbobject_1.pk, 'webmaster', 'password')
        self.assertEquals(post['title'], self.gbobject_1.title)
        self.assertEquals(post['description'], '<p>My content 1</p>')
        self.assertEquals(post['objecttypes'], ['Objecttype 1', 'Objecttype 2'])
        self.assertEquals(post['dateCreated'].value, '2010-01-01T00:00:00')
        self.assertEquals(post['link'],
                          'http://example.com/2010/01/01/my-gbobject-1/')
        self.assertEquals(post['permaLink'],
                          'http://example.com/2010/01/01/my-gbobject-1/')
        self.assertEquals(post['postid'], self.gbobject_1.pk)
        self.assertEquals(post['userid'], 'webmaster')
        self.assertEquals(post['mt_excerpt'], '')
        self.assertEquals(post['mt_allow_comments'], 1)
        self.assertEquals(post['mt_allow_pings'], 1)
        self.assertEquals(post['mt_keywords'], self.gbobject_1.tags)
        self.assertEquals(post['wp_author'], 'webmaster')
        self.assertEquals(post['wp_author_id'], self.webmaster.pk)
        self.assertEquals(post['wp_author_display_name'], 'webmaster')
        self.assertEquals(post['wp_password'], '')
        self.assertEquals(post['wp_slug'], self.gbobject_1.slug)

    def test_new_post(self):
        post = post_structure(self.gbobject_2, self.site)
        self.assertRaises(Fault, self.server.metaWeblog.newPost,
                          1, 'contributor', 'password', post, 1)
        self.assertEquals(Gbobject.objects.count(), 2)
        self.assertEquals(Gbobject.published.count(), 1)
        self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 1)
        self.assertEquals(Gbobject.objects.count(), 3)
        self.assertEquals(Gbobject.published.count(), 2)
        del post['dateCreated']
        post['wp_author_id'] = self.contributor.pk
        self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 0)
        self.assertEquals(Gbobject.objects.count(), 4)
        self.assertEquals(Gbobject.published.count(), 2)

    def test_edit_post(self):
        post = post_structure(self.gbobject_2, self.site)
        self.assertRaises(Fault, self.server.metaWeblog.editPost,
                          1, 'contributor', 'password', post, 1)
        new_post_id = self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 0)

        gbobject = Gbobject.objects.get(pk=new_post_id)
        self.assertEquals(gbobject.title, self.gbobject_2.title)
        self.assertEquals(gbobject.content, self.gbobject_2.html_content)
        self.assertEquals(gbobject.excerpt, self.gbobject_2.excerpt)
        self.assertEquals(gbobject.slug, self.gbobject_2.slug)
        self.assertEquals(gbobject.status, DRAFT)
        self.assertEquals(gbobject.password, self.gbobject_2.password)
        self.assertEquals(gbobject.comment_enabled, True)
        self.assertEquals(gbobject.pingback_enabled, True)
        self.assertEquals(gbobject.objecttypes.count(), 1)
        self.assertEquals(gbobject.authors.count(), 1)
        self.assertEquals(gbobject.authors.all()[0], self.webmaster)
        self.assertEquals(gbobject.creation_date, self.gbobject_2.creation_date)

        gbobject.title = 'Title edited'
        gbobject.creation_date = datetime(2000, 1, 1)
        post = post_structure(gbobject, self.site)
        post['objecttypes'] = ''
        post['description'] = 'Content edited'
        post['mt_excerpt'] = 'Content edited'
        post['wp_slug'] = 'slug-edited'
        post['wp_password'] = 'password'
        post['mt_allow_comments'] = 2
        post['mt_allow_pings'] = 0

        response = self.server.metaWeblog.editPost(
            new_post_id, 'webmaster', 'password', post, 1)
        self.assertEquals(response, True)
        gbobject = Gbobject.objects.get(pk=new_post_id)
        self.assertEquals(gbobject.title, post['title'])
        self.assertEquals(gbobject.content, post['description'])
        self.assertEquals(gbobject.excerpt, post['mt_excerpt'])
        self.assertEquals(gbobject.slug, 'slug-edited')
        self.assertEquals(gbobject.status, PUBLISHED)
        self.assertEquals(gbobject.password, 'password')
        self.assertEquals(gbobject.comment_enabled, False)
        self.assertEquals(gbobject.pingback_enabled, False)
        self.assertEquals(gbobject.objecttypes.count(), 0)
        self.assertEquals(gbobject.creation_date, datetime(2000, 1, 1))

        del post['dateCreated']
        post['wp_author_id'] = self.contributor.pk

        response = self.server.metaWeblog.editPost(
            new_post_id, 'webmaster', 'password', post, 1)
        gbobject = Gbobject.objects.get(pk=new_post_id)
        self.assertEquals(gbobject.authors.count(), 1)
        self.assertEquals(gbobject.authors.all()[0], self.contributor)
        self.assertEquals(gbobject.creation_date, datetime(2000, 1, 1))

    def test_new_media_object(self):
        file_ = TemporaryFile()
        file_.write('My test content')
        file_.seek(0)
        media = {'name': 'objectapp_test_file.txt',
                 'type': 'text/plain',
                 'bits': Binary(file_.read())}
        file_.close()

        self.assertRaises(Fault, self.server.metaWeblog.newMediaObject,
                          1, 'contributor', 'password', media)
        new_media = self.server.metaWeblog.newMediaObject(
            1, 'webmaster', 'password', media)
        self.assertTrue('/objectapp_test_file' in new_media['url'])
        default_storage.delete('/'.join([
            UPLOAD_TO, new_media['url'].split('/')[-1]]))
