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
from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.settings import *
from gstudio.models import *
from objectapp.models import *
from gstudio.methods import *


def userpreference(request):
	user = str(request.user)
	#url=request.get_full_path
	#print url,'url'
	#re = request.REQUEST.get("next","")
	#print re,"url"
	if request.method=="POST":
		fontcolor = request.POST.get("fontcolor","")
		bgcolor= request.POST.get("bgcolor","")
		colorsave = request.POST.get("colorsave","")
		#re = request.REQUEST.get("next","")
		#print re
		editcolorsave = request.POST.get("editcolorsave","")
		if colorsave:
			attributetype_fc = Attributetype.objects.filter(title="font_color")
			attributetype_bg = Attributetype.objects.filter(title="bg_color")
			if not attributetype_fc:
				newattributetype = Attributetype()
				newattributetype.title = "font_color"
				newattributetype.slug = "font_color"
				newattributetype.dataType = '2'
				newattributetype.applicable_nodetypes = "OB"
				newattributetype.subjecttype_id="7"
				newattributetype.content="text"
				newattributetype.save()
			if not attributetype_bg:
				newattributetype = Attributetype()
				newattributetype.title = "bg_color"
				newattributetype.slug = "bg_color"
				newattributetype.dataType = '2'
				newattributetype.subjecttype_id="7"
				newattributetype.applicable_nodetypes = "OB"
			        newattributetype.content="text"
				newattributetype.save()	
			usergb = Gbobject.objects.filter(title =user+"_preference")
			if not usergb:
				gb=Gbobject()
				gb.title= user+"_preference"
				gb.slug=user+"_loom_preference"
				gb.save()
				gb.objecttypes.add(Objecttype.objects.get(title="Factory_Object"))
				s=Author.objects.get(username=user)
				gb.authors.add(s)
			gb = Gbobject.objects.get(title =user+"_preference")
			print fontcolor,"font"
			if fontcolor:
				atf=Attribute()
				atf.attributetype=Attributetype.objects.get(title="font_color")
				atf.subject=gb
				atf.svalue=fontcolor
				atf.save()
			if bgcolor:
				atb=Attribute()
				atb.attributetype=Attributetype.objects.get(title="bg_color")
				atb.subject=gb
				atb.svalue=bgcolor
				atb.save()
			vars=RequestContext(request,{})
			template="gstudio/userpreference.html"
			return render_to_response(template, vars)
		
		if editcolorsave:
			a_id = Gbobject.objects.get(title=user+"_preference").id
			atypebg_id = Attributetype.objects.get(title="bg_color").id
			atypefc_id = Attributetype.objects.get(title="font_color").id
			allattri = Attribute.objects.all()
			print fontcolor,atypefc_id,"test"
			if bgcolor:
				for each in allattri:
					if each.subject_id == a_id and each.attributetype_id == atypebg_id:
						each.svalue = bgcolor
					        each.save()
			if fontcolor:
				for each in allattri:
					if each.subject_id == a_id and each.attributetype_id == atypefc_id:
						each.svalue = fontcolor
					        each.save()
			vars=RequestContext(request,{})
			template="gstudio/userpreference.html"
			return HttpResponseRedirect("/home/")
			
						
			


	usergbobject = Gbobject.objects.filter(title=user+"_preference")
	if usergbobject:
		usergbobject = Gbobject.objects.get(title=user+"_preference")
		usergbobjectattribute = usergbobject.get_attributes()
		if usergbobjectattribute:
			bgc = ""
			fc = ""
			for key in usergbobjectattribute.keys():
				if key == 'bg_color':
					bgc = str(usergbobjectattribute['bg_color'][0])
				if key == 'font_color':
					fc =  str(usergbobjectattribute['font_color'][0])
			if bgc or fc :
				print "edit"
				vars = RequestContext(request,{'bgcolor':bgc,'fontcolor':fc,'edit':'edit'})
				template="gstudio/userpreference.html"
				return render_to_response(template, vars)
		
					
		
        vars=RequestContext(request,{'show':'show'})
        template="gstudio/userpreference.html"
        return render_to_response(template, vars)
	
