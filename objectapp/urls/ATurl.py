from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns


urlpatterns = patterns('objectapp.views.dynamicAT',                       
                       url(r'^save/(\w.+)/(\w.+)/$','dynamic_save', 
                           name='objectapp_dynamic_save'),
                       )
