"""Admin of Gstudio CMS Plugins"""
from django.contrib import admin
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.plugin_rendering import render_placeholder
from cms.admin.placeholderadmin import PlaceholderAdmin

from gstudio.models import Nodetype
from gstudio.admin.nodetype import NodetypeAdmin
from gstudio.settings import NODETYPE_BASE_MODEL


class NodetypePlaceholderAdmin(PlaceholderAdmin, NodetypeAdmin):
    """NodetypePlaceholder Admin"""
    fieldsets = ((None, {'fields': ('title', 'image', 'status')}),
                 (_('Content'), {'fields': ('content_placeholder',),
                                 'classes': ('plugin-holder',
                                             'plugin-holder-nopage')}),
                 (_('Options'), {'fields': ('featured', 'excerpt', 'template',
                                            'related', 'authors',
                                            'creation_date',
                                            'start_publication',
                                            'end_publication'),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Privacy'), {'fields': ('password', 'login_required',),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Discussion'), {'fields': ('comment_enabled',
                                               'pingback_enabled')}),
                 (_('Publication'), {'fields': ('sites', 'metatypes',
                                                'tags', 'slug')}))

    def save_model(self, request, nodetype, form, change):
        """Fill the content field with the interpretation
        of the placeholder"""
        context = RequestContext(request)
        nodetype.content = render_placeholder(nodetype.content_placeholder, context)
        super(NodetypePlaceholderAdmin, self).save_model(
            request, nodetype, form, change)


if NODETYPE_BASE_MODEL == 'gstudio.plugins.placeholder.NodetypePlaceholder':
    admin.site.unregister(Nodetype)
    admin.site.register(Nodetype, NodetypePlaceholderAdmin)
