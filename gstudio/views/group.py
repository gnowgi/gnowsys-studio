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
from notification import models as notification
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from gstudio.templatetags.gstudio_tags import show_nodesystem

def notifyactivity(request,activ,sys_id,userid):
        print "activity =",activ
        sys=""
        box=""
        if activ=='edited_thread':
                print 'edited thread'
                ss=System.objects.filter(id=sys_id)
                if ss:
                        sys=System.objects.get(id=sys_id)
                        box=sys.system_set.all()[0]
                        sysurl=str(sys.get_view_url)

        else:
                print 'edited deleted',sys_id
                ss=Gbobject.objects.filter(id=sys_id)
                if ss:
                        print 'inside ss'
                        ss=Gbobject.objects.get(id=int(sys_id))
                        if activ=='edited_twist':
                                sys=ss.getthread_of_twist
                                sysurl='gstudio/'+str(show_nodesystem(sys.id))
                                box=get_threadbox_of_twist(int(sys_id))
                                
                        elif activ=='deleted_response'or 'added_response':
                                print 'ss=',ss
                                systhd=ss.getthread_of_response
                                sys=systhd
                                if systhd:
                                        box=systhd.system_set.all()[0]
                                        sysurl=str(systhd.get_view_url)
                                        sys_id=str(sys.id)
                        
                        print box,"box"
        if sys:
                site=Site.objects.get_current()
                render = render_to_string("/gstudio/notification/label.html",{'sender':request.user,'activity':activ,'conjunction':'\
-','object':sys.title,'url':sysurl,'site':site})
                if box:
                        for bx in box.member_set.all():
                                notification.create_notice_type(render, "Invitation Received", "you have received an invitation")
                                notification.send([bx], render, {"from_user": request.user})
        if activ=='edited_thread' or activ=='deleted_response' or activ=='added_response':
                return HttpResponseRedirect("/gstudio/group/gnowsys-grp/"+sys_id)
        elif activ=='edited_twist':
                return HttpResponseRedirect("/gstudio/"+sysurl)


def notifyuser(request,sys_id,userid):
	sys=System.objects.get(id=sys_id)
	box=sys.system_set.all()[0]
	sysurl = str(sys.get_view_url)
	site=Site.objects.get_current()
        box.member_set.add(Author.objects.get(id=userid))
	render = render_to_string("/gstudio/notification/label.html",{'sender':request.user,'activity':'Subscribed','conjunction':'to','object':sys.title, 'url':sysurl,'site':site}) 
	for bx in box.member_set.all():
		notification.create_notice_type(render, "Invitation Received", "you have received an invitation")
		notification.send([bx], render, {"from_user": request.user})
        return HttpResponseRedirect("/gstudio/group/gnowsys-grp/"+sys_id)

def notifyuserunsubscribe(request,sys_id,userid):
	sys=System.objects.get(id=sys_id)
	box=sys.system_set.all()[0]
	sysurl = str(sys.get_view_url)
	site=Site.objects.get_current()
	render = render_to_string("/gstudio/notification/label.html",{'sender':request.user,'activity':'UnSubscribed','conjunction':'from','object':sys.title,'url':sysurl,'site':site}) 
	for bx in box.member_set.all():
		notification.create_notice_type(render, "Invitation Received", "you have received an invitation")
		notification.send([bx], render, {"from_user": request.user})
        box.member_set.remove(Author.objects.get(id=userid))
        return HttpResponseRedirect("/gstudio/group/gnowsys-grp/"+sys_id)

def grouplater(request, sys_id, starttime):
#   return HttpResponse("the meeting is scheduled later")
	now=datetime.datetime.now()
	sys=System.objects.get(id=sys_id)
	template="gstudio/later.html"
	var=RequestContext(request, {'sys':sys, 'starttime':starttime})
	return render_to_response(template, var)
