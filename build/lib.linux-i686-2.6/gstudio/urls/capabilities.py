
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


"""Urls for the gstudio capabilities"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
from django.contrib.sites.models import Site

from gstudio.settings import PROTOCOL
from gstudio.settings import COPYRIGHT
from gstudio.settings import FEEDS_FORMAT

extra_context = {'protocol': PROTOCOL,
                 'site': Site.objects.get_current()}

extra_context_opensearch = extra_context.copy()
extra_context_opensearch.update({'copyright': COPYRIGHT,
                                 'feeds_format': FEEDS_FORMAT})

urlpatterns = patterns('django.views.generic.simple',
                       url(r'^rsd.xml$', 'direct_to_template',
                           {'template': 'gstudio/rsd.xml',
                            'mimetype': 'application/rsd+xml',
                            'extra_context': extra_context},
                           name='gstudio_rsd'),
                       url(r'^wlwmanifest.xml$', 'direct_to_template',
                           {'template': 'gstudio/wlwmanifest.xml',
                            'mimetype': 'application/wlwmanifest+xml',
                            'extra_context': extra_context},
                           name='gstudio_wlwmanifest'),
                       url(r'^opensearch.xml$', 'direct_to_template',
                           {'template': 'gstudio/opensearch.xml',
                            'mimetype':
                            'application/opensearchdescription+xml',
                            'extra_context': extra_context_opensearch},
                           name='gstudio_opensearch'),
                       )
