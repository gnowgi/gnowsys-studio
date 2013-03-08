

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
from django.utils.encoding import smart_str,smart_unicode
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from gstudio.methods import *
import json
import shutil
import codecs
from gstudio.models import *
from objectapp.models import *
rlist={}
import os
from settings import PYSCRIPT_URL_GSTUDIO
from demo.settings import FILE_URL,PYSCRIPT_URL_GSTUDIO,HTML_FILE_URL


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
    usr=str(request.user)
    iden = request.GET["id"]
    orgcontent = request.GET["content_org"]
    ext='.org'
    html='.html'
    myfile = open(os.path.join('/tmp/',usr+ext),'w')
    myfile.write(new_ob.content_org)
    myfile.close()
    myfile = open(os.path.join('/tmp/',usr+ext),'r')
    myfile.readline()
    myfile = open(os.path.join('/tmp/',usr+ext),'a')
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile.write("\n#+TITLE: ")
    myfile = open(os.path.join('/tmp/',usr+ext),'r')
    return HttpResponse("test sucess")

def AjaxCreateHtml(request):
    usr=str(request.user)
    ext='.org'
    stdout = os.popen("%s %s"%(PYSCRIPT_URL_GSTUDIO,usr+ext))
    output = stdout.read()
    return HttpResponse("sucess")

def AjaxAddContent(request):
    usr=str(request.user)
    html='.html'
    iden = request.GET["id"]
    nid = NID.objects.get(id = iden)
    refobj = nid.ref
    data = open(os.path.join('/tmp/',usr+html))
    data1 = data.readlines()
    data2 = data1[72:]
    data3 = data2[:-3]
    newdata=""
    for line in data3:
        newdata += line.lstrip()
    refobj.content= newdata
    refobj.save()
    return HttpResponse(refobj.content)

def AjaxAddDrawer(request):
    list1=request.GET["title"]
    wtitle=request.GET["wtitle"]
    sys=System.objects.get(id=wtitle)

    if list1 == "null":
	sys=System.objects.get(id=wtitle)
       
        sys.gbobject_set.clear()
            
	n_set=[]
        varobset=[]
        
    else:
        list1=list1+","
        list2=eval(list1)
        sys=System.objects.get(id=wtitle)
        sys.gbobject_set.clear()
        i=0
        n_set=[]
    
        while i<len(list2):
            objs=Gbobject.objects.get(id=list2[i])
            sys.gbobject_set.add(objs)
            n_set.append(list2[i])
            i=i+1
        var=sys.in_gbobject_set_of.__dict__['through']
        varobset=[]
        for each in var.objects.all():
            print sys.id,sys.title,each.system_id
            if each.system_id == sys.id:
                s=Gbobject.objects.get(id=each.gbobject_id)
                s1=s.title
                varobset.append(s)
    variables = RequestContext(request, {'sys':sys,'list':n_set,'objset':varobset})
    template = "metadashboard/newcollection.html"
    
    return render_to_response(template, variables)

