from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
#from objectapp.views import testview

urlpatterns = patterns('objectapp.views.dynamicAT',                       
                        url(r'^dynamicattr/$','dynamic_view',
                           name = 'objectapp_dynamic_view'),
                       url(r'^save/(\w.+)/$','dynamic_save', 
                           name='objectapp_dynamic_save'),
                       # url(r'^dynamicOT/(\w.+)/$','dynamic_objecttype', 
                       #     name='objectapp_dynamic_objecttype'),
                       )
