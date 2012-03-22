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


"""Urls for the Objectapp gbobjects"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from objectapp.models import Gbobject
from objectapp.settings import PAGINATION
from objectapp.settings import ALLOW_EMPTY
from objectapp.settings import ALLOW_FUTURE

gbobject_conf_index = {'paginate_by': PAGINATION,
                    'template_name': 'objectapp/gbobject_archive.html'}

gbobject_conf = {'date_field': 'creation_date',
              'allow_empty': ALLOW_EMPTY,
              'allow_future': ALLOW_FUTURE,
              'month_format': '%m'}

gbobject_conf_year = gbobject_conf.copy()
gbobject_conf_year['make_object_list'] = True
del gbobject_conf_year['month_format']

gbobject_conf_detail = gbobject_conf.copy()
del gbobject_conf_detail['allow_empty']
gbobject_conf_detail['queryset'] = Gbobject.published.on_site()


urlpatterns = patterns(
    'objectapp.views.gbobjects',
    url(r'^$',
        'gbobject_index', gbobject_conf_index,
        name='objectapp_gbobject_archive_index'),
    url(r'^page/(?P<page>\d+)/$',
        'gbobject_index', gbobject_conf_index,
        name='objectapp_gbobject_archive_index_paginated'),
    url(r'^(?P<year>\d{4})/$',
        'gbobject_year', gbobject_conf_year,
        name='objectapp_gbobject_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'gbobject_month', gbobject_conf,
        name='objectapp_gbobject_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'gbobject_day', gbobject_conf,
        name='objectapp_gbobject_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'gbobject_detail', gbobject_conf_detail,
        name='objectapp_gbobject_detail'),
    url(r'^(?P<object_id>\d+)/$',
        'gbobject_shortlink',
        name='objectapp_gbobject_shortlink'),
    )
