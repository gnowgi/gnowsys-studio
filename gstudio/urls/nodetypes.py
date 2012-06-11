
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

nodetype_conf_index = {'paginate_by': PAGINATION,
                    'template_name': 'gstudio/nodetype_archive.html'}

nodetype_conf = {'date_field': 'creation_date',
                   'allow_empty': ALLOW_EMPTY,
                   'allow_future': ALLOW_FUTURE,
                   'month_format': '%m',
                   'queryset': Nodetype.tree.all()}

metatype_conf = {}

nodetype_conf_year = nodetype_conf.copy()
nodetype_conf_year['make_object_list'] = True
del nodetype_conf_year['month_format']

nodetype_conf_detail = nodetype_conf.copy()
del nodetype_conf_detail['allow_empty']
#nodetype_conf_detail['queryset'] = Nodetype.published.on_site()


urlpatterns = patterns(
    'gstudio.views.nodetypes',
    url(r'^$',
        'nodetype_index', nodetype_conf_index,
        name='gstudio_nodetype_archive_index'),
    url(r'^page/(?P<page>\d+)/$',
        'nodetype_index', nodetype_conf_index,
        name='gstudio_nodetype_archive_index_paginated'),
    url(r'^(?P<year>\d{4})/$',
        'nodetype_year', nodetype_conf_year,
        name='gstudio_nodetype_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'nodetype_month', nodetype_conf,
        name='gstudio_nodetype_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'nodetype_day', nodetype_conf,
        name='gstudio_nodetype_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'nodetype_detail', nodetype_conf_detail,
        name='gstudio_nodetype_detail'),
    url(r'^(?P<object_id>\d+)/$',
        'nodetype_shortlink',
        name='gstudio_nodetype_shortlink'),
    )
