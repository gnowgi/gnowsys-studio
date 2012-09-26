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
from PIL import Image
import glob, os
import hashlib
from django.template.defaultfilters import slugify

size = 128, 128
report = "true"
md5_checksum = ""
def image(request):
	p=Objecttype.objects.get(title="Image")
	q=p.get_nbh['contains_members']
	if request.method=="POST":
		title = request.POST.get("title1","")
		content= unicode(request.POST.get("contenttext",""))
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
		texttags = unicode(request.POST.get("texttags",""))
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
			i.tags = i.tags+ ","+(texttags)
			i.save()

		
		a=[]
		reportid=''
		for each in request.FILES.getlist("image[]",""):
			a.append(each)
		if a != "":
			i=0
			for f in a:
				if i==0:
					report,imageeachid = save_file(f,title,user)
					if report == "false":
						reportid = imageeachid
					else:
						create_object(f,user,title,content,str(request.user))
						i=i+1
				else:	
					report,imageeachid = save_file(f,title+'_'+str(i),user)
					if report == "false":
						reportid = imageeachid
					else:
						create_object(f,user,title+'_'+str(i),content,str(request.user))
						i=i+1
			p=Objecttype.objects.get(title="Image")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'images':q,'reportid':reportid,'report':report})
			template="gstudio/image.html"
			return render_to_response(template, vars)	
	vars=RequestContext(request,{'images':q,'val':""})
	template="gstudio/image.html"
	return render_to_response(template, vars)

def save_file(file,title, user, path=""):
        report = "true"
	imageeachid = ''
	filename = title
	slugfile = str(file)
	slugfile=slugfile.replace(' ','_')
	os.system("mkdir -p "+ MEDIA_ROOTNEW2+"/"+user)
    	fd = open('%s/%s/%s' % (MEDIA_ROOTNEW2, str(user),str(path) + str(slugfile)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()
	global md5_checksum
	md5_checksum = md5Checksum(MEDIA_ROOTNEW2+"/"+ str(user)+"/"+slugfile)
	attype = Attributetype.objects.get(title="md5_checksum_image")
	att = Attribute.objects.all()
	flag = 0
	for each in att:
		if each.attributetype.id == attype.id:
			if each.svalue == md5_checksum :
				flag = 1
				imageeachid = each.subject.id
	if flag == 1:
		report = "false"
	else:	
		for infile in glob.glob(MEDIA_ROOTNEW2+"/"+str(user)+"/"+str(slugfile)):
			file, ext = os.path.splitext(infile)
			im = Image.open(infile)
			imm = Image.open(infile)
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(file + "-thumbnail", "JPEG")
			width, height = imm.size
			sizem = 1024,height
			if int(width) > 1024:
				imm.thumbnail(sizem, Image.ANTIALIAS)
				imm.save(file + "_display_1024","JPEG")
			else:
				imm.thumbnail(imm.size,Image.ANTIALIAS)
				imm.save(file + "_display_1024","JPEG")
    	return report,imageeachid	


def create_object(f,log,title,content,usr):
	p=Gbobject()
	filename = str(f)
	filename=filename.replace(' ','_')
	p.title=title
        fname=slugify(title)+"-"+usr
	p.image=log+"/"+filename
	#final = ''
	#for each1 in filename:
	#	if each1==" ":
	#		final=final+'-'
	#	else:
	#		final = final+each1	
	#i=0
	#dirname = ""
	#while final[i] != ".":
	#	dirname = dirname + final[i]
	#	i=i+1
	p.slug=slugify(filename)
	contorg=unicode(content)
	p.content_org=contorg.encode('utf8')
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
 	ext='.org'
        html='.html'
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(p.content_org)
	myfile.close()
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
        rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)
	#myfile.readline()
	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
	output = stdout.read()
	data = open(os.path.join(FILE_URL,fname+html))
 	data1 = data.readlines()
 	data2 = data1[72:]
 	data3 = data2[:-3]
 	newdata=""
 	for line in data3:
        	newdata += line.lstrip()
 	p.content = newdata
 	p.save()
        a=Attribute()
        a.attributetype=Attributetype.objects.get(title="md5_checksum_image")
        a.subject=p
        a.svalue=md5_checksum
        a.save()


def rate_it(topic_id,request,rating):
	ob = Gbobject.objects.get(id=topic_id)
	ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
	return True

def show(request,imageid):
	if request.method=="POST":
		rating = request.POST.get("star1","")
		imgid = request.POST.get("imgid","")
		addtags = request.POST.get("addtags","")
		texttags = unicode(request.POST.get("texttags",""))
		contenttext = unicode(request.POST.get("contenttext",""))
		if rating :
	       	 	rate_it(int(imgid),request,int(rating))
		if addtags != "":
			i=Gbobject.objects.get(id=imgid)
			i.tags = i.tags+ ","+(texttags)
			i.save()
		if contenttext !="":
			 edit_description(imgid,contenttext,str(request.user))
	gbobject = Gbobject.objects.get(id=imageid)
	vars=RequestContext(request,{'image':gbobject})
	template="gstudio/fullscreen.html"
	return render_to_response(template,vars)

def edit_description(sec_id,title,usr):
	new_ob = Gbobject.objects.get(id=int(sec_id))
	contorg=unicode(title)
	ssid=new_ob.get_ssid.pop()
	fname=str(ssid)+"-"+usr
	new_ob.content_org=contorg.encode('utf8')
	ext='.org'
	html='.html'
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(new_ob.content_org)
	myfile.close()
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)
	#myfile.readline()
	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
	
	output = stdout.read()
	data = open(os.path.join(FILE_URL,fname+html))
	data1 = data.readlines()
	data2 = data1[72:]
	data3 = data2[:-3]
	newdata=""
	for line in data3:
		newdata += line.lstrip()
	new_ob.content = newdata
	new_ob.save()
	return True

def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

