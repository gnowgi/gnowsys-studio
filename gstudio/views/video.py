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

#!/usr/bin/python
import time;
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ox
import os
from gstudio.models import *
from objectapp.models import *
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from demo.settings import *
from gstudio.methods import *
from django.contrib.auth import authenticate

def video(request):
	api=ox.api.API("http://wetube.gnowledge.org/api")
	p=Objecttype.objects.get(title="Video")
	q=p.get_nbh['contains_members']
	sd = request.user
	message = ''
	sd = str(sd)
	password = request.POST.get("upload","")
	content= request.POST.get("contenttext","")
	if request.method == 'POST':
		clip = request.FILES.get("clip","")
		content= request.POST.get("contenttext","")
		svid = request.POST.get("svid","")
		sub1 = request.POST.get("norm","")
		sub2 = request.POST.get("spe","")
		rating = request.POST.get("star1","")
		vidid = request.POST.get("vidid","")
		user = request.POST.get("user","")
		userpassword = request.POST.get("userpassword","")
		useremail = request.POST.get("useremail","")
		sub3 = request.POST.get("mydropdown","")
		favid=request.POST.get("favid","")
		favusr=request.POST.get("favusr","")
		fav=request.POST.get("fav","")
		full=request.POST.get("full","")
		author=request.POST.get("authorname","")
		date = request.POST.get("datename","")
		rate = request.POST.get("ratename","")
		contentname = request.POST.get("contentname","")
		mapname = request.POST.get("mapname","")
		wename = request.POST.get("wename","")
		titlename = request.POST.get("titlename","")
		addtags = request.POST.get("addtags","")
		texttags = request.POST.get("texttags","")
		password = request.POST.get("videopassword","")
		if rate == '0':
		   rate = 'No rating yet'
		else :
		   rate = rate

		if full!="" :
			i=Gbobject.objects.get(id=vidid)
			variables= RequestContext(request,{'id':full,'postedby':author,'date':date,'rateby':rate,'map':mapname,'we':wename,'vidid':vidid ,'titlename':titlename,'contentname':contentname,'video':i})
			template="gstudio/transcript.html"
			return render_to_response(template,variables)
		if fav != "" :
			list1=[]
			t=Gbobject.objects.get(title=user+"video")
			for each in t.get_nbh['has_favourite']:
				d=each.right_subject_id
				x=Gbobject.objects.get(id=d)
				list1.append(x)
			variables = RequestContext(request,{'vids':list1,'val':svid,'fav':fav})
			template = "gstudio/video.html"
			return render_to_response(template, variables)	
		if rating :
        	 	rate_it(int(vidid),request,int(rating))
		
		if favid!="":
                        e=0
                        r = Objecttype.objects.get(title="user")
                        for each in r.get_nbh['contains_members']:
                                if favusr+"video" == each.title:
                                    e=1
                        if e==0 :
				t=Gbobject()
                                t.title=favusr+"video"
                                t.slug=favusr+"video"
                                t.content=' '
                                t.status=2
                                t.save()
                                t.objecttypes.add(Objecttype.objects.get(title="user"))
                                t.save()
                        t=Gbobject.objects.get(title=favusr+"video")
                        rel=Relation()
                        rt=Relationtype.objects.get(title="has_favourite")
                        rel.relationtype_id=rt.id
                        f1=Gbobject.objects.get(id=favid)
                        rel.left_subject_id=t.id
                        rel.right_subject_id=f1.id
                        rel.save()
			t.save()

		
		if addtags != "":
			i=Gbobject.objects.get(id=vidid)
			i.tags = i.tags+ ","+str(texttags)
			i.save()


		if clip != "":
			api.signup({'username':user,'password':password,'email':useremail})
			save_file(clip,user)
			clipname = clip._get_name()
			i=0
			dirname = ""
			while clipname[i] != ".":
				dirname = dirname + clipname[i]
				i=i+1
			y=str(dirname)
			x=str(clipname[0]).upper()
			CreateConfig(user,password)
			# os.system("pandora_client config")
			os.system("pandora_client add_volume "+ user+" "+MEDIA_ROOTNEW+"/"+user )
			os.system("pandora_client scan")
			os.system("pandora_client sync")
			os.system("pandora_client upload") 
			wclip= api.find({'sort': [{'key': 'title','operator': '+'}],'query': {'conditions': [{'key': 'title','value': y,'operator': '='}],'operator': '&'},'keys': ['id', 'title','user','duration','sourcedescription','created'],'range': [0,100]})
			for each in wclip['data']['items']:
      				m=Gbobject()
				m.title=each['title'].lower()
				m.rurl="http://wetube.gnowledge.org/"+each['id']+'/480p.webm'
				m.slug=each['id']
				m.content_org=content
				m.status=2
				m.save()
				m.sites.add(Site.objects.get_current())
				m.save()
				m.objecttypes.add(Objecttype.objects.get(id=p.id))
				m.save()
				a=Attribute()
				a.attributetype=Attributetype.objects.get(title="posted_by")
				a.subject=m
				a.svalue=user
				a.save()
				a1=Attribute()
				a1.attributetype=Attributetype.objects.get(title="time_limit")
				a1.subject=m
				a1.svalue=each['duration']
				a1.save()
				a2=Attribute()
				a2.attributetype=Attributetype.objects.get(title="creation_day")
				a2.subject=m
				a2.svalue=each['created']
				a2.save()
				a3=Attribute()
				a3.attributetype=Attributetype.objects.get(title="source")
				a3.subject=m
				a3.svalue=each['sourcedescription']
				a3.save()
				a4=Attribute()
				a4.attributetype=Attributetype.objects.get(title="map_link")
				a4.subject=m
				l=each['sourcedescription']
				final=''
				for each in l:
					if each==" ":
						final=final+'+'
					else:
						final=final+each
				a4.svalue=final
				a4.save()
				m.save()
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
			 	m.content = newdata
			 	m.save()				
			
			
					
		if sub3 != "":
			if svid != "":
				if sub2 == "":
				
					vidon = Objecttype.objects.get(title="Video")
					vido_new = vidon.get_nbh['contains_members']
					vido = vido_new.filter(title__contains=svid)
					if sub3 == 'title':
						vido2 = vido.order_by(sub3)
					else:
						vido2 = sort_video(vido)
					variables = RequestContext(request,{'vids':vido2,'val':svid})
					template = "gstudio/video.html"
					return render_to_response(template, variables)
				else:
					vidon = Objecttype.objects.get(title="Video")
					vido_new = vidon.get_nbh['contains_members']
					vido = vido_new.filter(slug__contains=svid)
					if sub3 == 'title':
						vido2 = vido.order_by(sub3)
					else:
						vido2 = sort_video(vido)
					variables = RequestContext(request,{'vids':vido2,'val':svid})
					template = "gstudio/video.html"
					return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Video")
				vido_new = vidon.get_nbh['contains_members']
				if sub3 == 'title':
					vido=vido_new.order_by(sub3)
				else:
					vido=sort_video(vido_new)
				variables = RequestContext(request,{'vids':vido,'val':svid })
				template = "gstudio/video.html"
				return render_to_response(template, variables)
	api.signin({'username': sd,'password':password})
	r= api.find({'sort': [{'key': 'title','operator': '+'}],'query': {'conditions': [{'key': 'title','value': '','operator': ''}],'operator': '&'},'keys': ['id', 'title','user','created','duration','sourcedescription'],'range': [0,100]})
	s=r['data']['items']
	for each in s:
		flag=0
		for vid in q:
			if vid.title==each['title'].lower():
				flag=1
		if flag==0:
			m=Gbobject()
			m.title=each['title'].lower()
			m.rurl="http://wetube.gnowledge.org/"+each['id']+'/480p.webm'
			m.slug=each['id']
			m.content=content
			m.status=2
			m.save()
			m.sites.add(Site.objects.get_current())
			m.save()
			m.objecttypes.add(Objecttype.objects.get(id=p.id))
			m.save()
			a=Attribute()
			a.attributetype=Attributetype.objects.get(title="posted_by")
			a.subject=m
			a.svalue=each['user']
			a.save()
			a1=Attribute()
			a1.attributetype=Attributetype.objects.get(title="time_limit")
			a1.subject=m
			a1.svalue=each['duration']
			a1.save()
			a2=Attribute()
			a2.attributetype=Attributetype.objects.get(title="creation_day")
			a2.subject=m
			a2.svalue=each['created']
			a2.save()
			a3=Attribute()
			a3.attributetype=Attributetype.objects.get(title="source")
			a3.subject=m
			a3.svalue=each['sourcedescription']
			a3.save()
			a4=Attribute()
			a4.attributetype=Attributetype.objects.get(title="map_link")
			a4.subject=m
			l=each['sourcedescription']
			final=''
			for each in l:
				if each==" ":
					final=final+'+'
				else:
					final=final+each
			a4.svalue=final
			a4.save()
			m.save()
	svid=""
	q=p.get_nbh['contains_members']
	variables = RequestContext(request,{'vids':q,'val':svid})
	template = "gstudio/video.html"
	return render_to_response(template, variables)	

