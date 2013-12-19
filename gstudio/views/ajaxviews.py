

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
from django.template.defaultfilters import slugify
import json
import shutil
import codecs
from gstudio.models import *
from objectapp.models import *
rlist={}
import os
from settings import PYSCRIPT_URL_GSTUDIO
from demo.settings import FILE_URL,PYSCRIPT_URL_GSTUDIO,HTML_FILE_URL
from gstudio.methods import sendMail_RegisterUser,sendMail_NonMember
import unicodedata
from itertools import chain
from unidecode import unidecode

def Deldoccolln(request):
    try:
        obid=request.GET["obid"]
        a=System.objects.get(id=obid)
        a.delete()
        listcolls={}
        syst=Systemtype.objects.get(title='Documentcollection')
        a=syst.member_systems.all()
        for each in a:
            listcolls[each.id]=each.title
        listcolls={}
    except:
        return render_to_response("gstudio/doccollns.html",{'user':request.user})
    return render_to_response("gstudio/doccollns.html",{'user':request.user})

def Delimgcolln(request):
    try:
        obid=request.GET["obid"]
        a=System.objects.get(id=obid)
        a.delete()
        listcolls={}
        syst=Systemtype.objects.get(title='Documentcollection')
        a=syst.member_systems.all()
        for each in a:
            listcolls[each.id]=each.title
        listcolls={}
    except:
        return render_to_response("gstudio/imagecollns.html",{'user':request.user})
    return render_to_response("gstudio/imagecollns.html",{'user':request.user})




def getobjs(request):
    dic={}
    tosearch=""
    rt=request.GET["reltype"]
    oth=request.GET["otherrelns"]
    print "rt=",rt,"oth",oth
    allobs=[]
    rttitle=Relationtype.objects.get(id=rt).title
    unidecdtitle=unidecode(rttitle)
    allobs=""
    if oth == "0":
        if rttitle=='has_video':
            tosearch='Video'
        elif rttitle=='has_image':
            tosearch='Image'
        elif rttitle=='has_document':
            tosearch='Document'
        elif rttitle=='has_html':
            tosearch='Html'
        elif rttitle=='has_spreadsheet':
            tosearch='Spreadsheet'
        elif rttitle=='has_pdf':
            tosearch='PDF'
        elif rttitle=='has_presentation':
            tosearch='Presentation'
        elif rttitle=='has_multimedia':
            tosearch='Multimedia'
        elif rttitle=='has_graphics':
            tosearch='Graphics'
        elif rttitle=='has_audio':
            tosearch='Audio'
        elif unidecdtitle=='chvi hai':
            tosearch='Image'
        else:
            tosearch=""
        if tosearch:
            ob=Objecttype.objects.get(title=tosearch)
            allobs=ob.get_nbh['contains_members']
            allobs=allobs.exclude(title__icontains='page box of').exclude(title__icontains='message box of')

    else:
        wiki=Systemtype.objects.get(title='Wikipage')
        allwiki=wiki.member_systems.all()
        loom=Systemtype.objects.get(title='Meeting')
        alllooms=loom.member_systems.all()
        allobs=list(chain(allwiki,alllooms))
    if allobs:
        for each in allobs:
            dic[unidecode(each.title)+"-"+str(each.id)]=each.id
#            dic[unicodedata.normalize('NFKD', each.title).encode('ascii','ignore')+"-"+str(each.id)]=each.id
 
    jdictionary = json.dumps(dic)
    return HttpResponse(jdictionary)



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
    collection=request.GET["collection"]
    rt=Relationtype.objects.get(title="includes")
    if rt:
        relset=Relation.objects.filter(relationtype_id=rt.id)
        j=0
	if relset:
            relset1=relset.filter(left_subject_id=wtitle)
	    relset1.delete()
  
    if collection:
        collection=True
    else:
        collection=False
    
    sys=System.objects.get(id=wtitle)
    collection_set=Systemtype.objects.get(title="Collection")
    collection_set1=collection_set.member_systems.all()
    f=0
    for each in collection_set1:
        if (each.id) == wtitle:
            f=1
    if f == 0:
        sys.systemtypes.add(Systemtype.objects.get(title="Collection"))
    
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
            r=Relation()
            r.left_subject_id=wtitle
            r.right_subject_id=list2[i]
            r.relationtype_id=rt.id
            r.save()
            
            objs=Gbobject.objects.get(id=list2[i])
            sys.gbobject_set.add(objs)
            n_set.append(list2[i])
            i=i+1
        var=sys.in_gbobject_set_of.__dict__['through']
        varobset=[]
        for each in var.objects.all():
            if each.system_id == sys.id:
                s=Gbobject.objects.get(id=each.gbobject_id)
                s1=s.title
                varobset.append(s)
    variables = RequestContext(request, {'sys':sys,'list':n_set,'objset':varobset,'collection':collection})
    template = "metadashboard/newcollection.html"
    
    return render_to_response(template, variables)

