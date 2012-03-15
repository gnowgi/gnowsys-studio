
# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Urls for Gstudio forms"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.add',
                       url(r'^metatype/$', 'addmetatype',
                           name='gstudio_add_meatype'),
                       url(r'^objecttype/$', 'addobjecttype',
                           name='gstudio_add_objecttype'),

		       url(r'^attributetype/$', 'addattributetype',
                           name='gstudio_add_attributetype'),
		       
                       url(r'^relationtype/$', 'addrelationtype',
                           name='gstudio_add_relationtype'),	
		       url(r'^systemtype/$', 'addsystemtype',
                           name='gstudio_add_systemtype'),
		       url(r'^processtype/$', 'addprocesstype',
                           name='gstudio_add_systemtype'),	
		       url(r'^attribute/$', 'addattribute',
                           name='gstudio_add_attribute'),	
		       url(r'^relation/$', 'addrelation',
                           name='gstudio_add_relation'),	
		       url(r'^complement/$', 'addcomplement',
                           name='gstudio_add_complement'),
		       url(r'^intersection/$', 'addintersection',
                           name='gstudio_add_intersection'),	
		       url(r'^union/$', 'addunion',
                           name='gstudio_add_union'),	

	



                       )
