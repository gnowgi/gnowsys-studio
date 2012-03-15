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



"""
Admin ui common utilities.
"""

# PYTHON IMPORTS
import types
import warnings
from fnmatch import fnmatch

# DJANGO IMPORTS
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module


def _get_dashboard_cls(dashboard_cls, context):
    if type(dashboard_cls) is types.DictType:
        curr_url = context.get('request').META['PATH_INFO']
        for key in dashboard_cls:
            admin_site_mod, admin_site_inst = key.rsplit('.', 1)
            admin_site_mod = import_module(admin_site_mod)
            admin_site = getattr(admin_site_mod, admin_site_inst)
            admin_url = reverse('%s:index' % admin_site.name)
            if curr_url.startswith(admin_url):
                mod, inst = dashboard_cls[key].rsplit('.', 1)
                mod = import_module(mod)
                return getattr(mod, inst)
    else:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)
    raise ValueError('Dashboard matching "%s" not found' % dashboard_cls)


def get_index_dashboard(context):
    """
    Returns the admin dashboard defined in settings (or the default one).
    """
    
    return _get_dashboard_cls(getattr(
        settings,
        'GRAPPELLI_INDEX_DASHBOARD',
        'grappelli.dashboard.dashboards.DefaultIndexDashboard'
    ), context)()


def get_admin_site(context=None, request=None):
    dashboard_cls = getattr(
        settings,
        'GRAPPELLI_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultIndexDashboard'
    )
    
    if type(dashboard_cls) is types.DictType:
        if context:
            request = context.get('request')
        curr_url = request.META['PATH_INFO']
        for key in dashboard_cls:
            mod, inst = key.rsplit('.', 1)
            mod = import_module(mod)
            admin_site = getattr(mod, inst)
            admin_url = reverse('%s:index' % admin_site.name)
            if curr_url.startswith(admin_url):
                return admin_site
    else:
        return admin.site
    raise ValueError('Admin site matching "%s" not found' % dashboard_cls)


def get_admin_site_name(context):
    return get_admin_site(context).name


def get_avail_models(request):
    """ Returns (model, perm,) for all models user can possibly see """
    items = []
    admin_site = get_admin_site(request=request)
    
    for model, model_admin in admin_site._registry.items():
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        items.append((model, perms,))
    return items


def filter_models(request, models, exclude):
    """
    Returns (model, perm,) for all models that match models/exclude patterns
    and are visible by current user.
    """
    items = get_avail_models(request)
    included = []
    full_name = lambda model: '%s.%s' % (model.__module__, model.__name__)
    
    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.
    
    if len(models) == 0:
        included = items
    else:
        for pattern in models:
            pattern_items = []
            for item in items:
                model, perms = item
                if fnmatch(full_name(model), pattern) and item not in included:
                    pattern_items.append(item)
            pattern_items.sort(key=lambda x:x[0]._meta.verbose_name_plural)
            included.extend(pattern_items)
    
    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                result.remove(item)
    return result


class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the
    AppListMenuItem (to honor the DRY concept).
    """
    
    def _visible_models(self, request):
        
        included = self.models[:]
        excluded = self.exclude[:]
        if not self.models and not self.exclude:
            included = ["*"]
        return filter_models(request, included, excluded)
    
    def _get_admin_app_list_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:app_list' % get_admin_site_name(context),
                       args=(app_label,))
    
    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))
    
    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                         app_label,
                                         model.__name__.lower()))