def groupover(request,sys_id, endtime):  
#   return HttpResponse("the meeting is over!")
	sys=System.objects.get(id=sys_id)
	template="gstudio/over.html"
	var=RequestContext(request, {'sys':sys, 'endtime':endtime})
	return render_to_response(template, var)

   
    
def groupdashboard(request,grpid):
   grpid = int(grpid)
   (later, meetover, starttime, endtime) = get_time(grpid)
 #  if meetover:
#	return groupover(request, grpid, endtime)
   if later and request.user.id != System.objects.get(id=grpid).authors.all()[0].id:
	return grouplater(request, grpid, starttime)
   else:
	
	boolean1 = False
   	flag= False
	meeting_ob = System.objects.get(id=grpid)
   	if request.method == "POST" :
    		boolean = False
    		rep = request.POST.get("reply",'')
    		id_no = request.POST.get("iden",'')
    		id_no1 = request.POST.get("parentid","")
		idusr = request.POST.get("idusr",'')
                usr = request.POST.get("usr",'')
                rating = request.POST.get("star1","")
   		flag1=request.POST.get("release","")
    		block = request.POST.get("block","")
                topic_del = request.POST.get("del_topic", "")
                comment_del = request.POST.get("del_comment", "")
		editable=request.POST.get("edit","")
	        editval=request.POST.get("editval","")
		edittitle=request.POST.get("edittitle","")
	        editcontent=request.POST.get("editcont","")
	        editiden=request.POST.get("editiden","")
                docid = request.POST.get("docid","")
                addtags = request.POST.get("addtags","")
                texttags = unicode(request.POST.get("texttags",""))
	        if editval=='editthread':
			edit_thread(editiden,editcontent,str(request.user))
		if editable=='edited':
			if id_no :
				edit_topic(id_no,rep,usr)
    			elif id_no1 :
				edit_topic(id_no1,rep,str(request.user))
		if topic_del:
                        del_topic(int(id_no))
                if comment_del:
                        del_comment(int(id_no1))

	     	if addtags != "":
         		i=Gbobject.objects.get(id=int(docid))
		        i.tags = i.tags+ ","+(texttags)
		        i.save()
		if flag1:
      			boolean1 = True
      			make_att_true(meeting_ob)
    		if block :
      			make_att_false(meeting_ob)
    		if rating :
        		rate_it(int(id_no1),request,int(rating))
		if rep and  editable!='edited':
    			if not id_no :
                                
			   	boolean = make_relation(rep,int(id_no1),int(idusr),str(request.user))
    			elif not id_no1 :
				boolean = make_relation(rep,int(id_no),int(idusr),usr)
        	if boolean :
	     		return HttpResponseRedirect("/gstudio/group/gnowsys-grp/"+str(grpid))
   	grpid = int(grpid)
	if request.user.is_superuser:
		flag = True
   	if request.user.id == meeting_ob.authors.all()[0].id :
     		flag = True 
   	Topic = meeting_ob.system_set.all()[0].gbobject_set.all()
   	admin_id = meeting_ob.authors.all()[0].id #a list of topics
	for each in meeting_ob.subject_of.all():
		if each.attributetype.title=='release':

	   		attob = each.svalue
			break
   	admin_m = meeting_ob.authors.all()[0]
	topic_type_set=Objecttype.objects.get(title='Topic')
	if(len(topic_type_set.get_members)):
		latest_topic=topic_type_set.get_members[0]
	       	post=latest_topic.get_absolute_url()
       	else:
		post="no topic added yet!!"
	ot=Gbobject.objects.get(id=grpid)
        meeting_ob = System.objects.get(id=grpid)
	variables = RequestContext(request,{'ot' : ot,'topic' : Topic , 'meet_ob' : meeting_ob, "flag" : flag, "flag1" : boolean1, "admin_id" : admin_id, "attribute" : attob, 'admin_m':admin_m, 'endtime':endtime, 'post':post})
   	template = "metadashboard/grpdashboard.html"
   	return render_to_response(template, variables)


    
