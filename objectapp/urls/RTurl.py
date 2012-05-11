from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns


urlpatterns = patterns('objectapp.views.dynamicRT',                                            
                       url(r'^displaymem/(\w.+)/(\w.+)/$','context_member',
                           name='objectapp_context_display'),

                       url(r'^save/(\w.+)/(\w.+)/(\w.+)/$','context_save',
                           name='objectapp_context_save'),
                       )

