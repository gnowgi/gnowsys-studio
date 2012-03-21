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
"""XML-RPC methods of Objectapp Pingback"""
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError
from urlparse import urlsplit

from django.contrib import comments
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.core.urlresolvers import Resolver404
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from objectapp.models import Gbobject
from objectapp.settings import PINGBACK_CONTENT_LENGTH
from BeautifulSoup import BeautifulSoup
from django_xmlrpc.decorators import xmlrpc_func

UNDEFINED_ERROR = 0
SOURCE_DOES_NOT_EXIST = 16
SOURCE_DOES_NOT_LINK = 17
TARGET_DOES_NOT_EXIST = 32
TARGET_IS_NOT_PINGABLE = 33
PINGBACK_ALREADY_REGISTERED = 48


def generate_pingback_content(soup, target, max_length, trunc_char='...'):
    """Generate a description text for the pingback"""
    link = soup.find('a', href=target)

    content = strip_tags(unicode(link.findParent()))
    index = content.index(link.string)

    if len(content) > max_length:
        middle = max_length / 2
        start = index - middle
        end = index + middle

        if start <= 0:
            end -= start
            extract = content[0:end]
        else:
            extract = '%s%s' % (trunc_char, content[start:end])

        if end < len(content):
            extract += trunc_char
        return extract

    return content


@xmlrpc_func(returns='string', args=['string', 'string'])
def pingback_ping(source, target):
    """pingback.ping(sourceURI, targetURI) => 'Pingback message'

    Notifies the server that a link has been added to sourceURI,
    pointing to targetURI.

    See: http://hixie.ch/specs/pingback/pingback-1.0"""
    try:
        if source == target:
            return UNDEFINED_ERROR

        site = Site.objects.get_current()
        try:
            document = ''.join(urlopen(source).readlines())
        except (HTTPError, URLError):
            return SOURCE_DOES_NOT_EXIST

        if not target in document:
            return SOURCE_DOES_NOT_LINK

        scheme, netloc, path, query, fragment = urlsplit(target)
        if netloc != site.domain:
            return TARGET_DOES_NOT_EXIST

        try:
            view, args, kwargs = resolve(path)
        except Resolver404:
            return TARGET_DOES_NOT_EXIST

        try:
            gbobject = Gbobject.published.get(
                slug=kwargs['slug'],
                creation_date__year=kwargs['year'],
                creation_date__month=kwargs['month'],
                creation_date__day=kwargs['day'])
            if not gbobject.pingback_enabled:
                return TARGET_IS_NOT_PINGABLE
        except (KeyError, Gbobject.DoesNotExist):
            return TARGET_IS_NOT_PINGABLE

        soup = BeautifulSoup(document)
        title = soup.find('title')
        title = title and strip_tags(title) or _('No title')
        description = generate_pingback_content(soup, target,
                                                PINGBACK_CONTENT_LENGTH)

        comment, created = comments.get_model().objects.get_or_create(
            content_type=ContentType.objects.get_for_model(Gbobject),
            object_pk=gbobject.pk, user_url=source, site=site,
            defaults={'comment': description, 'user_name': title})
        if created:
            user = gbobject.authors.all()[0]
            comment.flags.create(user=user, flag='pingback')
            return 'Pingback from %s to %s registered.' % (source, target)
        return PINGBACK_ALREADY_REGISTERED
    except:
        return UNDEFINED_ERROR


@xmlrpc_func(returns='string[]', args=['string'])
def pingback_extensions_get_pingbacks(target):
    """pingback.extensions.getPingbacks(url) => '[url, url, ...]'

    Returns an array of URLs that link to the specified url.

    See: http://www.aquarionics.com/misc/archives/blogite/0198.html"""
    site = Site.objects.get_current()

    scheme, netloc, path, query, fragment = urlsplit(target)
    if netloc != site.domain:
        return TARGET_DOES_NOT_EXIST

    try:
        view, args, kwargs = resolve(path)
    except Resolver404:
        return TARGET_DOES_NOT_EXIST

    try:
        gbobject = Gbobject.published.get(
            slug=kwargs['slug'],
            creation_date__year=kwargs['year'],
            creation_date__month=kwargs['month'],
            creation_date__day=kwargs['day'])
    except (KeyError, Gbobject.DoesNotExist):
        return TARGET_IS_NOT_PINGABLE

    return [pingback.user_url for pingback in gbobject.pingbacks]
