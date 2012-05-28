
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.forms import ModelForm

from gstudio.models import *
from objectapp.models import *

def context_member(request,reltit , memtit):

    member = []
    subtype = []
    subtypemember = []
    finaldict = {}
    nt = []
    parenttype = []

#-------------------------------------------------------------
    if Objecttype.objects.filter(title = str(memtit)):
        ot = Objecttype.objects.get(title = str(memtit))
        absolute_url_node = ot.get_absolute_url()
    elif Gbobject.objects.filter(title = str(memtit)):
        ot = Gbobject.objects.get(title = str(memtit))
        absolute_url_node = ot.get_absolute_url()
#--------------------------------------------------------------

    if Relationtype.objects.filter(title = str(reltit)):
        r =Relationtype.objects.get(title = str(reltit))
        role = r.left_subjecttype.ref        
        roletype = str(r.left_applicable_nodetypes)
        print "Original is left role of relation"
        newrole = r.right_subjecttype.ref
        newroletype = str(r.right_applicable_nodetypes)
        print 'original ' ,str(role)
        print 'newrole (i.e right)', str(newrole)

    else:
        r = Relationtype.objects.get(inverse = str(reltit))
        role = r.right_subjecttype.ref
        roletype = str(r.right_applicable_nodetypes)
        print "Original is right role of relation"
        newrole = r.left_subjecttype.ref
        newroletype = str(r.left_applicable_nodetypes)
        print 'original ' ,str(role)
        print 'newrole (i.e left)', str(newrole)


#---------------------------------------------------------------------

    if newrole.reftype == 'Objecttype' and newroletype == 'OT':
        print "Objecttype and OT"
        for i in newrole.get_members:
            member.append(i)

        for i in member:
            finaldict.update({i.id:str(i.title)})

        # for i in newrole.get_children():
        #     subtype.append(i.ref)
        for i in newrole.get_descendants():
            subtype.append(i.ref)

        for i in subtype:
            finaldict.update({i.id:str(i.title)})

        for i in subtype:
            subtypemember.append(i.get_members)
            
        subtypemember = [num for elem in subtypemember for num in elem] 

        for i in subtypemember:
            finaldict.update({i.id:str(i.title)})

        finaldict.update({newrole.id:str(newrole.title)})

    elif newrole.reftype == 'Gbobject' and newroletype == 'OB':
        print "Gbobject and OB"
        nt = newrole.objecttypes.all()

        for i in nt:
            parenttype.append(i.ref)
        
        for i in parenttype:
            member.append(i.get_members)
              
        member = [num for elem in member for num in elem] 
        subtypent = []

        # for i in parenttype:
        #     subtypent.append(i.get_children())
        # subtypent = [num for elem in subtypent for num in elem]

        # for i in subtypent:
        #     subtype.append(i.ref)
        # subtype = [num for elem in subtype for num in elem]

        for i in parenttype:
            subtypent.append(i.get_descendants())

        for i in subtypent:
            subtype.append(i.ref)

        for i in subtype:
            subtypemember.append(i.get_members)
        subtypemember = [num for elem in subtypemember for num in elem]
              

        for i in member:
            finaldict.update({i.id:str(i.title)})

        for i in subtypemember:
            finaldict.update({i.id:str(i.title)})

    elif newrole.reftype == 'Objecttype' and newroletype == 'OB':        
        print "Objecttype and OB"
        for i in newrole.get_members:
            member.append(i)

        for i in member:
            finaldict.update({i.id:str(i.title)})

        # for i in newrole.get_children():
        #     subtype.append(i.ref)

        for i in newrole.get_descendants():
            subtype.append(i.ref)
        for i in subtype:
            subtypemember.append(i.get_members)
                     
        subtypemember = [num for elem in subtypemember for num in elem] 

        for i in subtypemember:
            finaldict.update({i.id:str(i.title)})
            
        print 'member',str(member)
        print 'subtype', str(subtype)
        print 'subtypemember', str(subtypemember)
    elif newrole.reftype == 'Gbobject' and newroletype == 'OT':
        print "Gbobject and OT"
        nt = newrole.objecttypes.all()
        for i in nt:
            parenttype.append(i.ref)
        
        for i in parenttype:
            member.append(i.get_members)
              
        member = [num for elem in member for num in elem] 
        subtypent = []

        # for i in parenttype:
        #     subtypent.append(i.get_children())
        # subtypent = [num for elem in subtypent for num in elem]

        # for i in subtypent:
        #     subtype.append(i.ref)
        # subtype = [num for elem in subtype for num in elem]
        for i in parenttype:
            subtypent.append(i.get_descendants())

        for i in subtypent:
            subtype.append(i.ref)
        
        for i in subtype:
            subtypemember.append(i.get_members)
        subtypemember = [num for elem in subtypemember for num in elem]
              

        for i in subtype:
            finaldict.update({i.id:str(i.title)})

        for i in parenttype:
            finaldict.update({i.id:str(i.title)})

        for i in member:
            finaldict.update({i.id:str(i.title)})

        for i in subtypemember:
            finaldict.update({i.id:str(i.title)})


    print 'absolute_url_node', str(absolute_url_node)
    template="objectapp/selectRT.html"
    context = RequestContext(request,{'finaldict':finaldict,'gb':memtit,'reltit':reltit, 'absolute_url_node': absolute_url_node})
    return render_to_response(template,context)


def context_save(request,leftmem, reltype, rightmem):
    try:
        leftmem = str(leftmem)
        reltype = str(reltype)
        rightmem = str(rightmem)



        print 'leftmem :', leftmem, 'rightmem :', rightmem
        pt = []
        nt = []

        left = NID.objects.get(title = leftmem)       
        print 'leftid', str(left.id)
        right = NID.objects.get(title = rightmem)
        print 'rightid', str(right.id)        

        if Relationtype.objects.filter(title=reltype):
            relation = Relationtype.objects.get(title = reltype)
        else:
            relation = Relationtype.objects.get(inverse = reltype)

        rightrole = relation.right_subjecttype_id
        r = relation.right_subjecttype.ref
        print 'rightrole', str(r)
        leftrole = relation.left_subjecttype_id
        l=relation.left_subjecttype.ref
        print 'leftrole', str(l)
#-----------------------------------------------------------------------
        flag = 1
        if Objecttype.objects.filter(title = leftmem):
            
            obj = Objecttype.objects.get(title = leftmem)
            print 'OT', str(obj)

            while obj.parent:
                pt.append((obj.parent).ref)
                obj=obj.parent
            for i in range(len(pt)):
                if pt[i].id == leftrole :
                    flag = 0
                    print "Objecttype flag = 0 "
                    break
                else:
                    print "Objecttype flag = 1 "
            
        elif Gbobject.objects.filter(title = leftmem):
            gb = Gbobject.objects.get(title = leftmem)
            print 'Ob', str(gb)
            nt = gb.objecttypes.all()            
            print 'nt ', str(nt)


            for i in range(len(nt)):
                pt.append(nt[i].ref)
                obj = nt[i].ref
                while  obj.parent:
                    pt.append(obj.parent.ref)
                    obj = obj.parent

            print 'pt ', str(pt)
            for i in range(len(pt)):
                if left.id == leftrole or pt[i].id == leftrole:
                    flag = 0
                    print "Object flag = 0"
                    break
                else:
                    print "Object flag = 1"
        print 'pt:',str(pt)
#-----------------------------------------------------------------------------------

        
        if flag == 0:
            print 'left_subject_id', l
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
        return HttpResponseRedirect("/nodetypes/")
        #pass

