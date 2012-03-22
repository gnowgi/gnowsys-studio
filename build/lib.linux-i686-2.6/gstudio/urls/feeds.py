
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


"""Urls for the Gstudio feeds"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from gstudio.feeds import LatestNodetypes
from gstudio.feeds import NodetypeDiscussions
from gstudio.feeds import NodetypeComments
from gstudio.feeds import NodetypeTrackbacks
from gstudio.feeds import NodetypePingbacks
from gstudio.feeds import SearchNodetypes
from gstudio.feeds import TagNodetypes
from gstudio.feeds import MetatypeNodetypes
from gstudio.feeds import AuthorNodetypes


urlpatterns = patterns(
    '',
    url(r'^latest/$',
        LatestNodetypes(),
        name='gstudio_nodetype_latest_feed'),
    url(r'^search/$',
        SearchNodetypes(),
        name='gstudio_nodetype_search_feed'),
    url(r'^tags/(?P<slug>[- \w]+)/$',
        TagNodetypes(),
        name='gstudio_tag_feed'),
    url(r'^authors/(?P<username>[.+-@\w]+)/$',
        AuthorNodetypes(),
        name='gstudio_author_feed'),
    url(r'^metatypes/(?P<path>[-\/\w]+)/$',
        MetatypeNodetypes(),
        name='gstudio_metatype_feed'),
    url(r'^discussions/(?P<year>\d{4})/(?P<month>\d{2})/' \
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        NodetypeDiscussions(),
        name='gstudio_nodetype_discussion_feed'),
    url(r'^comments/(?P<year>\d{4})/(?P<month>\d{2})/' \
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        NodetypeComments(),
        name='gstudio_nodetype_comment_feed'),
    url(r'^pingbacks/(?P<year>\d{4})/(?P<month>\d{2})/' \
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        NodetypePingbacks(),
        name='gstudio_nodetype_pingback_feed'),
    url(r'^trackbacks/(?P<year>\d{4})/(?P<month>\d{2})/' \
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        NodetypeTrackbacks(),
        name='gstudio_nodetype_trackback_feed'),
    )
