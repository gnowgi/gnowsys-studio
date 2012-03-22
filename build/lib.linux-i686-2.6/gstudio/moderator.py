
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


"""Moderator of Gstudio comments"""
from django.conf import settings
from django.template import Context
from django.template import loader
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.moderation import CommentModerator

from gstudio.settings import PROTOCOL
from gstudio.settings import MAIL_COMMENT_REPLY
from gstudio.settings import MAIL_COMMENT_AUTHORS
from gstudio.settings import AUTO_MODERATE_COMMENTS
from gstudio.settings import AUTO_CLOSE_COMMENTS_AFTER
from gstudio.settings import MAIL_COMMENT_NOTIFICATION_RECIPIENTS
from gstudio.settings import SPAM_CHECKER_BACKENDS
from gstudio.spam_checker import check_is_spam

class NodetypeCommentModerator(CommentModerator):
    """Moderate the comment of Nodes"""
    email_reply = MAIL_COMMENT_REPLY
    email_authors = MAIL_COMMENT_AUTHORS
    enable_field = 'comment_enabled'
    auto_close_field = 'start_publication'
    close_after = AUTO_CLOSE_COMMENTS_AFTER
    spam_checker_backends = SPAM_CHECKER_BACKENDS
    auto_moderate_comments = AUTO_MODERATE_COMMENTS
    mail_comment_notification_recipients = MAIL_COMMENT_NOTIFICATION_RECIPIENTS

    def email(self, comment, content_object, request):
        if comment.is_public:
            current_language = get_language()
            try:
                activate(settings.LANGUAGE_CODE)
                if self.mail_comment_notification_recipients:
                    self.do_email_notification(comment, content_object,
                                               request)
                if self.email_authors:
                    self.do_email_authors(comment, content_object,
                                          request)
                if self.email_reply:
                    self.do_email_reply(comment, content_object, request)
            finally:
                activate(current_language)

    def do_email_notification(self, comment, content_object, request):
        """Send email notification of a new comment to site staff when email
        notifications have been requested."""
        site = Site.objects.get_current()
        template = loader.get_template(
            'comments/comment_notification_email.txt')
        context = Context({'comment': comment, 'site': site,
                           'protocol': PROTOCOL,
                           'content_object': content_object})
        subject = _('[%(site)s] New comment posted on "%(title)s"') % \
                  {'site': site.name,
                   'title': content_object.title}
        message = template.render(context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  self.mail_comment_notification_recipients,
                  fail_silently=not settings.DEBUG)

    def do_email_authors(self, comment, content_object, request):
        """Send email notification of a new comment to the authors of the
        nodetype when email notifications have been requested."""
        exclude_list = self.mail_comment_notification_recipients
        recipient_list = set([author.email
                              for author in content_object.authors.all()]) ^ \
                              set(exclude_list)

        if recipient_list:
            site = Site.objects.get_current()
            template = loader.get_template(
                'comments/comment_authors_email.txt')
            context = Context({'comment': comment, 'site': site,
                               'protocol': PROTOCOL,
                               'content_object': content_object})
            subject = _('[%(site)s] New comment posted on "%(title)s"') % \
                      {'site': site.name,
                       'title': content_object.title}
            message = template.render(context)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      recipient_list, fail_silently=not settings.DEBUG)

    def do_email_reply(self, comment, content_object, request):
        """Send email notification of a new comment to the authors of
        the previous comments when email notifications have been requested."""
        exclude_list = self.mail_comment_notification_recipients + \
                       [author.email
                        for author in content_object.authors.all()] + \
                       [comment.userinfo['email']]
        recipient_list = set([comment.userinfo['email']
                              for comment in content_object.comments
                              if comment.userinfo['email']]) ^ \
                              set(exclude_list)

        if recipient_list:
            site = Site.objects.get_current()
            template = loader.get_template('comments/comment_reply_email.txt')
            context = Context({'comment': comment, 'site': site,
                               'protocol': PROTOCOL,
                               'content_object': content_object})
            subject = _('[%(site)s] New comment posted on "%(title)s"') % \
                      {'site': site.name,
                       'title': content_object.title}
            message = template.render(context)
            mail = EmailMessage(subject, message,
                                settings.DEFAULT_FROM_EMAIL,
                                bcc=recipient_list)
            mail.send(fail_silently=not settings.DEBUG)

    def moderate(self, comment, content_object, request):
        """Determine whether a given comment on a given object should be
        allowed to show up immediately, or should be marked non-public
        and await approval."""
        if self.auto_moderate_comments:
            return True

        if check_is_spam(comment, content_object, request,
                         self.spam_checker_backends):
            comment.save()
            user = comment.content_object.authors.all()[0]
            comment.flags.create(user=user, flag='spam')
            return True

        return False
