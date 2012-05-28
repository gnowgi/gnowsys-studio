
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


"""Defaults urls for the Gstudio project"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    '',
    url(r'^tags/', include('gstudio.urls.tags',)),
    url(r'^feeds/', include('gstudio.urls.feeds')),
    url(r'^authors/', include('gstudio.urls.authors')),
    url(r'^metatypes/', include('gstudio.urls.metatypes')),
    url(r'^search/', include('gstudio.urls.search')),
    url(r'^sitemap/', include('gstudio.urls.sitemap')),
    url(r'^trackback/', include('gstudio.urls.trackback')),
    url(r'^discussions/', include('gstudio.urls.discussions')),
    url(r'^add/', include('gstudio.urls.add')),
    url(r'^ajax/', include('gstudio.urls.ajaxurls')),
    url(r'^display/',include('gstudio.urls.history')),
    url(r'^graphs/', include('gstudio.urls.graphs')),
    url(r'^userdashboard/', include('gstudio.urls.dashboard')),
    url(r'^', include('gstudio.urls.quick_nodetype')),
    url(r'^', include('gstudio.urls.capabilities')),
    url(r'^', include('gstudio.urls.nodetypes')),
    )
