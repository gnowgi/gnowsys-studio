
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


"""Urls for the Gstudio nodetypes"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from gstudio.models import Nodetype
from gstudio.settings import PAGINATION
from gstudio.settings import ALLOW_EMPTY
from gstudio.settings import ALLOW_FUTURE

urlpatterns = patterns(
    'gstudio.views.graphs',
    url(r'^graph_json/(?P<node_id>\d+)$','graph_json', name='graph_json_d3'), 
    url(r'^version_graph_json/(?P<ssid>\d+)$','version_graph_json', name='version_graph_d3'), 
    url(r'^graph/(?P<node_id>\d+)$','force_graph', name='force_graph_d3'),  
    url(r'^graph_label/(?P<node_id>\d+)/(?P<key>[-\w]+)/$','graph_label', name='graph_label'),
    )
