"""Url for Gstudio User Dashboard"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.topicadd1',
                       url(r'(\d+)', 'topicadd1',
                           name='gstudio_meet'),

                       )
