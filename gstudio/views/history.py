from django.http import *
from reversion.models import *
from gstudio.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.date_based import object_detail


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

def showHistory(request,obj):
    obj=Objecttype.objects.get(id=obj)
    variables=RequestContext(request,{'ob':ob})
    template="gstudio/history.html"
    return render_to_response(template,variables)
