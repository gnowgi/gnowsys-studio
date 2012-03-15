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



"""Sitemaps for Gstudio"""
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from tagging.models import TaggedItem

from gstudio.models import Nodetype
from gstudio.models import Author
from gstudio.models import Metatype
from gstudio.managers import tags_published


class NodetypeSitemap(Sitemap):
    """Sitemap for nodetypes"""
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        """Return published nodetypes"""
        return Nodetype.published.all()

    def lastmod(self, obj):
        """Return last modification of a nodetype"""
        return obj.last_update


class MetatypeSitemap(Sitemap):
    """Sitemap for metatypes"""
    changefreq = 'monthly'

    def cache(self, metatypes):
        """Cache categorie's nodetypes percent on total nodetypes"""
        len_nodetypes = float(Nodetype.published.count())
        self.cache_metatypes = {}
        for cat in metatypes:
            if len_nodetypes:
                self.cache_metatypes[cat.pk] = cat.nodetypes_published(
                    ).count() / len_nodetypes
            else:
                self.cache_metatypes[cat.pk] = 0.0

    def items(self):
        """Return all metatypes with coeff"""
        metatypes = Metatype.objects.all()
        self.cache(metatypes)
        return metatypes

    def lastmod(self, obj):
        """Return last modification of a metatype"""
        nodetypes = obj.nodetypes_published()
        if not nodetypes:
            return None
        return nodetypes[0].creation_date

    def priority(self, obj):
        """Compute priority with cached coeffs"""
        priority = 0.5 + self.cache_metatypes[obj.pk]
        if priority > 1.0:
            priority = 1.0
        return '%.1f' % priority


class AuthorSitemap(Sitemap):
    """Sitemap for authors"""
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        """Return published authors"""
        return Author.published.all()

    def lastmod(self, obj):
        """Return last modification of an author"""
        nodetypes = obj.nodetypes_published()
        if not nodetypes:
            return None
        return nodetypes[0].creation_date

    def location(self, obj):
        """Return url of an author"""
        return reverse('gstudio_author_detail', args=[obj.username])


class TagSitemap(Sitemap):
    """Sitemap for tags"""
    changefreq = 'monthly'

    def cache(self, tags):
        """Cache tag's nodetypes percent on total nodetypes"""
        len_nodetypes = float(Nodetype.published.count())
        self.cache_tags = {}
        for tag in tags:
            nodetypes = TaggedItem.objects.get_by_model(
                Nodetype.published.all(), tag)
            self.cache_tags[tag.pk] = (nodetypes, nodetypes.count() / len_nodetypes)

    def items(self):
        """Return all tags with coeff"""
        tags = tags_published()
        self.cache(tags)
        return tags

    def lastmod(self, obj):
        """Return last modification of a tag"""
        nodetypes = self.cache_tags[obj.pk][0]
        return nodetypes[0].creation_date

    def priority(self, obj):
        """Compute priority with cached coeffs"""
        priority = 0.5 + self.cache_tags[obj.pk][1]
        if priority > 1.0:
            priority = 1.0
        return '%.1f' % priority

    def location(self, obj):
        """Return url of a tag"""
        return reverse('gstudio_tag_detail', args=[obj.name])
