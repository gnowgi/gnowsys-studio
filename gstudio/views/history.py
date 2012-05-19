from django.http import *
from reversion.models import *
from gstudio.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.date_based import object_detail
from reversion.helpers import *
import pprint
from gstudio.models import *
from reversion.models import *
from gstudio.views.decorators import protect_nodetype
from gstudio.views.decorators import update_queryset
import ast

def history(request,ssid,cnt):
   # iden=request.GET["id"]
    nt1=Version.objects.get(id=ssid)
    nt=nt1.object.ref
    ver_dict=nt.version_info(ssid)
    variables = RequestContext(request,{'ver_dict':ver_dict ,'nt':nt,'ssid':ssid,'cnt':cnt })
    template="gstudio/display.html"
    return render_to_response(template,variables)

def showHistory(request,ssid):
   # vid1=request.GET["group1"]
    vid1=ssid
    vid2=request.GET["group2"]
    nt=Version.objects.get(id=vid1)
    nt1=nt.object.ref
    pp=pprint.PrettyPrinter(indent=4)
    ver_new1=Version.objects.get(id=vid1)
    ver_old1=Version.objects.get(id=vid2) 
    
    ver_new_dict=nt1.version_info(request.GET["group1"])
    content=str(ver_new_dict['content'])
    content=content[3:-4]
    ver_new_dict['content']=content
    ver_old_dict=nt1.version_info(request.GET["group2"])
    content=str(ver_old_dict['content'])
    content=content[3:-4]
    ver_old_dict['content']=content
    
    ver_new_nbh=ver_new_dict['nbhood']
    ver_new_dict1=ast.literal_eval(ver_new_nbh)
    
    ver_old_nbh=ver_old_dict['nbhood']
    ver_old_dict1=ast.literal_eval(ver_old_nbh)

  #  ver_new_nbh=ver_new_nbh.replace(",","\n")
  #  ver_old_nbh=ver_old_nbh.replace(",","\n")
    d=[]
    d1=[]
    field=['Name','Plural Name','Alternate Name','Authors','Content']
    for each in ver_new_dict1:
	 ver_new=""
         ver_old=""
	 if each =='altnames':
         	ver_new+=ver_new_dict['altnames']
		ver_old+=ver_old_dict['altnames']  
		  
		diffs = dmp.diff_main(ver_new, ver_old)
		d.append(dmp.diff_prettyHtml(diffs))
	#	diffs = dmp.diff_main(ver_old, ver_new)
	#	d1.append(dmp.diff_prettyHtml(diffs))
    		
         if each =='title':
		ver_new+=ver_new_dict['title']
		ver_old+=ver_old_dict['title'] 
		diffs = dmp.diff_main(ver_new, ver_old)
    		d.append(dmp.diff_prettyHtml(diffs))
	#	diffs = dmp.diff_main(ver_old, ver_new)
	#	d1.append(dmp.diff_prettyHtml(diffs))
	 if each =='plural':
         	ver_new+=ver_new_dict['plural']
		ver_old+=ver_old_dict['plural'] 
		diffs = dmp.diff_main(ver_new, ver_old)
    		d.append(dmp.diff_prettyHtml(diffs))
	#	diffs = dmp.diff_main(ver_old, ver_new)
	#	d1.append(dmp.diff_prettyHtml(diffs))
       #  if each =='content':
    ver_new=""
    ver_old=""
    ver_new+=ver_new_dict['content']
    ver_old+=ver_old_dict['content']
    diffs = dmp.diff_main(ver_new, ver_old)
    d.append(dmp.diff_prettyHtml(diffs))
	#	diffs = dmp.diff_main(ver_old, ver_new)
	#	d1.append(dmp.diff_prettyHtml(diffs))

  #  for each in ver_new_dict1:
#	ver_new=""
 #       ver_old=""
  #  	ver_new+=each + ":" + str(ver_new_dict1[each])
#	ver_old+=each + ":" + str(ver_old_dict1[each])
 #   	diffs = dmp.diff_main(ver_new, ver_old)
  #  	d.append(dmp.diff_prettyHtml(diffs))
	
  #  return HttpResponse(d) 
    ver_new=nt1.version_info(request.GET["group1"])
    ver_old=nt1.version_info(request.GET["group2"])
     
    variables=RequestContext(request,{'nt':nt1,'ver_old':ver_old_dict,'ver_new':ver_new_dict,'diffs':d ,'vid1':vid1,'vid2':vid2 })
    template="gstudio/version_diff.html"
    return render_to_response(template,variables)