def HtmlExport(request):
    ptitle=request.GET["ptitle"]
    set1=request.GET["title"]
    if set1 == "null":
        
        ptitle=System.objects.get(id=ptitle)
        s=ptitle.get_ssid.pop()	
        contorg=ptitle.content_org    #ptitle=eval(ptitle)
        content_org="* "+ptitle.title+"\n"+unicode(contorg)+"\n"

    else:
	ptitle1=System.objects.get(id=ptitle)
	s=ptitle1.get_ssid.pop()
        
        set1=set1+","
        set2=eval(set1)
        
        s1=str(ptitle.title)
        varobset=get_gbobjects(ptitle)
        contorg=ptitle1.content_org    #ptitle=eval(ptitle)
        content_org="* "+ptitle1.title+"\n"+unicode(contorg)+"\n"
        set2=[]
        set2=ptitle1.gbobject_set.all()
        l=len(set2)
        i=0
        if l>0:
            while i<len(varobset):
                st=System.objects.get(id=varobset[i].id)
                stcontorg=st.content_org
                content_org += "** "+varobset[i].title+"\n"+unicode(stcontorg)+"\n"
                if st.gbobject_set.exists():
                    gbset=get_gbobjects(st.id)
                    
                    
                    for each in gbset:
                        subst=System.objects.get(id=each.id)
                        substcontorg=subst.content_org
                        content_org += "*** "+str(each)+"\n"+unicode(substcontorg)+"\n"
                  
                            
                
                        if subst.gbobject_set.exists():
                            subgbset=get_gbobjects(subst.id)
                            for each in subgbset:
                                subtwost=System.objects.get(id=each.id)
                            
                                content_org += "**** "+str(each)+"\n"+each.content_org+"\n"
                            
                                if subtwost.gbobject_set.exists():
                                    subtwogbset=get_gbobjects(subtwost.id)
                                    for each in subtwogbset:
                                        subthreest=System.objects.get(id=each.id)
                                        content_org += "***** "+str(each)+"\n"+each.content_org+"\n"
                

                                        if subthreest.gbobject_set.exists():
                                            subthreegbset=get_gbobjects(subthreest.id)
                                            for each in subthreegbset:
                                                subfourst=System.objects.get(id=each.id)
                                                content_org += "****** "+str(each)+"\n"+each.content_org+"\n"
                                            
                                                if subfourst.gbobject_set.exists():
                                                    subfourgbset=get_gbobjects(subfourst.id)
                                                    for each in subfourgbset:
                                                        subfivest=System.objects.get(id=each.id)
                                                        content_org += "******* "+str(each)+"\n"+each.content_org+"\n"
                                                    
                                                        if subfivest.gbobject_set.exists():
                                                            subfivegbset=get_gbobjects(subfivest.id)
                                                            for each in subfivegbset:
                                                                subsixst=System.objects.get(id=each.id)
                                                                content_org += "******** "+str(each)+"\n"+each.content_org+"\n"
                                                            
                    
                i+=1 
		
   
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
	objectid1 = ""
	gbid1=""
	if request.is_ajax() and request.method =="POST":
		objectid1=request.POST['objectid1']
		objectid2=request.POST['objectid2']
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

def ajaxAddResponsesToTwist(request):
    userid = ''
    admin_id = ''
    response_content=""
    twistid=""
    username=""
    attribute="true"
    if request.is_ajax() and request.method =="POST":
        response_content=request.POST['response_content']
        twistid=request.POST['twistid']
        userid=request.POST['userid']
        username=request.POST['username']
	admin_id =request.POST['admin_id'] 
	
        
    boolean = make_relation(response_content,int(twistid),int(userid),username)
    twistobject = Gbobject.objects.get(id=int(twistid))
    for each in twistobject.subject_of.all():
	if each.attributetype.title == "release":
	   attribute = each.svalue
    variables = RequestContext(request, {'comment':twistobject , 'idusr' : int(userid), 'flag' : "True", 'admin_id' : admin_id , 'attribute' : attribute})
    template = "gstudio/tags/comment.html"
    return render_to_response(template,variables)
#Ajax views for retriving comment for auto refresh in Loom>twist Response div
def ajaxResponseReciev(request):
    userid = ''
    admin_id = ''
    twistid=""
    attribute="true"
    if request.is_ajax() and request.method =="POST":
        twistid=request.POST['twistid']
        userid=request.POST['userid']
        admin_id =request.POST['admin_id']

    twistobject = Gbobject.objects.get(id=int(twistid))
    for each in twistobject.subject_of.all():
        if each.attributetype.title == "release":
            attribute = each.svalue
            break
    variables = RequestContext(request, {'comment':twistobject , 'idusr' : int(userid), 'flag' : "True", 'admin_id' : admin_id , 'attribute' :
 attribute})
    template = "gstudio/tags/comment.html"
    return render_to_response(template,variables)


