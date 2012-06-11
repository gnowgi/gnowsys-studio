
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
from settings import PYSCRIPT_URL_GSTUDIO

def AjaxAttribute(request):
    iden = request.GET["id"]
    attr = Attributetype.objects.get(id=iden)
    subjecttype = attr.subjecttype
    returndict = {}

    for ots in Objecttype.objects.all():
        if attr.subjecttype.id ==ots.id:
            for member in ots.get_members:
                returndict[member.id] = member.title
            childrenots = ots.get_children()
        
            if childrenots:
                for eachchild in childrenots:
                    returndict[eachchild.id] = eachchild.title    
                    membs=eachchild.ref.get_members
                    for each in membs:
                        returndict[each.id] = each.title

    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json")

def AjaxRelationleft(request):
    global rlist
    rlist={}
    idenid=request.GET["id"]
    rts=Relationtype.objects.filter(id=idenid)
    for each in rts:
        subj=str(each.left_subjecttype.title)
        appltype=each.left_applicable_nodetypes
        fnname= "selectionlist_"+appltype+"('"+subj+"')" 
        
        exec fnname
    
    returndict=rlist  
    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json") 

def AjaxRelationright(request):
    global rlist
    rlist={}
    idenid = request.GET["id"]
    rts=Relationtype.objects.filter(id=idenid)
    print "rtsright",rts
    for each in rts:
       subj=str(each.right_subjecttype.title)
       appltype=each.right_applicable_nodetypes
       fnname="selectionlist_"+appltype+"('"+subj+"')"
       
       exec fnname
    
    returndict=rlist
    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json") 
                
def additemdict(sdict,itemtoadd):
    fl=0
    for key,value in sdict.items():
        if value==itemtoadd:
            fl=1
    if fl==0:
        sdict[itemtoadd.id]=itemtoadd.title
    return sdict                 
def selectionlist_OT(obj):
    # Basically the filter must filter out the OT, their members, the children and members of the children

    global rlist
    # Return all OTs and members of subtypes of OT
    obs=Objecttype.objects.filter(title=obj)
    #	Get all members of subtypes of each OT
    if obs: 
        # Add the items first
        for each in obs:
            rlist=additemdict(rlist,each)
        obs=Objecttype.objects.get(title=obj)
        # Add the objects first
        # for each in obs:
        #     rlist = additemdict(rlist,each)
        memobs=obs.get_members
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        # Add children first
        for each in childrenots:
            rlist=additemdict(rlist,each)
        # Add memebers of each child
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)


        
    return rlist 
            
def selectionlist_MT(obj):
    global rlist
    # Return all MTs and members of subtypes of MT
    obs=Metatype.objects.filter(title=obj)
    #Get all members of subtypes of each MT
    if obs:
    	obs=Metatype.objects.get(title=obj)
	memobs=obs.member_types.all()
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
               childrenots=each.ref.get_members
               if childrenots:
    		   for eachchild in childrenots:
        	        rlist=additemdict(rlist,eachchild)
      
    return rlist
def selectionlist_NT(obj):
    global rlist
    # Return all NTs and members of subtypes of NT
    obs=Nodetype.objects.filter(title=obj)
    #Get all members of subtypes of each NT
    if obs: 
        obs=Nodetype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_AT(obj):
    global rlist
    # Return all ATs and members of subtypes of AT
    obs=Attributetype.objects.filter(title=obj)
    #Get all members of subtypes of each AT
    if obs:
        obs=Attributetype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_ST(obj):
    global rlist
    # Return all STs and members of subtypes of ST
    obs=Systemtype.objects.filter(title=obj)
    #Get all members of subtypes of each ST
    if obs:
        obs=Systemtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_PT(obj):
    global rlist
    # Return all PTs and members of subtypes of PT
    obs=Processtype.objects.filter(title=obj)
    #Get all members of subtypes of each PT
    if obs:
        obs=Processtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_RT(obj):
    global rlist
    # Return all RTs and members of subtypes of RT
    obs=Relationtype.objects.filter(title=obj)
    #Get all members of subtypes of each RT
    if obs:
        obs=Relationtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist

def selectionlist_RN(obj):
    global rlist
    
    obs=Relation.objects.filter(title=obj)
    #Get all members of RN
    if obs:
        obs=Relation.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_AS(obj):
    global rlist
    
    obs=AttributeSpecification.objects.filter(title=obj)
    #Get all members of AS
    if obs:
        obs=AttributeSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_NS(obj):
    global rlist
    
    obs=NodeSpecification.objects.filter(title=obj)
    #Get all members of NS
    if obs:
        obs=NodeSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_SY(obj):
    global rlist
    
    obs=System.objects.filter(title=obj)
    #Get all members of SY
    if obs:
        obs=System.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_RS(obj):
    global rlist
    # Return all members of RS
    obs=RelationSpecification.objects.filter(title=obj)
    if obs:
        obs=RelationSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_ND(obj):
    global rlist
    
    obs=Node.objects.filter(title=obj)
    #Get all members of ND
    if obs:
        obs=Node.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_ED(obj):
    global rlist
    
    obs=Edge.objects.filter(title=obj)
    #Get all members of ED
    if obs:
        obs=Edge.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_IN(obj):
    global rlist
    
    obs=Intersection.objects.filter(title=obj)
    #Get all members of IN
    if obs:
        obs=Intersection.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_CP(obj):
    global rlist
    
    obs=Complement.objects.filter(title=obj)
    #Get all members of CP
    if obs:
        obs=Complement.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_UP(obj):
    global rlist
    
    obs=Objecttype.objects.all()
    #Get all members UP
    print 'obs=',obs
    for each in obs:
        childrenots=each.get_children()
        for eachchild in childrenots: 
            membs=eachchild.objecttypes.all()
def selectionlist_OB(obj):
    global rlist
    obs=Objecttype.objects.get(title=obj)
    #Get all members of OB
    for each in  obs.member_objects.all(): 
        rlist=additemdict(rlist,each)
    return rlist
    
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
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile = open('/tmp/file.org', 'r')
    
#   os.remove("/tmp/file.org")
    return HttpResponse("test sucess")

# def AjaxSetOption(request):
#     myfile = open('/tmp/file.org', 'a')
#     myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:t toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
#     myfile = open('/tmp/file.org', 'r')
#     return HttpResponse("set option")

def AjaxCreateHtml(request):
    stdout = os.popen(PYSCRIPT_URL_GSTUDIO)
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
        newdata += line.lstrip()
    refobj.content= newdata
    refobj.save()
    return HttpResponse(refobj.content)
                    
                
                

            



	
	
	
	
