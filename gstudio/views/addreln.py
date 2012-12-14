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
from django.shortcuts import render_to_response
from django.template import RequestContext
from gstudio.models import Relation,Relationtype
from objectapp.models import System,Gbobject
from gstudio.models import NID
from django.template.loader import get_template
from django.template import Context


def addrelnform(request,meetob):
    title=""
    if request.method == 'POST' :
        title=request.POST.get("reln","")
        inverse =request.POST.get("obj","")
        slug=request.POST.get("slug","")

    if request.method == 'GET' :
        title=request.GET.get("reln","")
        inverse=request.GET.get("obj","")
        slug=request.GET.get("slug","")
    if title:
        ob=Relationtype()
        ob.title=title
        ob.inverse=inverse
        ob.slug=slug
        left_subjecttype=NID.objects.get(title='Page')
        left_applicable_nodetypes =unicode('OT')
        right_subjecttype=NID.objects.get(title='Page')
        right_applicable_nodetypes =unicode('OT')
        ob.left_subjecttype=left_subjecttype
        ob.left_applicable_nodetypes=left_applicable_nodetypes
        ob.right_subjecttype=right_subjecttype
        ob.right_applicable_nodetypes=right_applicable_nodetypes
        ob.save()

    variables = RequestContext(request,{'meetob':meetob})
    template = "gstudio/addrelnform.html"
    return render_to_response(template, variables)



def addreln(request,meetob):
    a=Relation()
    try:
        if request.method == 'GET' :
            relntype=request.GET['relnobj']
            obobj=request.GET['obobject']
        rt=Relationtype.objects.filter(title=relntype)
        a.left_subject=Gbobject.objects.get(id=meetob)
        obt=Gbobject.objects.filter(title=obobj)
        rt=Relationtype.objects.filter(title=relntype)
        if rt:
            a.relationtype=Relationtype.objects.get(title=relntype)
        if obt:
            obt=Gbobject.objects.get(title=obobj)
        a.right_subject=obt
        a.save()
        j=System.objects.get(id=meetob)
        p=j.get_view_url
        if not obobj:
                return HttpResponseRedirect(p)
        else:
                t = get_template('gstudio/addrelnform_refresh.html')
                html = t.render(Context({'meetobj':j}))
                return HttpResponse(html)
    except:
        t = get_template('gstudio/addrelnform_refresh.html')
        html = t.render(Context({'meetingobj':j}))
        return HttpResponse(html)
