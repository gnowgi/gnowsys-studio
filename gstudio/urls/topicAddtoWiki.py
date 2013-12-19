"""Url for Gstudio Page Dashboard"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.topicAddtoWiki',
                       url(r'(\d+)', 'topicAddtoWiki',name='gstudio_meet'),
                       )