def ajaxSendInvitation(request):
    userid = ''
    admin_id = ''
    invalidEmail = ""
    if request.is_ajax() and request.method =="POST":
        systemid=request.POST['systemid']
        data=request.POST['data']
        senderuserid=request.POST['senderuserid']
    senderuser = User.objects.get(id=senderuserid)
    data = data.split(',')
    for each in data:
	lengthofdata = ""
	lengthofdata=len(each.split())
	if lengthofdata == 1:
		receiveremail = ""
		receiveremail = each.split()[0]
		sendMail_NonMember(senderuser,receiveremail,"invites you to Metastudio.org and","to the loom thread",systemid,"/gstudio/group/gnowsys-grp/"+systemid)
        else:
	    receiveruser = User.objects.filter(username=each.split()[0])
	    if receiveruser :
		sendMail_RegisterUser(senderuser,receiveruser,"invites you","to the thread",systemid,"/gstudio/group/gnowsys-grp/"+systemid)
	    else:
		invalidEmail = invalidEmail+each +" , "
    if invalidEmail:
       return HttpResponse(invalidEmail)
    else:
       return HttpResponse("sucess")	

def ajaxuserListForInvitation(request):
    userListJson = ""
    if request.method =="GET":
        systemid=request.GET['systemid']
        senderuserid=request.GET['senderuserid']
    userlist = []
    for each in User.objects.all():
	if not each.id == senderuserid:
	      userlist.append(each.username.__str__()+"  <"+each.email.__str__()+">")
        userListJson = json.dumps(userlist)
    return HttpResponse(userListJson)

def ajaxReleaseBlockResponseOfTwist(request):
    threadTwistid = ""
    twistActivity = ""
    gbobjecttwist = ""
    checkAttribute = False
    if request.is_ajax() and request.method =="POST":
        threadTwistid=request.POST['threadTwistid']
        twistActivity=request.POST['twistActivity']
    gbobjecttwist = Gbobject.objects.filter(id=threadTwistid)
    if gbobjecttwist:
	gbobjecttwist = Gbobject.objects.get(id=threadTwistid)
	if gbobjecttwist.subject_of.all():	
	    for each in gbobjecttwist.subject_of.all():
		if each.attributetype.title=="release":
		    each.svalue=twistActivity
		    gbobjecttwist.subject_of.add(each)
		    checkAttribute = True
	if checkAttribute == False:
	    a = Attribute()
	    a.title = "released button of " + gbobjecttwist.title
	    a.slug = slugify(a.title)
	    a.content = a.slug
            a.status = 2
	    a.subject = gbobjecttwist
	    a.svalue = twistActivity
	    a.attributetype_id = Attributetype.objects.get(title="release").id
	    a.save()
					
    return HttpResponse("sucess")
	
def ajaxRateIt(request):
    objectid = ""
    rating = ""
    if request.is_ajax() and request.method =="POST":
        objectid = request.POST['objectid']
	rating = request.POST['data']
    ob = Gbobject.objects.get(id=objectid)
    ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
    variables = RequestContext(request, { 'object' : ob})
    template = "gstudio/addingrate.html"
    return render_to_response(template,variables)                         
                
                
def Status(request):
    page_ob=request.GET["pageobj"]
    sys=System.objects.get(id=page_ob)
    sys.status = 2
    sys.save()
    return HttpResponse("sucess")

#ajax views for getting graph text in Releted topic       
def ajaxgetConceptPageGraphText(request):
    nidObject=""
    objectid= ""
    resultDict = {}
    nidObjectSystem = ""
    collection=False
    if request.is_ajax() and request.method =="POST":
        objectid=request.POST['objectid']
        nidObject = NID.objects.filter(id=objectid)
    else :
	return HttpResponse("failed")	
    if nidObject:
	nbhdata=get_nbh_of_nbh(objectid)
    else :
        return HttpResponse("failed")
    variables = RequestContext(request, {'nbhdata':nbhdata})
    template = "metadashboard/graphText.html"
    return render_to_response(template,variables)

#ajax Resources in tab view
def ajaxgetConceptPageResources(request):
    nidObject=""
    objectid= ""
    resultDict = {}
    nidObjectSystem = ""
    collection=False
    if request.is_ajax() and request.method =="POST":
        objectid=request.POST['objectid']
        nidObject = NID.objects.filter(id=objectid)
    else :
	return HttpResponse("failed")	
    if nidObject:
	nidObjectGet = NID.objects.get(id=objectid)
	nidObjectSystem = nidObjectGet.ref.system
	collsys=nidObjectSystem.systemtypes.all()
        iscoll=collsys.filter(title="Collection")
        if iscoll:
            collection=True
	Section = nidObjectSystem.system_set.all()[0].gbobject_set.all()
	ot=nidObjectSystem.gbobject
	test1=get_pdrawer()

    else :
        return HttpResponse("failed")
    variables = RequestContext(request, {"page_ob":nidObjectSystem,"collection":collection,'ot' : ot,'section' : Section,'object':nidObjectSystem,'test1':test1})
    template = "metadashboard/wikiResources.html"
    return render_to_response(template,variables)


            



	
	
	
	
