
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


from django.http import HttpResponse
import json
from gstudio.models import *
from objectapp.models import *

def AjaxAttribute(request):
    iden = request.GET["id"]
    attr = Attributetype.objects.get(id=iden)
    subjecttype = attr.subjecttype
    returndict = {}

    for each in Objecttype.objects.all():
        if attr.subjecttype.id == each.id:
            for member in each.get_members:
                returndict[member.id] = member.title
    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json")
    
                
                
                

            



	
	
	
	
