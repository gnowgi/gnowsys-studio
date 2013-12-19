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
from tagging.models import Tag
import json

def refreshsearch(request):
    t = get_template('gstudio/puttagsearchrefresh.html')
    html = t.render(Context())
    return HttpResponse(html)

def puttagsearch(request):
    first=request.GET.get("first","")
    second=request.GET.get("second","")
    oprtn=request.GET.get("operation","")
   
    tag1=Tag.objects.filter(name=first)
    if tag1:
        tag1=Tag.objects.get(name=first)
        ft=tag1.name
    tag2=Tag.objects.filter(name=second)
    if tag2:
        tag2=Tag.objects.get(name=second)
        st=tag2.name
    fl=0
    if oprtn=="":
        if tag1 or tag2:
            fl=1
    lst={}
    flst={}
    if oprtn=="AND" or fl==1:
        if tag1:
            for each in Gbobject.objects.all():
                if ft in each.tags:
                    lst[each]=each.get_view_object_url
                    if not tag2:
                       flst=lst
        if tag2 and tag1:
            for each1 in lst:
                if st in each1.tags:
                    flst[each1]=each1.get_view_object_url
        else:
            if tag2:
                for each in Gbobject.objects.all():
                    if st in each.tags:
                        flst[each]=each.get_view_object_url
    if oprtn=="OR":
        if tag1:
            for each in Gbobject.objects.all():
                if ft in each.tags:
                    flst[each]=each.get_view_object_url
        if tag2:
            for each1 in Gbobject.objects.all():
                if st in each1.tags:
                    flst[each1]=each1.get_view_object_url
    variables = RequestContext(request,{'tags':flst,'tag1':tag1,'tag2':tag2})
    template = "gstudio/reftags.html"
    return render_to_response(template, variables)




def getrefreshrts(request):
    retrt={}
    listrts=[]
    for each in Relationtype.objects.all():
        s=each.title
        listrts.append(str(s))
    retrt['relns']=listrts
    jsonobject = json.dumps(retrt)
    return HttpResponse(jsonobject, "application/json")


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
#        rt=Relationtype.objects.filter(title=relntype)
        a.left_subject=Gbobject.objects.get(id=meetob)
        obt=Gbobject.objects.filter(id=obobj)
        rt=Relationtype.objects.filter(id=relntype)
        if rt:
            a.relationtype=Relationtype.objects.get(id=relntype)
        if obt:
            obt=Gbobject.objects.get(id=obobj)
        a.right_subject=obt
        a.save()
        j=System.objects.get(id=meetob)
        p=j.get_view_url
        if not obobj:
                return HttpResponseRedirect(p)
        else:
                t = get_template('gstudio/addrelnform_refresh.html')
                html = t.render(Context({'meetingob':j}))
                return HttpResponse(html)
    except:
        t = get_template('gstudio/addrelnform_refresh.html')
        html = t.render(Context({'meetingob':j}))
        return HttpResponse(html)


def deleteRelation(request,meetingob):
    if request.method == 'GET' :
        relation_ajax_id=request.GET['relation_ajax_id']

    relation = Relation.objects.filter(id=relation_ajax_id)
    if relation:
	relation.delete()

    j=System.objects.get(id=meetingob);
    t = get_template('gstudio/addrelnform_refresh.html')
    html = t.render(Context({'meetingob':j}))
    return HttpResponse(html)
