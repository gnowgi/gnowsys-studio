g# Copyright (c) 2011,  2012 Free Software Foundation

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
"""Plugins for CMS"""
import itertools

from django.conf import settings
from django.utils.translation import ugettext as _

from tagging.models import TaggedItem
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from objectapp.models import Gbobject
from objectapp.models import Author
from objectapp.managers import tags_published
from objectapp.plugins.models import RandomGbobjectsPlugin
from objectapp.plugins.models import LatestGbobjectsPlugin
from objectapp.plugins.models import SelectedGbobjectsPlugin


class CMSLatestGbobjectsPlugin(CMSPluginBase):
    """Django-cms plugin for the latest gbobjects filtered"""
    module = _('gbobjects')
    model = LatestGbobjectsPlugin
    name = _('Latest gbobjects')
    render_template = 'objectapp/cms/gbobject_list.html'
    filter_horizontal = ['objecttypes', 'authors', 'tags']
    fieldsets = (
        (None, {
            'fields': (
                'number_of_gbobjects',
                'template_to_render'
            )
        }),
        (_('Sorting'), {
            'fields': (
                'objecttypes',
                'authors',
                'tags'
            ),
            'classes': (
                'collapse',
            )
        }),
        (_('Advanced'), {
            'fields': (
                'subobjecttypes',
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
        return super(CMSLatestGbobjectsPlugin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        gbobjects = Gbobject.published.all()

        if instance.objecttypes.count():
            cats = instance.objecttypes.all()

            if instance.subobjecttypes:
                cats = itertools.chain(cats, *[c.get_descendants()
                                               for c in cats])

            gbobjects = gbobjects.filter(objecttypes__in=cats)
        if instance.authors.count():
            gbobjects = gbobjects.filter(authors__in=instance.authors.all())
        if instance.tags.count():
            gbobjects = TaggedItem.objects.get_union_by_model(
                gbobjects, instance.tags.all())

        gbobjects = gbobjects.distinct()[:instance.number_of_gbobjects]
        context.update({'gbobjects': gbobjects,
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'objectapp/img/plugin.png'


class CMSSelectedGbobjectsPlugin(CMSPluginBase):
    """Django-cms plugin for a selection of gbobjects"""
    module = _('gbobjects')
    model = SelectedGbobjectsPlugin
    name = _('Selected gbobjects')
    render_template = 'objectapp/cms/gbobject_list.html'
    fields = ('gbobjects', 'template_to_render')
    filter_horizontal = ['gbobjects']
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'gbobjects': instance.gbobjects.all(),
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'objectapp/img/plugin.png'


class CMSRandomGbobjectsPlugin(CMSPluginBase):
    """Django-cms plugin for random gbobjects"""
    module = _('gbobjects')
    model = RandomGbobjectsPlugin
    name = _('Random gbobjects')
    render_template = 'objectapp/cms/random_gbobjects.html'
    fields = ('number_of_gbobjects', 'template_to_render')
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update(
            {'number_of_gbobjects': instance.number_of_gbobjects,
             'template_to_render': str(instance.template_to_render) or
             'objectapp/tags/random_gbobjects.html'})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'objectapp/img/plugin.png'

plugin_pool.register_plugin(CMSLatestGbobjectsPlugin)
plugin_pool.register_plugin(CMSSelectedGbobjectsPlugin)
plugin_pool.register_plugin(CMSRandomGbobjectsPlugin)
