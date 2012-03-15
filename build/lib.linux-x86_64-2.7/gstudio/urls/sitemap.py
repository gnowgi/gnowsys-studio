"""Urls for the Gstudio sitemap"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.sitemap',
                       url(r'^$', 'sitemap',
                           {'template': 'gstudio/sitemap.html'},
                           name='gstudio_sitemap'),
                       )
