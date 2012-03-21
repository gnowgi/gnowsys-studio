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
"""Test cases for Gstudio's moderator"""
from django.core import mail
from django.test import TestCase
from django.contrib import comments
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from gstudio.models import Nodetype
from gstudio.managers import PUBLISHED
from gstudio.moderator import NodetypeCommentModerator


class NodetypeCommentModeratorTestCase(TestCase):
    """Test cases for the moderator"""

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.nodetype_ct_id = ContentType.objects.get_for_model(Nodetype).pk

        params = {'title': 'My test nodetype',
                  'content': 'My test nodetype',
                  'slug': 'my-test-nodetype',
                  'status': PUBLISHED}
        self.nodetype = Nodetype.objects.create(**params)
        self.nodetype.sites.add(self.site)
        self.nodetype.authors.add(self.author)

    def test_email(self):
        comment = comments.get_model().objects.create(
            comment='My Comment', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        self.assertEquals(len(mail.outbox), 0)
        moderator = NodetypeCommentModerator(Nodetype)
        moderator.email_reply = False
        moderator.email_authors = False
        moderator.mail_comment_notification_recipients = []
        moderator.email(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 0)
        moderator.email_reply = True
        moderator.email_authors = True
        moderator.mail_comment_notification_recipients = ['admin@example.com']
        moderator.email(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 1)

    def test_do_email_notification(self):
        comment = comments.get_model().objects.create(
            comment='My Comment', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        self.assertEquals(len(mail.outbox), 0)
        moderator = NodetypeCommentModerator(Nodetype)
        moderator.mail_comment_notification_recipients = ['admin@example.com']
        moderator.do_email_notification(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 1)

    def test_do_email_authors(self):
        comment = comments.get_model().objects.create(
            comment='My Comment', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        self.assertEquals(len(mail.outbox), 0)
        moderator = NodetypeCommentModerator(Nodetype)
        moderator.email_authors = True
        moderator.mail_comment_notification_recipients = ['admin@example.com']
        moderator.do_email_authors(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 0)
        moderator.mail_comment_notification_recipients = []
        moderator.do_email_authors(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 1)

    def test_do_email_reply(self):
        comment = comments.get_model().objects.create(
            comment='My Comment 1', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        moderator = NodetypeCommentModerator(Nodetype)
        moderator.email_notification_reply = True
        moderator.mail_comment_notification_recipients = ['admin@example.com']
        moderator.do_email_reply(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 0)

        comment = comments.get_model().objects.create(
            comment='My Comment 2', user_email='user_1@example.com',
            content_object=self.nodetype, is_public=True, site=self.site)
        moderator.do_email_reply(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 0)

        comment = comments.get_model().objects.create(
            comment='My Comment 3', user_email='user_2@example.com',
            content_object=self.nodetype, is_public=True, site=self.site)
        moderator.do_email_reply(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].bcc, [u'user_1@example.com'])

        comment = comments.get_model().objects.create(
            comment='My Comment 4', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        moderator.do_email_reply(comment, self.nodetype, 'request')
        self.assertEquals(len(mail.outbox), 2)
        self.assertEquals(mail.outbox[1].bcc, [u'user_1@example.com',
                                               u'user_2@example.com'])

    def test_moderate(self):
        comment = comments.get_model().objects.create(
            comment='My Comment', user=self.author, is_public=True,
            content_object=self.nodetype, site=self.site)
        moderator = NodetypeCommentModerator(Nodetype)
        moderator.auto_moderate_comments = True
        moderator.spam_checker_backends = ()
        self.assertEquals(moderator.moderate(comment, self.nodetype, 'request'),
                          True)
        moderator.auto_moderate_comments = False
        self.assertEquals(moderator.moderate(comment, self.nodetype, 'request'),
                          False)
        self.assertEquals(comments.get_model().objects.filter(
            flags__flag='spam').count(), 0)
        moderator.spam_checker_backends = (
            'gstudio.spam_checker.backends.all_is_spam',)
        self.assertEquals(moderator.moderate(comment, self.nodetype, 'request'),
                          True)
        self.assertEquals(comments.get_model().objects.filter(
            flags__flag='spam').count(), 1)
