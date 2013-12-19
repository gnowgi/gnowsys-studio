from gstudio.models import *
from objectapp.models import *
from tagging.models import *

def puttagsearch(f,s,o):
    first=f
    second=s
    oprtn=o
 
    tag1=Tag.objects.filter(name=first)
    if tag1:
        tag1=Tag.objects.get(name=first)
        ft=tag1.name
    tag2=Tag.objects.filter(name=second)
    if tag2:
        tag2=Tag.objects.get(name=second)
        st=tag2.name
    fl=0

    if oprtn=="":
        if tag1 or tag2:
            fl=1
    lst={}
    flst={}
    if oprtn=="AND" or fl==1:
        if tag1:
            for each in Gbobject.objects.all():
                if ft in each.tags:
                    lst[each]=each.get_view_object_url
                    if not tag2:
                       flst=lst
        if tag2 and tag1:
            for each1 in lst:
                if st in each1.tags:
                    flst[each1]=each1.get_view_object_url
        else:
            if tag2:
                for each in Gbobject.objects.all():
                    if st in each.tags:
                        flst[each]=each.get_view_object_url
    if oprtn=="OR":
        if tag1:
            for each in Gbobject.objects.all():
                if ft in each.tags:
                    flst[each]=each.get_view_object_url
        if tag2:
            for each1 in Gbobject.objects.all():
                if st in each1.tags:
                    flst[each1]=each1.get_view_object_url
    print flst
