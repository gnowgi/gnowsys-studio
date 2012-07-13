
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
rlist={}
import os
from settings import PY_SCRIPT_OBJECTAPP

def AjaxAddContentOrg(request):
    iden = request.GET["id"]
    content = request.GET["contentorg"]
    nid = NID.objects.get(id = iden)
    refobj = nid.ref
    refobj.content_org = content
    refobj.save()
    return HttpResponse("sucess")


def AjaxCreateFile(request):
    iden = request.GET["id"]
    # newtitle = request.GET["title"]
    orgcontent = request.GET["content_org"]
    myfile = open('/tmp/file.org', 'w')
    myfile.write(orgcontent)
    myfile.close()
    myfile = open('/tmp/file.org', 'r')
    myfile.readline()
    myfile = open('/tmp/file.org', 'a')
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:t toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile.write("\n#+TITLE: ")
    myfile = open('/tmp/file.org', 'r')
    return HttpResponse("test sucess")

def AjaxCreateHtml(request):
    stdout = os.popen()
    output = stdout.read()
    return HttpResponse(output)

def AjaxAddContent(request):
    iden = request.GET["id"]
    nid = NID.objects.get(id = iden)
    refobj = nid.ref
    data = open("/tmp/file.html")
    data1 = data.readlines()
    data2 = data1[67:]
    newdata=""
    for line in data2:
        newdata+= line.strip()
        refobj.content= newdata
        refobj.save()
    return HttpResponse(refobj.content)
             
          
                
                
                

            



	
	
	
	
