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
import os
from gstudio.methods import *

def image(request):
	p=Objecttype.objects.get(title="Image")
	q=p.get_nbh['contains_members']
	if request.method=="POST":
		title = request.POST.get("title1","")
		content= request.POST.get("contenttext","")
		simg = request.POST.get("simg","")
		sub3 = request.POST.get("mydropdown","")
		user = request.POST.get("user","")
		delete = request.POST.get("delete","")
		rating = request.POST.get("star1","")
		imgid = request.POST.get("imgid","")
		pict = request.POST.get("pict","")
		fulid = request.POST.get("fulid","")
		show = request.POST.get("Show","")
		addtags = request.POST.get("addtags","")
		texttags = request.POST.get("texttags","")
		contenttext = request.POST.get("contenttext","")
		if show != "":
			i=Gbobject.objects.get(id=fulid)
			vars=RequestContext(request,{'image':i})
			template="gstudio/fullscreen.html"
			return render_to_response(template, vars)
		if rating :
        	 	rate_it(int(imgid),request,int(rating))
		if delete != "":
			each=q.get(id=pict)
			each.delete()
			ti=each.title
			os.system("rm -f "+MEDIA_ROOTNEW+'/'+ti)
			p=Objecttype.objects.get(title="Image")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'images':q,'val':simg})
			template="gstudio/image.html"
			return render_to_response(template, vars)
		if sub3 != "":
			if simg != "":
				vidon = Objecttype.objects.get(title="Image")
				vido_new = vidon.get_nbh['contains_members']
				vido = vido_new.filter(title__contains=simg)
				vido2 = vido.order_by(sub3)
				variables = RequestContext(request,{'images':vido2,'val':simg})
				template = "gstudio/image.html"
				return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Image")
				vido_new = vidon.get_nbh['contains_members']
				vido=vido_new.order_by(sub3)
				variables = RequestContext(request,{'images':vido,'val':simg})
				template = "gstudio/image.html"
				return render_to_response(template, variables)


		if addtags != "":
			i=Gbobject.objects.get(id=imgid)
			i.tags = i.tags+ ","+str(texttags)
			i.save()

		
		a=[]
		for each in request.FILES.getlist("image[]",""):
			a.append(each)
		if a != "":
			i=0
			for f in a:
				if i==0:
					save_file(f,title,user)
					create_object(f,user,title,content)
					i=i+1
				else:	
					save_file(f,title+'_'+str(i),user)
					create_object(f,user,title+'_'+str(i),content)
					i=i+1
			p=Objecttype.objects.get(title="Image")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'images':q})
			template="gstudio/image.html"
			return render_to_response(template, vars)	
	vars=RequestContext(request,{'images':q,'val':""})
	template="gstudio/image.html"
	return render_to_response(template, vars)

def save_file(file,title, user, path=""):
	filename = title
	os.system("mkdir -p "+ MEDIA_ROOTNEW2+"/"+user)
    	fd = open('%s/%s/%s' % (MEDIA_ROOTNEW2, str(user),str(path) + str(file)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()

def create_object(f,log,title,content):
	p=Gbobject()
	filename = str(f)
	p.title=title
	p.image=log+"/"+filename
	final = ''
	for each1 in filename:
		if each1==" ":
			final=final+'-'
		else:
			final = final+each1	
	i=0
	dirname = ""
	while final[i] != ".":
		dirname = dirname + final[i]
		i=i+1
	p.slug=dirname
	p.content_org=content
	p.status=2
	p.save()
	p.sites.add(Site.objects.get_current())
	p.save()
	s=Author.objects.get(username=log)
	p.authors.add(s)
	p.save()
	q=Objecttype.objects.get(title="Image")
	p.objecttypes.add(Objecttype.objects.get(id=q.id))
	p.save()
	new_ob = content
 	myfile = open('/tmp/file.org', 'w')
 	myfile.write(new_ob)
	myfile.close()
	myfile = open('/tmp/file.org', 'r')
	myfile.readline()
	myfile = open('/tmp/file.org', 'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open('/tmp/file.org', 'r')
	stdout = os.popen(PYSCRIPT_URL_GSTUDIO)
	output = stdout.read()
	data = open("/tmp/file.html")
 	data1 = data.readlines()
 	data2 = data1[72:]
 	data3 = data2[:-3]
 	newdata=""
 	for line in data3:
        	newdata += line.lstrip()
 	p.content = newdata
 	p.save()

def rate_it(topic_id,request,rating):
	ob = Gbobject.objects.get(id=topic_id)
	ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
	return True

def show(request,imageid):
	if request.method=="POST":
		rating = request.POST.get("star1","")
		imgid = request.POST.get("imgid","")
		addtags = request.POST.get("addtags","")
		texttags = request.POST.get("texttags","")
		contenttext = request.POST.get("contenttext","")
		if rating :
	       	 	rate_it(int(imgid),request,int(rating))
		if addtags != "":
			i=Gbobject.objects.get(id=imgid)
			i.tags = i.tags+ ","+str(texttags)
			i.save()
		if contenttext !="":
			 edit_description(imgid,contenttext)
	gbobject = Gbobject.objects.get(id=imageid)
	vars=RequestContext(request,{'image':gbobject})
	template="gstudio/fullscreen.html"
	return render_to_response(template,vars)

def edit_description(sec_id,title):
	new_ob = Gbobject.objects.get(id=int(sec_id))
	new_ob.content_org = title
	myfile = open('/tmp/file.org', 'w')
	myfile.write(new_ob.content_org)
	myfile.close()
	myfile = open('/tmp/file.org', 'r')
	myfile.readline()
	myfile = open('/tmp/file.org', 'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open('/tmp/file.org', 'r')
	stdout = os.popen(PYSCRIPT_URL_GSTUDIO)
	output = stdout.read()
	data = open("/tmp/file.html")
	data1 = data.readlines()
	data2 = data1[72:]
	data3 = data2[:-3]
	newdata=""
	for line in data3:
		newdata += line.lstrip()
	new_ob.content = newdata
	new_ob.save()
	return True
