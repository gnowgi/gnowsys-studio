
from django.http import *
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import modelform_factory

from objectapp.models import *
from objectapp.forms import *

from gstudio.models import *
from gstudio.admin.forms import *

def MakeForm(model_cls, *args, **kwargs):
	class ContextForm(ModelForm):
		class Meta:
			model = model_cls.values()[0]
			fields = ('value',)
		def __init__(self, *args, **kwargs):
			super(ContextForm,self).__init__(*args, **kwargs)
		 	
			
	return ContextForm(*args, **kwargs)

def dynamic_save(request, attit, memtit):
	rdict ={}
	savedict = {}
	memtit = NID.objects.get(title = str(memtit))
	name = memtit.ref
	absolute_url_node = name.get_absolute_url()
	at = Attributetype.objects.get(title = str(attit))
	dt = str(at.get_dataType_display())
	MyModel = eval('Attribute'+dt)
	rdict.update({str(at.title):MyModel})
	if request.method == 'POST':	
		form = MakeForm(rdict,request.POST)
		if form.is_valid():
			value = form.cleaned_data['value']			
			savedict = {'title':value,'slug':value,'svalue':value,'subject':memtit, 'attributetype':at,'value':value}
			att = MyModel.objects.create(**savedict)
			att.save()
			return HttpResponseRedirect(absolute_url_node)	

	else:
		form = MakeForm(rdict)

	template = "objectapp/fillAT.html"
	context = RequestContext(request,{'form' : form,'title':str(attit), 'absolute_url_node':absolute_url_node}) 
	return render_to_response(template,context)




