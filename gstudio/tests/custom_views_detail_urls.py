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


"""Test urls for the gstudio project"""
from functools import wraps

from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from gstudio.views.tags import tag_detail
from gstudio.views.authors import author_detail
from gstudio.views.metatypes import metatype_detail
from gstudio.tests.urls import urlpatterns as test_urlpatterns


def call_with_template_and_extra_context(
    view, template_name='gstudio/nodetype_list.html',
    extra_context={'extra': 'context'}):

    @wraps(view)
    def wrapper(*args, **kwargs):
        return view(template_name=template_name,
                    extra_context=extra_context,
                    *args, **kwargs)

    return wrapper

custom_tag_detail = call_with_template_and_extra_context(tag_detail)
custom_author_detail = call_with_template_and_extra_context(author_detail)
custom_metatype_detail = call_with_template_and_extra_context(metatype_detail)


urlpatterns = patterns(
    '',
    url(r'^authors/(?P<username>[.+-@\w]+)/$',
        custom_author_detail, name='gstudio_author_detail'),
    url(r'^authors/(?P<username>[.+-@\w]+)/page/(?P<page>\d+)/$',
        custom_author_detail, name='gstudio_author_detail_paginated'),
    url(r'^metatypes/(?P<path>[-\/\w]+)/page/(?P<page>\d+)/$',
        custom_metatype_detail, name='gstudio_metatype_detail_paginated'),
    url(r'^metatypes/(?P<path>[-\/\w]+)/$',
        custom_metatype_detail, name='gstudio_metatype_detail'),
    url(r'^tags/(?P<tag>[- \w]+)/$',
        custom_tag_detail, name='gstudio_tag_detail'),
    url(r'^tags/(?P<tag>[- \w]+)/page/(?P<page>\d+)/$',
        custom_tag_detail, name='gstudio_tag_detail_paginated'),
    ) + test_urlpatterns
