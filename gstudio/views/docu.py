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
from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.settings import *
from gstudio.models import *
from objectapp.models import *

def docu(request):
	p=Objecttype.objects.get(title="Document")
	q=p.get_nbh['contains_members']
	if request.method=="POST":
		user = request.POST.get("user","")
		sdoc = request.POST.get("sdoc","")
		dn = request.POST.get("dn","")
		sub3 = request.POST.get("mydropdown","")
		rating = request.POST.get("star1","")
		docid = request.POST.get("docid","")
		delete = request.POST.get("delete","")
		if rating :
        	 	rate_it(int(docid),request,int(rating))
		if delete != "":
			each=q.get(id=dn)
			each.delete()
			ti=each.title
			os.system("rm -f "+MEDIA_ROOTNEW+'/'+ti)
			p=Objecttype.objects.get(title="Document")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'documents':q,'val':sdoc})
			template="gstudio/docu.html"
			return render_to_response(template, vars)
		if sub3 != "":
			if sdoc != "":
				vidon = Objecttype.objects.get(title="Document")
				vido_new = vidon.get_nbh['contains_members']
				vido = vido_new.filter(title__contains=sdoc)
				vido2 = vido.order_by(sub3)
				variables = RequestContext(request,{'documents':vido2,'val':sdoc})
				template = "gstudio/docu.html"
				return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Document")
				vido_new = vidon.get_nbh['contains_members']
				vido=vido_new.order_by(sub3)
				variables = RequestContext(request,{'documents':vido,'val':sdoc})
				template = "gstudio/docu.html"
				return render_to_response(template, variables)
		a=[]
		for each in request.FILES.getlist("doc[]",""):
			a.append(each)
		if a != "":
			for f in a:
				save_file(f)
				create_object(f,user)
			vars=RequestContext(request,{'documents':q})
			template="gstudio/docu.html"
			return render_to_response(template, vars)	
	vars=RequestContext(request,{'documents':q})
	template="gstudio/docu.html"
	return render_to_response(template, vars)

def save_file(file, path=""):
	filename = file._get_name()
    	fd = open('%s/%s' % (MEDIA_ROOTNEW2, str(path) + str(filename)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()

def create_object(file,log):
	p=Gbobject()
	p.title=file._get_name()
	p.rurl=MEDIA_ROOTNEW2+"p.title"
	final = ''
	for each1 in p.title:
		if each1==".":
			final=final+'-'
		elif each1==" ":
			final=final+'-'
		else:
			final = final+each1	
	p.slug=final
	p.content=' '
	p.status=2
	p.save()
	p.sites.add(Site.objects.get_current())
	p.save()
	s=Author.objects.get(username=log)
	p.authors.add(s)
	p.save()
	q=Objecttype.objects.get(title="Document")
	p.objecttypes.add(Objecttype.objects.get(id=q.id))
	p.save()

def rate_it(topic_id,request,rating):
	ob = Gbobject.objects.get(id=topic_id)
	ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
	return True
