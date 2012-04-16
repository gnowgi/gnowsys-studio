from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
#from objectapp.views import testview

urlpatterns = patterns('objectapp.views.dynamicRT',                       
                       url(r'^displayRT/(\w.+)/$','context_RT',
                           name='objectapp_context_view'),               
                       url(r'^displaymem/(\w+)/(\w+)/$','context_member',
                           name='objectapp_context_display'),
                       url(r'^save/(\w+)/(\w+)/(\w+)/$','context_save',
                           name='objectapp_context_save'),
                       )

