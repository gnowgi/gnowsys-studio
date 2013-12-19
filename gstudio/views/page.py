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
from django.http import Http404
from gstudio.models import *
from gstudio.methods import *
   
def pagedashboard(request,pageid):
   pageid = int(pageid)
   flag= False
   collection=False
   status=False
   usr1=request.user
   is_staff=False
   if usr1.is_staff:
      is_staff=True
   page_ob = System.objects.filter(id=pageid)
   if page_ob:
      page_ob = System.objects.get(id=pageid)
      if "Wikipage" in [each.title for each in page_ob.systemtypes.all()]:
         pass 
      else:
         raise Http404
   else:
       raise Http404
   test=""
   test=get_gbobjects(page_ob.id)
   test1=get_pdrawer()
   Topic=""
   attob=''
   boolean1 = False
   flag= False

   
   if request.method == "POST" :
      boolean = False
      rep = request.POST.get("replytosection",'')
      id_no = request.POST.get("iden",'')
      id_no1 = request.POST.get("parentid","")
      idusr = request.POST.get("idusr",'')
      usr = request.POST.get("usr",'')
      rating = request.POST.get("star1","")
      section_del = request.POST.get("del_section", "")
      comment_del = request.POST.get("del_comment", "")
      docid = request.POST.get("docid","")
      addtags = request.POST.get("addtags","")
      texttags = unicode(request.POST.get("texttags",""))
      editable = request.POST.get("edit","")
      
      #Discus section started
      rating = request.POST.get("star1","")
      flag1=request.POST.get("release","")
      block = request.POST.get("block","")
      topic_del = request.POST.get("del_topic", "")
      if flag1:
         boolean1 = True
         make_att_true(meeting_ob)
      if block :
         make_att_false(meeting_ob)
      if rating :
         rate_it(int(id_no1),request,int(rating))
      if topic_del:
         del_topic(int(id_no))
      #Close discus  
      
      if editable=="edited":
          if id_no:
             edit_section(id_no,rep,usr)
          elif id_no1:
             edit_section(id_no1,rep,str(request.user))
      if section_del:
         del_section(int(id_no))
      if comment_del:
         del_comment(int(id_no1))
      if rating :
         rate_section(int(id_no),request,int(rating))
      if addtags != "":
         i=Gbobject.objects.get(id=docid)
         i.tags = i.tags+ ","+(texttags)
         i.save()

      if rep and editable!='edited':
         if not id_no :
            ptitle= make_title(int(id_no1))      
            boolean = make_sectionrelation(rep,ptitle,int(id_no1),int(idusr),usr)
         elif not id_no1 :
            ptitle= make_title(int(id_no))
            boolean = make_sectionrelation(rep,ptitle,int(id_no),int(idusr),usr)
      if boolean :
         return HttpResponseRedirect("/gstudio/page/gnowsys-page/"+str(pageid))
   pageid = int(pageid)
   if request.user.id == page_ob.authors.all()[0].id :
      flag = True 
   #Section = page_ob.system_set.all()[0].gbobject_set.all()
   admin_id = page_ob.authors.all()[0].id #a list of topics
   admin_m = page_ob.authors.all()[0]
   
   topic_type_set=Objecttype.objects.get(title='Section')
   if(len(topic_type_set.get_members)):
      latest_topic=topic_type_set.get_members[0]
      post=latest_topic.get_absolute_url()
   else:
      post="no topic added yet!!"
   ot=Gbobject.objects.get(id=pageid)
   page_ob = System.objects.get(id=pageid)
   collsys=page_ob.systemtypes.all()
   iscoll=collsys.filter(title="Collection")
   if iscoll:
      collection=True
   if (page_ob.status == 1):
      status=True
   #if section for retrive Topic of Discus
   if page_ob:
        if page_ob.system_set.all():
                 Topic = page_ob.system_set.all()[0].gbobject_set.all()
   
   variables = RequestContext(request, {'ot' : ot,'page_ob' : page_ob,'object':page_ob,'admin_m':admin_m,"flag" : flag,"admin_id" : admin_id,'post':post,'test':test, 'test1':test1,'collection':collection,'status':status, 'topic':Topic, "is_staff":is_staff})
   template= "metadashboard/download.html"
   template = "metadashboard/pgedashboard.html"
   return render_to_response(template, variables)
 			
