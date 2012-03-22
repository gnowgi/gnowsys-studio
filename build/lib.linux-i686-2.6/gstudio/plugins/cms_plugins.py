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



"""Plugins for CMS"""
import itertools

from django.conf import settings
from django.utils.translation import ugettext as _

from tagging.models import TaggedItem
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from gstudio.models import Nodetype
from gstudio.models import Author
from gstudio.managers import tags_published
from gstudio.plugins.models import RandomNodetypesPlugin
from gstudio.plugins.models import LatestNodetypesPlugin
from gstudio.plugins.models import SelectedNodetypesPlugin


class CMSLatestNodetypesPlugin(CMSPluginBase):
    """Django-cms plugin for the latest nodetypes filtered"""
    module = _('nodetypes')
    model = LatestNodetypesPlugin
    name = _('Latest nodetypes')
    render_template = 'gstudio/cms/nodetype_list.html'
    filter_horizontal = ['metatypes', 'authors', 'tags']
    fieldsets = (
        (None, {
            'fields': (
                'number_of_nodetypes',
                'template_to_render'
            )
        }),
        (_('Sorting'), {
            'fields': (
                'metatypes',
                'authors',
                'tags'
            ),
            'classes': (
                'collapse',
            )
        }),
        (_('Advanced'), {
            'fields': (
                'submetatypes',
            ),
        }),
    )

    text_enabled = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filtering manytomany field"""
        if db_field.name == 'authors':
            kwargs['queryset'] = Author.published.all()
        if db_field.name == 'tags':
            kwargs['queryset'] = tags_published()
        return super(CMSLatestNodetypesPlugin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        nodetypes = Nodetype.published.all()

        if instance.metatypes.count():
            cats = instance.metatypes.all()

            if instance.submetatypes:
                cats = itertools.chain(cats, *[c.get_descendants()
                                               for c in cats])

            nodetypes = nodetypes.filter(metatypes__in=cats)
        if instance.authors.count():
            nodetypes = nodetypes.filter(authors__in=instance.authors.all())
        if instance.tags.count():
            nodetypes = TaggedItem.objects.get_union_by_model(
                nodetypes, instance.tags.all())

        nodetypes = nodetypes.distinct()[:instance.number_of_nodetypes]
        context.update({'nodetypes': nodetypes,
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'gstudio/img/plugin.png'


class CMSSelectedNodetypesPlugin(CMSPluginBase):
    """Django-cms plugin for a selection of nodetypes"""
    module = _('nodetypes')
    model = SelectedNodetypesPlugin
    name = _('Selected nodetypes')
    render_template = 'gstudio/cms/nodetype_list.html'
    fields = ('nodetypes', 'template_to_render')
    filter_horizontal = ['nodetypes']
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'nodetypes': instance.nodetypes.all(),
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'gstudio/img/plugin.png'


class CMSRandomNodetypesPlugin(CMSPluginBase):
    """Django-cms plugin for random nodetypes"""
    module = _('nodetypes')
    model = RandomNodetypesPlugin
    name = _('Random node types')
    render_template = 'gstudio/cms/random_nodetypes.html'
    fields = ('number_of_nodetypes', 'template_to_render')
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update(
            {'number_of_nodetypes': instance.number_of_nodetypes,
             'template_to_render': str(instance.template_to_render) or
             'gstudio/tags/random_nodetypes.html'})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'gstudio/img/plugin.png'

plugin_pool.register_plugin(CMSLatestNodetypesPlugin)
plugin_pool.register_plugin(CMSSelectedNodetypesPlugin)
plugin_pool.register_plugin(CMSRandomNodetypesPlugin)
