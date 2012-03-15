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
Dashboard template tags, the following dashboard tags are available:
 * ``{% grp_render_dashboard %}``
 * ``{% grp_render_dashboard_module %}``

To load the dashboard tags: ``{% load grp_dashboard_tags %}``.
"""

import math

from django import template
from django.core.urlresolvers import reverse

from grappelli.dashboard.utils import get_admin_site_name, get_index_dashboard

register = template.Library()
tag_func = register.inclusion_tag('grappelli/dashboard/dummy.html', takes_context=True)


def grp_render_dashboard(context, location='index', dashboard=None):
    """
    Template tag that renders the dashboard, it takes two optional arguments:
    
    ``location``
        The location of the dashboard, it can be 'index' (for the admin index
        dashboard) or 'app_index' (for the app index dashboard), the default
        value is 'index'.
    
    ``dashboard``
        An instance of ``Dashboard``, if not given, the dashboard is retrieved
        with the ``get_index_dashboard`` or ``get_app_index_dashboard``
        functions, depending on the ``location`` argument.
    """
    if dashboard is None:
        dashboard = get_index_dashboard(context)
    
    dashboard.init_with_context(context)
    
    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
grp_render_dashboard = tag_func(grp_render_dashboard)


def grp_render_dashboard_module(context, module, index=None, subindex=None):
    """
    Template tag that renders a given dashboard module, it takes a
    ``DashboardModule`` instance as first parameter and an integer ``index`` as
    second parameter, that is the index of the module in the dashboard.
    """
    module.init_with_context(context)
    context.update({
        'template': module.template,
        'module': module,
        'index': index,
        'subindex': subindex,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
grp_render_dashboard_module = tag_func(grp_render_dashboard_module)


