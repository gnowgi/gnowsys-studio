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



from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from gstudio.methods import *
from tagging.models import Tag, TaggedItem

def collection(request,objecttypeTitle):
	objectList = [] 
	if objecttypeTitle:
	    objecttypeTitle = objecttypeTitle.lower()
	    if objecttypeTitle in ["audio","document","interactive"]:
		tag = Tag.objects.filter(name = objecttypeTitle+" collection")
		if tag :
		      	tag = Tag.objects.get(name = objecttypeTitle+" collection")
			for eachTagItem in tag.items.all():
				if eachTagItem.object : 
					objectList.append(eachTagItem.object)
			vars=RequestContext(request,{'objecttype':objecttypeTitle.title(),'objectList':objectList})					
			template="gstudio/collection.html"
			return render_to_response(template, vars)		
            	else:
            		raise Http404		
            else:
            	raise Http404

	else:
            raise Http404



