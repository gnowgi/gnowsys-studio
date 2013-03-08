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
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *
import datetime
def pageadd(request):
    errors = []
    collection= None
    pageId = ""
    test1=get_pdrawer()
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a title.')
        # if not request.POST.get('org1', ''):
        #      errors.append('Enter a page.')
        if not errors:
            title=request.POST['subject']
       #     content=request.POST['page']
            content_org=unicode(request.POST['org1'])
            idusr=request.POST['idusr']
            list1=request.POST['list1']
            collection = request.POST.get("collection",'')
            orgcontent=request.POST['orgcontent']
            usr = request.POST.get("usr",'')
            editable= request.POST.get("edit","")
           # print content_org,"content"
            if collection:
                collection=True
                
            else:
                collection=False
            
            if editable=='edited':
                
                #if id_no:
                edit_section(idusr,content_org,usr)
               # elif id_no1:
                #    edit_section(id_no1,rep)

	    pageId = create_wikipage(title,int(idusr),orgcontent,usr,collection,list1)
            
            if pageId :
                return HttpResponseRedirect('/gstudio/page/gnowsys-page/'+ str(pageId))
    variables = RequestContext(request,{'errors' : errors, 'pageId' : pageId,'test1': test1})
    template = "gstudio/NewPage.html"
    return render_to_response(template, variables)
