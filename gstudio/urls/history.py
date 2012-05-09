"""Urls for Gstudio forms"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.history',
                       url(r'^viewhistory/(?P<ssid>\d+)/$', 'history',
                           name='gstudio_history'),
		       url(r'^showhistory/$','showHistory'),)
