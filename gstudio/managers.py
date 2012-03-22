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
"""Managers of gstudio"""
from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2


def tags_published():
    """Return the published tags"""
    from tagging.models import Tag
    from gstudio.models import Nodetype
    tags_nodetype_published = Tag.objects.usage_for_queryset(
        Nodetype.published.all())
    # Need to do that until the issue #44 of django-tagging is fixed
    return Tag.objects.filter(name__in=[t.name for t in tags_nodetype_published])


class AuthorPublishedManager(models.Manager):
    """Manager to retrieve published authors"""

    def get_query_set(self):
        """Return published authors"""
        now = datetime.now()
        return super(AuthorPublishedManager, self).get_query_set().filter(
            nodetypes__status=PUBLISHED,
            nodetypes__start_publication__lte=now,
            nodetypes__end_publication__gt=now,
            nodetypes__sites=Site.objects.get_current()
            ).distinct()

def nodes_published(queryset):

    """Return only the nodetypes published"""
    now = datetime.now()
    return queryset.filter(status=PUBLISHED,
                           start_publication__lte=now,
                           end_publication__gt=now,
                           sites=Site.objects.get_current())

class NodePublishedManager(models.Manager):
    """Manager to retrieve published nodes"""

    def get_query_set(self):
        """Return published nodes"""
        return nodes_published(
            super(NodePublishedManager, self).get_query_set())

    def on_site(self):
        """Return nodes published on current site"""
        return super(NodePublishedManager, self).get_query_set(
            ).filter(sites=Site.objects.get_current())

    def search(self, pattern):
        """Top level search method on nodes"""
        try:
            return self.advanced_search(pattern)
        except:
            return self.basic_search(pattern)

    def advanced_search(self, pattern):
        """Advanced search on nodes"""
        from gstudio.search import advanced_search
        return advanced_search(pattern)

    def basic_search(self, pattern):
        """Basic search on nodes"""
        lookup = None
        for pattern in pattern.split():
            query_part = models.Q(title__icontains=pattern)
            ''' models.Q(content__icontains=pattern) | \
                         models.Q(excerpt__icontains=pattern) | \ '''
            if lookup is None:
                lookup = query_part
            else:
                lookup |= query_part

        return self.get_query_set().filter(lookup)


def nodetypes_published(queryset):

    """Return only the nodetypes published"""
    now = datetime.now()
    return queryset.filter(status=PUBLISHED,
                           start_publication__lte=now,
                           end_publication__gt=now,
                           sites=Site.objects.get_current())


class NodetypePublishedManager(models.Manager):
    """Manager to retrieve published nodetypes"""

    def get_query_set(self):
        """Return published nodetypes"""
        return nodetypes_published(
            super(NodetypePublishedManager, self).get_query_set())

    def on_site(self):
        """Return nodetypes published on current site"""
        return super(NodetypePublishedManager, self).get_query_set(
            ).filter(sites=Site.objects.get_current())

    def search(self, pattern):
        """Top level search method on nodetypes"""
        try:
            return self.advanced_search(pattern)
        except:
            return self.basic_search(pattern)

    def advanced_search(self, pattern):
        """Advanced search on nodetypes"""
        from gstudio.search import advanced_search
        return advanced_search(pattern)

    def basic_search(self, pattern):
        """Basic search on nodetypes"""
        lookup = None
        for pattern in pattern.split():
            query_part = models.Q(content__icontains=pattern) | \
                         models.Q(excerpt__icontains=pattern) | \
                         models.Q(title__icontains=pattern)
            if lookup is None:
                lookup = query_part
            else:
                lookup |= query_part

        return self.get_query_set().filter(lookup)