def save_file(file, user,path=""):
	filename = file._get_name()
       	i=0
	dirname = ""
	while filename[i] != ".":
		dirname = dirname + filename[i]
		i=i+1
	x=str(filename[0]).upper()
	y=str(dirname)
	z = ''
	for each1 in y:
		if each1==" ":
			z=z+'\ '
		else:
			z=z+each1
        fileuser = str(user)
	os.system("mkdir -p "+ MEDIA_ROOTNEW+"/"+fileuser+"/"+x+"/"+z)
    	fd = open('%s/%s/%s/%s/%s' % (MEDIA_ROOTNEW,str(fileuser), str(filename[0]).upper(), str(dirname), str(path) + str(filename)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()
        return 
		
			
			

def sort_video(video):
	a = []
	i = 0
	for each in video:
		a.append(each)
	while i < video.count()-1:
    		min = i
    		j = i+1
    		while j < video.count():
			if a[min].get_nbh['creation_day'][0] > a[j].get_nbh['creation_day'][0] :
            			min = j
        		j = j+1
		temp = a[i]
		a[i] = a[min]
		a[min] = temp
		i = i+1
	return a



def CreateConfig(user,password):
    myfile = open(VIDEO_PANDORA_URL,'w')
    myfile = open(VIDEO_PANDORA_URL,'a')
    myfile.write('{ \n "username":"'+user+'", \n "url":"http://wetube.gnowledge.org/api/",\n"cache": "~/.ox/client.sqlite",\n"media-cache": "~/.ox/media",\n"volumes":{},\n"password":"'+password+'"\n }')
    myfile.close()
    


def show(request,videoid):
	if request.method == 'POST':
		svid = request.POST.get("svid","")
		rating = request.POST.get("star1","")
		vidid = request.POST.get("vidid","")
		user = request.POST.get("user","")
		favid=request.POST.get("favid","")
		favusr=request.POST.get("favusr","")
		addtags = request.POST.get("addtags","")
		texttags = request.POST.get("texttags","")
		contenttext = request.POST.get("contenttext","")
		if rating :
        	 	rate_it(int(vidid),request,int(rating))
		
		if favid!="":
                        e=0
                        r = Objecttype.objects.get(title="user")
                        for each in r.get_nbh['contains_members']:
                                if favusr+"video" == each.title:
                                    e=1
                        if e==0 :
				t=Gbobject()
                                t.title=favusr+"video"
                                t.slug=favusr+"video"
                                t.content=' '
                                t.status=2
                                t.save()
                                t.objecttypes.add(Objecttype.objects.get(title="user"))
                                t.save()
                        t=Gbobject.objects.get(title=favusr+"video")
                        rel=Relation()
                        rt=Relationtype.objects.get(title="has_favourite")
                        rel.relationtype_id=rt.id
                        f1=Gbobject.objects.get(id=favid)
                        rel.left_subject_id=t.id
                        rel.right_subject_id=f1.id
                        rel.save()
			t.save()

		
		if addtags != "":
			i=Gbobject.objects.get(id=vidid)
			i.tags = i.tags+ ","+str(texttags)
			i.save()
		if contenttext !="":
			 edit_description(vidid,contenttext)		
	gbobject = Gbobject.objects.get(id=videoid)
	vars=RequestContext(request,{'video':gbobject})
	template="gstudio/transcript.html"
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
