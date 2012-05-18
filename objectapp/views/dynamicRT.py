
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.forms import ModelForm

from gstudio.models import *
from objectapp.models import *


def context_member(request,reltit , memtit):

    if Relationtype.objects.filter(title = str(reltit)):
        r =Relationtype.objects.get(title = str(reltit))
    else:
        r = Relationtype.objects.get(inverse = str(reltit))

    gbdict = {}
    otmem=[]
    childpt = []
    childmem = []
    finaldict={}
    memdict = {} #otmem + childmem
	
    if Objecttype.objects.filter(title = str(memtit)):
        flag = 1
        name = Objecttype.objects.get(title = str(memtit))
	#get members of name
        for i in name.get_members:
            otmem.append(i)

	#get children of name
        for i in name.children.all():
            childpt.append(Objecttype.objects.get(title = NID.objects.get(title = i.title)))
	#get child's members
        for i in childpt:
            childmem = i.get_members
        for i in otmem:
            memdict.update({i.id:str(i.title)})
        for i in childmem:	
            memdict.update({i.id:str(i.title)})

    elif Gbobject.objects.filter(title = str(memtit)):
        flag = 0	
        nt = []
        name = Gbobject.objects.get(title = str(memtit))
        nt = name.objecttypes.all() #nodetype
        pt = []
        for i in nt:
            pt.append(Objecttype.objects.get(title = NID.objects.get(title = i.title)))
        for i in pt:
            otmem.append(i.get_members)       

        otmem = [num for elem in otmem for num in elem]
        gbdict.update({name.id :str(name.title)})        

#-----------------------------------------------------------------------
    
    memid = name.id
    if r.left_subjecttype_id == memid:	
        nodetype = str(r.right_applicable_nodetypes)
        print"equal to left"
    else:
        print"equal to right"
        nodetype = str(r.left_applicable_nodetypes)

#------------------------------------------------------------------------

    if nodetype=="OB" and flag==0:# gb itself
        finaldict=gbdict
        for i in otmem:
            finaldict.update({i.id:str(i.title)})
        print "nodetype OB and Flag 0"

    elif nodetype=="OT" and flag==1:#name,name ka child ,member of both
        print "nodetype OT and Flag 1"
        finaldict.update({name.id:str(name.title)})#ot itself 
        for i in childpt:#otchild
            finaldict.update({i.id:str(i.title)})
        for i in range(len(memdict)):#member of both 
            finaldict.update({memdict.keys()[i]:memdict.values()[i]})

    elif nodetype=="OT" and flag==0: #name,name ka ot ,ot ka mem
        print "nodetype OT and Flag 0"
        finaldict.update({name.id:str(name.title)})
        for i in name.objecttypes.all():
            finaldict.update({i.id : str(i.title)})            
        for i in otmem:
            finaldict.update({i.id:str(i.title)})

    elif nodetype=="OB" and flag==1: #child of both
        print "nodetype OB and Flag 1"
        finaldict=memdict
	
    absolute_url_node = name.get_absolute_url()
    print finaldict	
    
    template="objectapp/selectRT.html"
    context = RequestContext(request,{'finaldict':finaldict,'gb':name,'reltit':reltit, 'absolute_url_node': absolute_url_node})
    return render_to_response(template,context)


def context_save(request,leftmem, reltype, rightmem):
    try:
        leftmem = str(leftmem)
        reltype = str(reltype)
        rightmem = str(rightmem)

        left = NID.objects.get(title = leftmem)       
        right = NID.objects.get(title = rightmem)
        
        if Relationtype.objects.filter(title=reltype):
            relation = Relationtype.objects.get(title = reltype)
        else:
            relation = Relationtype.objects.get(inverse = reltype)

        rightrole = relation.right_subjecttype_id
        leftrole = relation.left_subjecttype_id
#-----------------------------------------------------------------------
        flag = 1
        if Objecttype.objects.filter(title = leftmem):
            if left.id == leftrole :
                flag = 0
                print "Objecttype flag = 0 "
            else:
                print "Objecttype flag = 1 "
        elif Gbobject.objects.filter(title = leftmem):
            gb = Gbobject.objects.get(title = leftmem)
            pt = gb.objecttypes.all()
            for i in range(len(pt)):
                if left.id == leftrole or pt[i].id == leftrole:
                    flag = 0
                    print "Object flag = 0"
                else:
                    print "Object flag = 1"

#-----------------------------------------------------------------------------------

        if flag == 0:
            savedict = {'title':relation, 'slug':relation, 'left_subject_id':left.id, 'right_subject_id':right.id, 'relationtype_id':relation.id, 'left_subject_scope':' ', 'right_subject_scope':' ', 'relationtype_scope':' ' }
        else:
            savedict = {'title':relation, 'slug':relation, 'left_subject_id':right.id, 'right_subject_id':left.id, 'relationtype_id':relation.id, 'left_subject_scope':' ', 'right_subject_scope':' ', 'relationtype_scope':' '}
        
        rtt = Relation.objects.create(**savedict)
        rtt.save()
        print "left"+ str(left) + " right" + str(right) + " reltype" +str(relation)+ "    leftrole"+ str(leftrole) +  "   rightrole " + str(rightrole)

        print savedict
    
        return HttpResponseRedirect("/nodetypes/")
        #return savedict
    
    except IntegrityError: #Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails, duplicate key, etc.
        raise Http404()
        #pass

