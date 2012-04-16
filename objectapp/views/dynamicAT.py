
from django.http import *
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from objectapp.models import *
from objectapp.forms import *

from gstudio.models import *

def dynamic_view(request):
	rdict = {}
	for j in Gbobject.objects.all():
		rdict.update({j.id:j.title})

	template="objectapp/selectAT.html"
	context= RequestContext(request,{ 'rdict':rdict })
	return render_to_response(template,context)

def dynamic_save(request,tit): #view for gb and ot too
	testlst = []	
	parenttype = []
	attributetype = []
	rdict = {}
	nodelist = []
	syst = []#parent for system 
	try:
		offset = str(tit)
	except ValueError:
		raise Http404()	

	#flag = 0 #means its object
	
	if Objecttype.objects.filter(title = offset):
		flag = 1
	elif Gbobject.objects.filter(title = offset):
		flag = 0
	elif Systemtype.objects.filter(title = offset):
		flag = 2

	if flag == 1:
		parenttype.append(Objecttype.objects.get(title = offset))
		pt_id = NID.objects.get(title = offset) 
		name = pt_id
		
	elif flag == 0:		
		#utit = Gbobject.objects.get(title = offset)
		gb=Gbobject.objects.get(title=offset)	
		name = gb
		# checking whether object is gb or system coz created objects are treated as Gbobject n then System objects
		if System.objects.filter(title = (gb.ref).title):
			gb = System.objects.get(title = offset)
			syst = gb.systemtypes.all()
			for i in syst:
				nodelist = i.nodetype_set.all()
				parenttype.append(i)
		
			for i in nodelist:
				parenttype.append(i.ref)

		elif Gbobject.objects.filter(title = (gb.ref).title):		
			parenttype = gb.objecttypes.all()

		pt_id = NID.objects.get(id = gb.id) 

	elif flag == 2:
		systype = Systemtype.objects.get(title = offset)
		nodelist = systype.nodetype_set.all()
		parenttype.append(Systemtype.objects.get(title = offset))
		for i in nodelist:
			parenttype.append(i.ref)
		pt_id = NID.objects.get(title = offset)
		name = pt_id


	absolute_url_node = name.get_absolute_url()
	for each in parenttype:
		attributetype.append(each.subjecttype_of.all())

	attributetype = [num for elem in attributetype for num in elem]

	for each in range(len(attributetype)):
		rdict.update({attributetype[each]:str(Attributetype.get_dataType_display(attributetype[each]))})
				
	if request.method=='POST':	
		form = ContextForm(rdict,request.POST)
		bound= form.is_bound

		if form.is_valid():
			for key,val in rdict.items():
				testlst.append(str(request.POST[str(key)+"_"+str(val)]))
			
			for val in range(len(testlst)):				
				if testlst[val] != '' :
					savedict = {'title':testlst[val],'slug':testlst[val], 'svalue':testlst[val], 'subject':pt_id, 'attributetype':rdict.keys()[val]}
					att = Attribute.objects.create(**savedict)
					att.save()

			return HttpResponseRedirect(absolute_url_node)
	else:
	 	form = ContextForm(rdict)	
	

	template = "objectapp/fillAT.html"
	context = RequestContext(request,{'form' : form, 'name':name,'absolute_url_node':absolute_url_node})
	return render_to_response(template,context)



# def dynamic_objecttype(request,iden): #gb view for dynamic at 
# 	testlst = []	
# 	attributetype = []
# 	rdict = {}
# 	try:
# 		offset = str(iden)
# 	except ValueError:
# 		raise Http404()

# 	#uid = Gbobject.objects.get(title = offset)
# 	gb=Gbobject.objects.get(title=offset)	
# 	parenttype = gb.objecttypes.all()
# 	pt_id = NID.objects.get(id = gb.id) 


# 	for each in parenttype:
# 		attributetype.append(each.subjecttype_of.all())

# 	attributetype = [num for elem in attributetype for num in elem]

# 	for each in range(len(attributetype)):
# 		rdict.update({attributetype[each]:str(Attributetype.get_dataType_display(attributetype[each]))})
				
# 	if request.method=='POST':	
# 		form = ContextForm(rdict,request.POST)
# 		bound= form.is_bound

# 		if form.is_valid():
# 			for key,val in rdict.items():
# 				testlst.append(str(request.POST[str(key)+"_"+str(val)]))
			
# 			for val in range(len(testlst)):				
# 				if testlst[val] != '' :
# 					savedict = {'title':testlst[val],'slug':testlst[val], 'svalue':testlst[val], 'subject':pt_id, 'attributetype':rdict.keys()[val]}
# 					att = Attribute.objects.create(**savedict)
# 					att.save()

# 			return HttpResponseRedirect("/objects/")
# 	else:
# 	 	form = ContextForm(rdict)	
	

# 	template = "objectapp/fillAT.html"
# 	context = RequestContext(request,{'form' : form})
# 	return render_to_response(template,context)
