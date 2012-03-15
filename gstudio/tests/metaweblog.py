
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


s# Copyright (c) 2011,  2012 Free Software Foundation

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
"""Test cases for Gstudio's MetaWeblog API"""
from xmlrpclib import Binary
from xmlrpclib import Fault
from xmlrpclib import ServerProxy
from datetime import datetime
from tempfile import TemporaryFile

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage

from gstudio.models import Nodetype
from gstudio.models import Metatype
from gstudio.managers import DRAFT
from gstudio.managers import PUBLISHED
from gstudio.settings import UPLOAD_TO
from gstudio.xmlrpc.metaweblog import authenticate
from gstudio.xmlrpc.metaweblog import post_structure
from gstudio.tests.utils import TestTransport


class MetaWeblogTestCase(TestCase):
    """Test cases for MetaWeblog"""
    urls = 'gstudio.tests.urls'

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
        self.metatypes = [
            Metatype.objects.create(title='Metatype 1',
                                    slug='metatype-1'),
            Metatype.objects.create(title='Metatype 2',
                                    slug='metatype-2')]
        params = {'title': 'My nodetype 1', 'content': 'My content 1',
                  'tags': 'gstudio, test', 'slug': 'my-nodetype-1',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        self.nodetype_1 = Nodetype.objects.create(**params)
        self.nodetype_1.authors.add(self.webmaster)
        self.nodetype_1.metatypes.add(*self.metatypes)
        self.nodetype_1.sites.add(self.site)

        params = {'title': 'My nodetype 2', 'content': 'My content 2',
                  'creation_date': datetime(2010, 3, 15),
                  'tags': 'gstudio, test', 'slug': 'my-nodetype-2'}
        self.nodetype_2 = Nodetype.objects.create(**params)
        self.nodetype_2.authors.add(self.webmaster)
        self.nodetype_2.metatypes.add(self.metatypes[0])
        self.nodetype_2.sites.add(self.site)
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
                          'password', 'gstudio.change_nodetype')
        self.assertEquals(authenticate('webmaster', 'password'),
                          self.webmaster)
        self.assertEquals(authenticate('webmaster', 'password',
                                       'gstudio.change_nodetype'),
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

    def test_get_metatypes(self):
        self.assertRaises(Fault, self.server.metaWeblog.getMetatypes,
                          1, 'contributor', 'password')
        self.assertEquals(
            self.server.metaWeblog.getMetatypes('apikey',
                                                 'webmaster', 'password'),
            [{'rssUrl': 'http://example.com/feeds/metatypes/metatype-1/',
              'description': 'Metatype 1',
              'htmlUrl': 'http://example.com/metatypes/metatype-1/',
              'metatypeId': 1, 'parentId': 0,
              'metatypeName': 'Metatype 1',
              'metatypeDescription': ''},
             {'rssUrl': 'http://example.com/feeds/metatypes/metatype-2/',
              'description': 'Metatype 2',
              'htmlUrl': 'http://example.com/metatypes/metatype-2/',
              'metatypeId': 2, 'parentId': 0,
              'metatypeName': 'Metatype 2',
              'metatypeDescription': ''}])
        self.metatypes[1].parent = self.metatypes[0]
        self.metatypes[1].description = 'metatype 2 description'
        self.metatypes[1].save()
        self.assertEquals(
            self.server.metaWeblog.getMetatypes('apikey',
                                                 'webmaster', 'password'),
            [{'rssUrl': 'http://example.com/feeds/metatypes/metatype-1/',
              'description': 'Metatype 1',
              'htmlUrl': 'http://example.com/metatypes/metatype-1/',
              'metatypeId': 1, 'parentId': 0,
              'metatypeName': 'Metatype 1',
              'metatypeDescription': ''},
             {'rssUrl':
              'http://example.com/feeds/metatypes/metatype-1/metatype-2/',
              'description': 'Metatype 2',
              'htmlUrl':
              'http://example.com/metatypes/metatype-1/metatype-2/',
              'metatypeId': 2, 'parentId': 1,
              'metatypeName': 'Metatype 2',
              'metatypeDescription': 'metatype 2 description'}])

    def test_new_metatype(self):
        metatype_struct = {'name': 'Metatype 3', 'slug': 'metatype-3',
                           'description': 'Metatype 3 description',
                           'parent_id': self.metatypes[0].pk}
        self.assertRaises(Fault, self.server.wp.newMetatype,
                          1, 'contributor', 'password', metatype_struct)
        self.assertEquals(Metatype.objects.count(), 2)
        new_metatype_id = self.server.wp.newMetatype(
            1, 'webmaster', 'password', metatype_struct)
        self.assertEquals(Metatype.objects.count(), 3)
        metatype = Metatype.objects.get(pk=new_metatype_id)
        self.assertEquals(metatype.title, 'Metatype 3')
        self.assertEquals(metatype.description, 'Metatype 3 description')
        self.assertEquals(metatype.slug, 'metatype-3')
        self.assertEquals(metatype.parent.pk, 1)

    def test_get_recent_posts(self):
        self.assertRaises(Fault, self.server.metaWeblog.getRecentPosts,
                          1, 'contributor', 'password', 10)
        self.assertEquals(len(self.server.metaWeblog.getRecentPosts(
            1, 'webmaster', 'password', 10)), 2)

    def test_delete_post(self):
        self.assertRaises(Fault, self.server.blogger.deletePost,
                          'apikey', 1, 'contributor', 'password', 'publish')
        self.assertEquals(Nodetype.objects.count(), 2)
        self.assertTrue(
            self.server.blogger.deletePost(
            'apikey', self.nodetype_1.pk, 'webmaster', 'password', 'publish'))
        self.assertEquals(Nodetype.objects.count(), 1)

    def test_get_post(self):
        self.assertRaises(Fault, self.server.metaWeblog.getPost,
                          1, 'contributor', 'password')
        post = self.server.metaWeblog.getPost(
            self.nodetype_1.pk, 'webmaster', 'password')
        self.assertEquals(post['title'], self.nodetype_1.title)
        self.assertEquals(post['description'], '<p>My content 1</p>')
        self.assertEquals(post['metatypes'], ['Metatype 1', 'Metatype 2'])
        self.assertEquals(post['dateCreated'].value, '2010-01-01T00:00:00')
        self.assertEquals(post['link'],
                          'http://example.com/2010/01/01/my-nodetype-1/')
        self.assertEquals(post['permaLink'],
                          'http://example.com/2010/01/01/my-nodetype-1/')
        self.assertEquals(post['postid'], self.nodetype_1.pk)
        self.assertEquals(post['userid'], 'webmaster')
        self.assertEquals(post['mt_excerpt'], '')
        self.assertEquals(post['mt_allow_comments'], 1)
        self.assertEquals(post['mt_allow_pings'], 1)
        self.assertEquals(post['mt_keywords'], self.nodetype_1.tags)
        self.assertEquals(post['wp_author'], 'webmaster')
        self.assertEquals(post['wp_author_id'], self.webmaster.pk)
        self.assertEquals(post['wp_author_display_name'], 'webmaster')
        self.assertEquals(post['wp_password'], '')
        self.assertEquals(post['wp_slug'], self.nodetype_1.slug)

    def test_new_post(self):
        post = post_structure(self.nodetype_2, self.site)
        self.assertRaises(Fault, self.server.metaWeblog.newPost,
                          1, 'contributor', 'password', post, 1)
        self.assertEquals(Nodetype.objects.count(), 2)
        self.assertEquals(Nodetype.published.count(), 1)
        self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 1)
        self.assertEquals(Nodetype.objects.count(), 3)
        self.assertEquals(Nodetype.published.count(), 2)
        del post['dateCreated']
        post['wp_author_id'] = self.contributor.pk
        self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 0)
        self.assertEquals(Nodetype.objects.count(), 4)
        self.assertEquals(Nodetype.published.count(), 2)

    def test_edit_post(self):
        post = post_structure(self.nodetype_2, self.site)
        self.assertRaises(Fault, self.server.metaWeblog.editPost,
                          1, 'contributor', 'password', post, 1)
        new_post_id = self.server.metaWeblog.newPost(
            1, 'webmaster', 'password', post, 0)

        nodetype = Nodetype.objects.get(pk=new_post_id)
        self.assertEquals(nodetype.title, self.nodetype_2.title)
        self.assertEquals(nodetype.content, self.nodetype_2.html_content)
        self.assertEquals(nodetype.excerpt, self.nodetype_2.excerpt)
        self.assertEquals(nodetype.slug, self.nodetype_2.slug)
        self.assertEquals(nodetype.status, DRAFT)
        self.assertEquals(nodetype.password, self.nodetype_2.password)
        self.assertEquals(nodetype.comment_enabled, True)
        self.assertEquals(nodetype.pingback_enabled, True)
        self.assertEquals(nodetype.metatypes.count(), 1)
        self.assertEquals(nodetype.authors.count(), 1)
        self.assertEquals(nodetype.authors.all()[0], self.webmaster)
        self.assertEquals(nodetype.creation_date, self.nodetype_2.creation_date)

        nodetype.title = 'Title edited'
        nodetype.creation_date = datetime(2000, 1, 1)
        post = post_structure(nodetype, self.site)
        post['metatypes'] = ''
        post['description'] = 'Content edited'
        post['mt_excerpt'] = 'Content edited'
        post['wp_slug'] = 'slug-edited'
        post['wp_password'] = 'password'
        post['mt_allow_comments'] = 2
        post['mt_allow_pings'] = 0

        response = self.server.metaWeblog.editPost(
            new_post_id, 'webmaster', 'password', post, 1)
        self.assertEquals(response, True)
        nodetype = Nodetype.objects.get(pk=new_post_id)
        self.assertEquals(nodetype.title, post['title'])
        self.assertEquals(nodetype.content, post['description'])
        self.assertEquals(nodetype.excerpt, post['mt_excerpt'])
        self.assertEquals(nodetype.slug, 'slug-edited')
        self.assertEquals(nodetype.status, PUBLISHED)
        self.assertEquals(nodetype.password, 'password')
        self.assertEquals(nodetype.comment_enabled, False)
        self.assertEquals(nodetype.pingback_enabled, False)
        self.assertEquals(nodetype.metatypes.count(), 0)
        self.assertEquals(nodetype.creation_date, datetime(2000, 1, 1))

        del post['dateCreated']
        post['wp_author_id'] = self.contributor.pk

        response = self.server.metaWeblog.editPost(
            new_post_id, 'webmaster', 'password', post, 1)
        nodetype = Nodetype.objects.get(pk=new_post_id)
        self.assertEquals(nodetype.authors.count(), 1)
        self.assertEquals(nodetype.authors.all()[0], self.contributor)
        self.assertEquals(nodetype.creation_date, datetime(2000, 1, 1))

    def test_new_media_object(self):
        file_ = TemporaryFile()
        file_.write('My test content')
        file_.seek(0)
        media = {'name': 'gstudio_test_file.txt',
                 'type': 'text/plain',
                 'bits': Binary(file_.read())}
        file_.close()

        self.assertRaises(Fault, self.server.metaWeblog.newMediaObject,
                          1, 'contributor', 'password', media)
        new_media = self.server.metaWeblog.newMediaObject(
            1, 'webmaster', 'password', media)
        self.assertTrue('/gstudio_test_file' in new_media['url'])
        default_storage.delete('/'.join([
            UPLOAD_TO, new_media['url'].split('/')[-1]]))
