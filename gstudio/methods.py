from gstudio.models import *
from objectapp.models import *
from django.template.defaultfilters import slugify
import datetime

def delete(idnum):
 del_ob = Gbobject.objects.get(id=idnum)
 del_ob.delete()
 return True

def make_rep_object(title,auth_id):
 new_ob = Gbobject()
 new_ob.title = title
 new_ob.status = 2
 new_ob.slug = slugify(title)
 new_ob.content = ""
 new_ob.save()
 new_ob.objecttypes.add(Objecttype.objects.get(title="Reply"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob

def make_topic_object(title,auth_id,content):
 new_ob = Gbobject()
 new_ob.title = title
 new_ob.status = 2
 new_ob.slug = slugify(title)
 new_ob.content = content
 new_ob.save()
 new_ob.objecttypes.add(Objecttype.objects.get(title="Topic"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob

def make_relation(rep,id_no,idusr):
 r = make_rep_object(rep,idusr)
 t = Gbobject.objects.get(id=id_no)
 t.posterior_nodes.add(r)
 r.prior_nodes.add(t)
 return True

def rate_it(topic_id,request,rating):
 ob = Gbobject.objects.get(id=topic_id)
 ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
 return True


def create_meeting(title,idusr,content):
 sys = System()
 sys.title = title
 sys.status = 2
 sys.content = content
 sys.slug = slugify(title)
 sys.save()
 sys.systemtypes.add(Systemtype.objects.get(title="Meeting"))
 sys.authors.add(Author.objects.get(id=idusr))
 
 a = Attribute()
 a.title = "released button of " + title
 a.slug = slugify(a.title)
 a.content = a.slug
 a.status = 2
 a.subject = sys
 a.svalue = "False"
 a.attributetype_id = Attributetype.objects.get(title="release").id
 a.save()
 sys1 = System()
 sys1.title = "message box of " + title
 sys1.status = 2
 sys1.content = "contains messages of " + title
 sys1.slug = slugify(title)
 sys1.save()
 sys1.systemtypes.add(Systemtype.objects.get(title="message_box"))
 sys.system_set.add(sys1)
 sys.member_set.add(Author.objects.get(id=idusr))
 sys.sites.add(Site.objects.get_current())
 sys1.sites.add(Site.objects.get_current())
 return sys.id
def make_att_true(meet_ob):
 for each in  meet_ob.subject_of.all():
	if(each.attributetype.title=='release'):
		each.svalue = "true"
 	 	meet_ob.subject_of.add(each) 
		break

def make_att_false(meet_ob):
 for each in  meet_ob.subject_of.all():
	if(each.attributetype.title=='release'):
 		each.svalue = ""
		meet_ob.subject_of.add(each)
		break
def schedule_time(stTime, endTime, sys_id):
	 sys=System.objects.get(id=sys_id)
	 atty1=Attributetype.objects.get(title='timeofstart')
         atty2=Attributetype.objects.get(title='timeofend')
         ate= AttributeDateTimeField()
         ats= AttributeDateTimeField()
         ats.title='starttime of '+ sys.title;ats.slug=slugify(ats.title);
	 ats.subject=sys; ats.value=stTime; ats.attributetype=atty1;
         ate.title='endtime of '+ sys.title;ate.slug=slugify(ate.title);
         ate.subject=sys; ate.value=endTime; ate.attributetype=atty2;
	 ate.save()
	 ats.save()
	 sys.save()
	 return  sys.id
def get_time(sys_id):
	later = False
	meetover = False
	sys=System.objects.get(id=sys_id)
        now=datetime.datetime.now()
        for each in AttributeDateTimeField.objects.all():
                if(each.attributetype.title=='timeofstart' and each.subject.title==sys.title):
                        starttime=each.value
		        if (now - starttime)< datetime.timedelta (minutes = 1):
		                later=True
        		else:
                		later = False

                if(each.attributetype.title=='timeofend' and each.subject.title==sys.title):
                        endtime=each.value
		        if(now-endtime)>datetime.timedelta(minutes=1):
		                meetover=True
        		else:
                		meetover=False
	return (later, meetover, starttime, endtime)
def del_comment(comment_id):
 ob = Gbobject.objects.get(id=int(comment_id))
 for each in ob.posterior_nodes.all():
	a= each.id
	del_comment(a)
 ob.delete()
 return True

def del_topic(topic_id):
 ob = Gbobject.objects.get(id=int(topic_id))
 for each in ob.posterior_nodes.all():
	del_comment(each.id)
 ob.delete()
 return True
