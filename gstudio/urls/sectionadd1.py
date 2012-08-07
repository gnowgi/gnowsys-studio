"""Url for Gstudio User Dashboard"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.sectionadd1',
                       url(r'(\d+)', 'sectionadd1',
                           name='gstudio_section'),

                       )
