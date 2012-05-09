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

def history(request,ssid):
   # iden=request.GET["id"]
    nt1=Version.objects.get(id=ssid)
    nt=nt1.object
    ver_dict=nt.version_info(ssid)
    variables = RequestContext(request,{'ver_dict':ver_dict ,'nt':nt,'ssid':ssid })
    template="gstudio/display.html"
    return render_to_response(template,variables)

def showHistory(request):
    vid1=request.GET["group1"]
    vid2=request.GET["group2"]
    nt=Version.objects.get(id=vid1)
    nt1=nt.object
    pp=pprint.PrettyPrinter(indent=4)
    # ver_new=Version.objects.get(id=vid1)
    # ver_old=Version.objects.get(id=vid2) 
    ver_new_dict=nt1.version_info(request.GET["group1"])
    ver_old_dict=nt1.version_info(request.GET["group2"])
    ver_new_nbh=ver_new_dict['nbhood']
    ver_old_nbh=ver_old_dict['nbhood']
    ver_new_nbh=ver_new_nbh.replace(",","\n")
    ver_new_nbh=ver_old_nbh.replace(",","\n")
   # ver_new=""
   # ver_old=""
   # for each in ver_new_nbh:
   #	ver_new+=each + ":" + str(ver_new_nbh[each])+'\n'
   # for each in ver_old_nbh: 
   #	ver_old+=each + ":" + str(ver_old_nbh[each])+'\n'
    diffs = dmp.diff_main(ver_new_nbh, ver_old_nbh)
    d=dmp.diff_prettyHtml(diffs)
    return HttpResponse(d) 
    # ver_new=nt1.version_info(request.GET["group1"])
    # ver_old=nt1.version_info(request.GET["group2"])
     
    # variables=RequestContext(request,{'nt':nt1,'ver_old':ver_old,'ver_new':ver_new,'diffs':diffs })
    # template="gstudio/version_diff.html"
    # return render_to_response(template,variables)
