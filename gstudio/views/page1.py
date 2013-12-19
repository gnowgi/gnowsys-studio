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
   
def pagedashboard(request,pageid):
   pageid = int(pageid)
   
   # boolean1 = False
   flag= False
   page_ob = System.objects.get(id=pageid)
   if request.method == "POST" :
      boolean = False
      rep = request.POST.get("replytosection",'')
      id_no = request.POST.get("iden",'')
      id_no1 = request.POST.get("parentid","")
      print rep,"rep    ",id_no,"id_no   ",id_no1,"id_no1    "
      idusr = request.POST.get("idusr",'')
      rating = request.POST.get("star1","")
      section_del = request.POST.get("del_section", "")
      comment_del = request.POST.get("del_comment", "")
      docid = request.POST.get("docid","")
      addtags = request.POST.get("addtags","")
      texttags = unicode(request.POST.get("texttags",""))
      editable = request.POST.get("edit","")
      if editable=="edited":
         if id_no:
            edit_section(id_no,rep)
         elif id_no1:
            edit_section(id_no1,rep)
        
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

      if rep and editable!='edited' :
         if not id_no :
            ptitle= make_title(int(id_no))      
            boolean = make_sectionrelation(rep,ptitle,int(id_no1),int(idusr))
            
           
         elif not id_no1 :
            ptitle= make_title(int(id_no))
            boolean = make_sectionrelation(rep,ptitle,int(id_no),int(idusr))
            
      if boolean :
         return HttpResponseRedirect("/gstudio/page/gnowsys-page/"+str(pageid))
   pageid = int(pageid)
   if request.user.id == page_ob.authors.all()[0].id :
      flag = True 
   Section = page_ob.system_set.all()[0].gbobject_set.all()
   admin_id = page_ob.authors.all()[0].id #a list of topics
   #    #    for each in page_ob.subject_of.all():
   #    #       if each.attributetype.title=='pagerelease':
   #    #          attob = each.svalue
   #    #       break
   admin_m = page_ob.authors.all()[0]
   
   topic_type_set=Objecttype.objects.get(title='Section')
   if(len(topic_type_set.get_members)):
      latest_topic=topic_type_set.get_members[0]
      post=latest_topic.get_absolute_url()
   else:
      post="no topic added yet!!"
   ot=Gbobject.objects.get(id=pageid)
   page_ob = System.objects.get(id=pageid)
   variables = RequestContext(request, {'ot' : ot,'section' : Section,'page_ob' : page_ob,'admin_m':admin_m,"flag" : flag,"admin_id" : admin_id,'post':post})
   template = "metadashboard/pgedashboard.html"
   return render_to_response(template, variables)
