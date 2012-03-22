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


"""Blogger to Gstudio command module
Based on Elijah Rutschman's code"""
import sys
from getpass import getpass
from datetime import datetime
from optparse import make_option

from django.utils.encoding import smart_str
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments import get_model as get_comment_model

from gstudio import __version__
from gstudio.models import Nodetype
from gstudio.models import Metatype
from gstudio.managers import DRAFT, PUBLISHED

gdata_service = None
Comment = get_comment_model()


class Command(NoArgsCommand):
    """Command object for importing a Blogger blog
    into Gstudio via Google's gdata API."""
    help = 'Import a Blogger blog into Gstudio.'

    option_list = NoArgsCommand.option_list + (
        make_option('--blogger-username', dest='blogger_username', default='',
                    help='The username to login to Blogger with'),
        make_option('--metatype-title', dest='metatype_title', default='',
                    help='The Gstudio metatype to import Blogger posts to'),
        make_option('--blogger-blog-id', dest='blogger_blog_id', default='',
                    help='The id of the Blogger blog to import'),
        make_option('--author', dest='author', default='',
                    help='All imported nodetypes belong to specified author')
        )

    SITE = Site.objects.get_current()

    def __init__(self):
        """Init the Command and add custom styles"""
        super(Command, self).__init__()
        self.style.TITLE = self.style.SQL_FIELD
        self.style.STEP = self.style.SQL_COLTYPE
        self.style.ITEM = self.style.HTTP_INFO

    def write_out(self, message, verbosity_level=1):
        """Convenient method for outputing"""
        if self.verbosity and self.verbosity >= verbosity_level:
            sys.stdout.write(smart_str(message))
            sys.stdout.flush()

    def handle_noargs(self, **options):
        global gdata_service
        try:
            from gdata import service
            gdata_service = service
        except ImportError:
            raise CommandError('You need to install the gdata ' \
                               'module to run this command.')

        self.verbosity = int(options.get('verbosity', 1))
        self.blogger_username = options.get('blogger_username')
        self.metatype_title = options.get('metatype_title')
        self.blogger_blog_id = options.get('blogger_blog_id')

        self.write_out(self.style.TITLE(
            'Starting migration from Blogger to Gstudio %s\n' % __version__))

        if not self.blogger_username:
            self.blogger_username = raw_input('Blogger username: ')
            if not self.blogger_username:
                raise CommandError('Invalid Blogger username')

        self.blogger_password = getpass('Blogger password: ')
        try:
            self.blogger_manager = BloggerManager(self.blogger_username,
                                                  self.blogger_password)
        except gdata_service.BadAuthentication:
            raise CommandError('Incorrect Blogger username or password')

        default_author = options.get('author')
        if default_author:
            try:
                self.default_author = User.objects.get(username=default_author)
            except User.DoesNotExist:
                raise CommandError(
                    'Invalid Gstudio username for default author "%s"' % \
                    default_author)
        else:
            self.default_author = User.objects.all()[0]

        if not self.blogger_blog_id:
            self.select_blog_id()

        if not self.metatype_title:
            self.metatype_title = raw_input(
                'Metatype title for imported nodetypes: ')
            if not self.metatype_title:
                raise CommandError('Invalid metatype title')

        self.import_posts()

    def select_blog_id(self):
        self.write_out(self.style.STEP('- Requesting your weblogs\n'))
        blogs_list = [blog for blog in self.blogger_manager.get_blogs()]
        while True:
            i = 0
            blogs = {}
            for blog in blogs_list:
                i += 1
                blogs[i] = blog
                self.write_out('%s. %s (%s)' % (i, blog.title.text,
                                                get_blog_id(blog)))
            try:
                blog_index = int(raw_input('\nSelect a blog to import: '))
                blog = blogs[blog_index]
                break
            except (ValueError, KeyError):
                self.write_out(self.style.ERROR(
                    'Please enter a valid blog number\n'))

        self.blogger_blog_id = get_blog_id(blog)

    def get_metatype(self):
        metatype, created = Metatype.objects.get_or_create(
            title=self.metatype_title,
            slug=slugify(self.metatype_title)[:255])

        if created:
            metatype.save()

        return metatype

    def import_posts(self):
        metatype = self.get_metatype()
        self.write_out(self.style.STEP('- Importing nodetypes\n'))
        for post in self.blogger_manager.get_posts(self.blogger_blog_id):
            creation_date = convert_blogger_timestamp(post.published.text)
            status = DRAFT if is_draft(post) else PUBLISHED
            title = post.title.text or ''
            content = post.content.text or ''
            slug = slugify(post.title.text or get_post_id(post))[:255]
            try:
                nodetype = Nodetype.objects.get(creation_date=creation_date,
                                          slug=slug)
                output = self.style.NOTICE('> Skipped %s (already migrated)\n'
                    % nodetype)
            except Nodetype.DoesNotExist:
                nodetype = Nodetype(status=status, title=title, content=content,
                              creation_date=creation_date, slug=slug)
                if self.default_author:
                    nodetype.author = self.default_author
                nodetype.tags = ','.join([slugify(cat.term) for
                                       cat in post.metatype])
                nodetype.last_update = convert_blogger_timestamp(
                    post.updated.text)
                nodetype.save()
                nodetype.sites.add(self.SITE)
                nodetype.metatypes.add(metatype)
                nodetype.authors.add(self.default_author)
                try:
                    self.import_comments(nodetype, post)
                except gdata_service.RequestError:
                    # comments not available for this post
                    pass
                output = self.style.ITEM('> Migrated %s + %s comments\n'
                    % (nodetype.title, len(Comment.objects.for_model(nodetype))))

            self.write_out(output)

    def import_comments(self, nodetype, post):
        blog_id = self.blogger_blog_id
        post_id = get_post_id(post)
        comments = self.blogger_manager.get_comments(blog_id, post_id)
        nodetype_content_type = ContentType.objects.get_for_model(Nodetype)

        for comment in comments:
            submit_date = convert_blogger_timestamp(comment.published.text)
            content = comment.content.text

            author = comment.author[0]
            if author:
                user_name = author.name.text if author.name else ''
                user_email = author.email.text if author.email else ''
                user_url = author.uri.text if author.uri else ''

            else:
                user_name = ''
                user_email = ''
                user_url = ''

            com, created = Comment.objects.get_or_create(
                content_type=nodetype_content_type,
                object_pk=nodetype.pk,
                comment=content,
                submit_date=submit_date,
                site=self.SITE,
                user_name=user_name,
                user_email=user_email,
                user_url=user_url)

            if created:
                com.save()


def convert_blogger_timestamp(timestamp):
    # parse 2010-12-19T15:37:00.003
    date_string = timestamp[:-6]
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')


def is_draft(post):
    if post.control:
        if post.control.draft:
            if post.control.draft.text == 'yes':
                return True
    return False


def get_blog_id(blog):
    return blog.GetSelfLink().href.split('/')[-1]


def get_post_id(post):
    return post.GetSelfLink().href.split('/')[-1]


class BloggerManager(object):

    def __init__(self, username, password):
        self.service = gdata_service.GDataService(username, password)
        self.service.server = 'www.blogger.com'
        self.service.service = 'blogger'
        self.service.ProgrammaticLogin()

    def get_blogs(self):
        feed = self.service.Get('/feeds/default/blogs')
        for blog in feed.nodetype:
            yield blog

    def get_posts(self, blog_id):
        feed = self.service.Get('/feeds/%s/posts/default' % blog_id)
        for post in feed.nodetype:
            yield post

    def get_comments(self, blog_id, post_id):
        feed = self.service.Get('/feeds/%s/%s/comments/default' % \
                                (blog_id, post_id))
        for comment in feed.nodetype:
            yield comment
