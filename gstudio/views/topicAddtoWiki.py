from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *

def topicAddtoWiki(request,pageid):
    if request.is_ajax():
        page_ob = System.objects.get(id=pageid)
        title=request.POST['subject']
        idusr=request.POST['idusr']
        usr=request.POST['usr']
	admin_id=request.POST['admin_id']
	print 'data=',title,idusr,usr,pageid
        tp = make_topic_wikiobject(title,int(idusr),usr)	
        System.objects.get(id=int(pageid)).system_set.all()[0].gbobject_set.add(tp)	
	if page_ob.system_set.all():
                 Topic = page_ob.system_set.all()[0].gbobject_set.all()
	print tp
	variables=RequestContext(request,{'topic':Topic,'idusr' : idusr, 'flag' : "True", 'admin_id' : admin_id})
	template = "gstudio/wikiDiscus.html"
   	return render_to_response(template, variables)
	#return HttpResponse("succes")
        #if  tp:
        #   return HttpResponseRedirect('/gstudio/page/gnowsys-grp/'+pageid)


def make_topic_wikiobject(title,auth_id,usr):
    exist_ob=Gbobject.objects.filter(title="Discus: " + title)	
    if not exist_ob:		
    	new_ob = Gbobject()
    	new_ob.title = "Discussion on: " + title
    	new_ob.slug = slugify(title)	
    	new_ob.save()
    	print new_ob.id
   	new_ob.slug = new_ob.slug + "-" + str(new_ob.id)
    	new_ob.save()
    	new_ob.objecttypes.add(Objecttype.objects.get(title="Topic"))
    	new_ob.authors.add(Author.objects.get(id=auth_id))
    	new_ob.sites.add(Site.objects.get_current())
	return new_ob
	#new_ob=Gbobject.objects.get(title=title)
    else:
	return exist_ob
    