def HtmlExport(request):
    ptitle=request.GET["ptitle"]
    set1=request.GET["title"]
    if set1 == "null":
        
        ptitle=System.objects.get(id=ptitle)
        s=ptitle.get_ssid.pop()	
        contorg=ptitle.content_org    #ptitle=eval(ptitle)
        content_org="* "+ptitle.title+"\n"+contorg+"\n"

    else:
	ptitle1=System.objects.get(id=ptitle)
	s=ptitle1.get_ssid.pop()
        
        set1=set1+","
        set2=eval(set1)
        
        s1=str(ptitle.title)
        varobset=get_gbobjects(ptitle)
        contorg=ptitle1.content_org    #ptitle=eval(ptitle)
        content_org="* "+ptitle1.title+"\n"+str(contorg)+"\n"
        set2=[]
        set2=ptitle1.gbobject_set.all()
        l=len(set2)
        i=0
        if l>0:
            while i<len(varobset):
                st=System.objects.get(id=varobset[i].id)
                stcontorg=st.content_org
                content_org += "** "+varobset[i].title+"\n"+stcontorg+"\n"
                if st.gbobject_set.exists():
                    gbset=get_gbobjects(st.id)
                    
                    
                    for each in gbset:
                        subst=System.objects.get(title=each.title)
                        substcontorg=subst.content_org
                        content_org += "*** "+"\n"+substcontorg+"\n"
                i+=1                
                  
                            
                
                #          if subst.gbobject_set.exists():
                #              subgbset=get_gbobjects(subst.id)
                #              for each in subgbset:
                #                  subtwost=System.objects.get(id=each.id)
                            
                #                  content_org += "**** "+str(each)+"\n"+each.content_org+"\n"
                            
                #                  if subtwost.gbobject_set.exists():
                #                      subtwogbset=get_gbobjects(subtwost.id)
                #                      for each in subtwogbset:
                #                          subthreest=System.objects.get(id=each.id)
                #                          content_org += "***** "+str(each)+"\n"+each.content_org+"\n"
                

                #                          if subthreest.gbobject_set.exists():
                #                              subthreegbset=get_gbobjects(subthreest.id)
                #                              for each in subthreegbset:
                #                                  subfourst=System.objects.get(id=each.id)
                #                                  content_org += "****** "+str(each)+"\n"+each.content_org+"\n"
                                            
                #                                  if subfourst.gbobject_set.exists():
                #                                      subfourgbset=get_gbobjects(subfourst.id)
                #                                      for each in subfourgbset:
                #                                          subfivest=System.objects.get(id=each.id)
                #                                          content_org += "******* "+str(each)+"\n"+each.content_org+"\n"
                                                    
                #                                          if subfivest.gbobject_set.exists():
                #                                              subfivegbset=get_gbobjects(subfivest.id)
                #                                              for each in subfivegbset:
                #                                                  subsixst=System.objects.get(id=each.id)
                #                                                  content_org += "******** "+str(each)+"\n"+each.content_org+"\n"
                                                            
                    
                # i+=1 
		
   
    fname=str(s)+"-download"
    ext=".org"
    myfile = open(os.path.join(FILE_URL,fname+ext),'w')
    content_org=content_org.encode("utf-8")
    myfile.write(content_org)
    myfile.close()

    myfile = open(os.path.join(FILE_URL,fname+ext),'r')
    rfile=myfile.readlines()
    scontent="".join(rfile)
    newcontent=scontent.replace("\r","")
    myfile = open(os.path.join(FILE_URL,fname+ext),'w')
    myfile.write(newcontent)

    myfile = open(os.path.join(FILE_URL,fname+ext),'a')
    myfile.write("\n  /All material is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License unless mentioned otherwise./ ")
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile.write("\n#+TITLE: ")
    myfile = open(os.path.join(FILE_URL,fname+ext),'r')
    stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
    output = stdout.read()
    file1= fname+".html"
    a=open(os.path.join(FILE_URL,file1),'r')
    r=a.readlines()
    r1=r[:-6]
    ap=open(os.path.join(FILE_URL,file1),'w')
    s=""
    s=r1
    n=""
    for line in s:
        n += line.lstrip()
    print r1
    ap.write(n)
    ap.close()
    src=FILE_URL+fname+".html"
    des=HTML_FILE_URL
    file_relocate=shutil.copy(src,des)
    fname1=fname+".html"
    variables = RequestContext(request, {'fname':fname1,'newfname':"test"})
    template = "metadashboard/newdownload.html"
    return render_to_response(template, variables)


    

def AjaxAddCollection(request):
    title1=request.GET["title"]
    collection=request.GET["collection"]
    uid=request.GET["uid"]
    usr=request.GET["usr"]
    orgcontent=request.GET["orgcontent"]
    list1=request.GET["list"]
    list1=list1.split(",");
    create_wikipage(title1,uid,orgcontent,usr,collection,list1)
    return HttpResponseRedirect("/gstudio/page/gnowsys-page/1815")

def IsWiki(request):
    ptitle=request.GET["title"]
    iswiki=Gbobject.objects.filter(title=ptitle)
    if iswiki:
        return HttpResponse("sucess")

def ajaxDeletePriorpage(request):
	print "in ajax"
	objectid1 = ""
	gbid1=""
	if request.is_ajax() and request.method =="POST":
		print "in get"
		objectid1=request.POST['objectid1']
		objectid2=request.POST['objectid2']
		print objectid1,objectid2,"objectsid"
		gbid1=Gbobject.objects.get(id=objectid1)
		gbid2 = Gbobject.objects.get(id=objectid2)
		gbid1.prior_nodes.remove(gbid2)
		gbid2.posterior_nodes.remove(gbid1)
		gbid1=Gbobject.objects.get(id=objectid1)
	priorgbobject = gbid1.prior_nodes.all()
	posteriorgbobject = gbid1.posterior_nodes.all()
	variables = RequestContext(request, {'priorgbobject':priorgbobject,'posteriorgbobject':posteriorgbobject,'objectid':objectid1,'optionpriorpost':"priorpost"})
        template = "gstudio/repriorpost.html"
        return render_to_response(template, variables)

	
                    
                
                

            



	
	
	
	
