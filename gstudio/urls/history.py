"""Urls for Gstudio forms"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.history',
                       url(r'^viewhistory/(?P<ssid>\d+)/(?P<version_no>\d+)/$', 'history',
                           name='gstudio_history'),
		       url(r'^compare_history/(?P<ssid>\d+)/$','compare_history'),
		       url(r'^merge/(?P<ssid1>\d+)/(?P<ssid2>\d+)/$','merge_version'),
		       url(r'^revert/$','revert_version'),)
