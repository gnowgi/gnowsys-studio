from gstudio.models import *
from objectapp.models import *
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError


def context_RT(request, gbid):
    pt =[] #contains parenttype
    reltype =[] #contains relationtype
    titledict = {} #contains relationtype's title
    inverselist = [] #contains relationtype's inverse
    finaldict = {} #contains either title of relationtype or inverse of relationtype
    listval=[] #contains keys of titledict to check whether parenttype id is equals to listval's left or right subjecttypeid

    #flag = 0 #check whether OT or OB, flag = 0 means it is OB

    # if its an OT, then parse separately
    if Objecttype.objects.filter(title=str(gbid)):
        flag = 1
    elif Gbobject.objects.filter(title = str(gbid)):
        flag = 0
    elif Systemtype.objects.filter(title = str(gbid)):
        flag = 2

    if flag == 1:
        pt.append(Objecttype.objects.get(title = str(gbid)))
        name = NID.objects.get(title = str(gbid))
        
        for i in range(len(pt)):
            if Relationtype.objects.filter(left_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(left_subjecttype = pt[i].id))    
            if Relationtype.objects.filter(right_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(right_subjecttype = pt[i].id)) 
                
        # it converts 2 or more list as one list
        #reltype = [num for elem in reltype for num in elem] #this rqud for filtering
            
        for i in reltype:
            titledict.update({i:i.id})
            
            
        for i in range(len(titledict)):
            listval.append(Relationtype.objects.get(title = titledict.keys()[i]))
            inverselist.append(titledict.keys()[i].inverse)
            
   
        for j in range(len(pt)):
            for i in range(len(listval)):
                if pt[j].id == listval[i].left_subjecttype_id :
                    finaldict.update({titledict.values()[i]:titledict.keys()[i]})
                elif pt[j].id == listval[i].right_subjecttype_id:
                    finaldict.update({titledict.values()[i]:inverselist[i]})


    elif flag == 0:
        gb= Gbobject.objects.get(title=str(gbid))
        name = gb
        pt = gb.objecttypes.all()
        for i in range(len(pt)):
            if Relationtype.objects.filter(left_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(left_subjecttype = pt[i].id))    
            if Relationtype.objects.filter(right_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(right_subjecttype = pt[i].id)) 
            if Relationtype.objects.filter(left_subjecttype = gb):
                reltype.append(Relationtype.objects.get(left_subjecttype = gb))
            if Relationtype.objects.filter(right_subjecttype = gb):
                reltype.append(Relationtype.objects.get(right_subjecttype = gb))                           

                
        #reltype = [num for elem in reltype for num in elem]
        
        for i in reltype:
            titledict.update({i:i.id})

            
        for i in range(len(titledict)):
            listval.append(Relationtype.objects.get(title = titledict.keys()[i]))
            inverselist.append(titledict.keys()[i].inverse)            
   
        for j in range(len(pt)):
            for i in range(len(listval)):
                if pt[j].id == listval[i].left_subjecttype_id or gb.id == listval[i].left_subjecttype_id :
                    finaldict.update({titledict.values()[i]: titledict.keys()[i]})
                elif pt[j].id == listval[i].right_subjecttype_id or gb.id == listval[i].right_subjecttype_id:
                    finaldict.update({titledict.values()[i]:inverselist[i]})

    elif flag == 2:
        systype = Systemtype.objects.get(title = str(gbid))
        nodelist = []
        nodelist = systype.nodetype_set.all()
        for i in nodelist:
            pt.append(i.ref)
        pt.append(systype)
        name = NID.objects.get(title = str(gbid))
        
        for i in range(len(pt)):
            if Relationtype.objects.filter(left_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(left_subjecttype = pt[i].id))    
            if Relationtype.objects.filter(right_subjecttype = pt[i].id):
                reltype.append(Relationtype.objects.get(right_subjecttype = pt[i].id)) 
                
        # it converts 2 or more list as one list
        #reltype = [num for elem in reltype for num in elem] #this rqud for filtering
            
        for i in reltype:
            titledict.update({i:i.id})
            
            
        for i in range(len(titledict)):
            listval.append(Relationtype.objects.get(title = titledict.keys()[i]))
            inverselist.append(titledict.keys()[i].inverse)
            
   
        for j in range(len(pt)):
            for i in range(len(listval)):
                if pt[j].id == listval[i].left_subjecttype_id :
                    finaldict.update({titledict.values()[i]:titledict.keys()[i]})
                elif pt[j].id == listval[i].right_subjecttype_id:
                    finaldict.update({titledict.values()[i]:inverselist[i]})
        
        
    absolute_url_node = name.get_absolute_url()

    template="objectapp/selectRT.html"
    context = RequestContext(request,{'final':finaldict , 'gb':name ,'gbid':name.id, 'absolute_url_node':absolute_url_node})
    return render_to_response(template,context)


def context_member(request,relid, memid):#id of relationtype, id of selected object
    try:
        relid = int(relid) #relationtype
        memid = int(memid) #left member id
    except:
        raise Http404()

    # checks wheter memid is OT or OB
    flag=0 #means OB

    if Objecttype.objects.filter(id = memid):
        flag=1

    nt =[] #contains parent as <Nodetype:parent>
    pt= [] #contains parent as <Objecttype:parent>

    if flag == 1:
        pt.append(Objecttype.objects.get(id=memid))

    else:
        gb = Gbobject.objects.get(id = memid)
        nt = gb.objecttypes.all()
        for i in range(len(nt)): #conversion of nodetype in objecttype
            pt.append(Objecttype.objects.get(id = nt[i].id))    

    memlist = [] #contains OB and OT for appearing in 1st combo box

    r = Relationtype.objects.get(id = relid) #contains RelationType

    # extracting left and right applicable nodetypes(OB or OT) of RelationType
    lefttype = str(r.left_applicable_nodetypes)
    righttype = str(r.right_applicable_nodetypes)

    if lefttype == righttype:
        if lefttype == "OB" and righttype == "OB":

            if r.left_subjecttype_id == memid:
                memlist.append(Gbobject.objects.get(id = r.right_subjecttype_id))
            else :
                memlist.append(Gbobject.objects.get(id = r.left_subjecttype_id))

        elif lefttype == "OT" and righttype == "OT":
            for each in range(len(pt)):
                if r.left_subjecttype_id == memid or r.left_subjecttype_id == pt[each].id:
                    o = Objecttype.objects.get(title = NID.objects.get(title=(r.right_subjecttype).title))    
                    memlist.append(o)
                    for i in o.get_members:
                        memlist.append(i)
                # elif r.right_subjecttype_id == memid or r.right_subejcttype_id == pt[each].id:
                else:
                    o = Objecttype.objects.get(title = NID.objects.get(title=(r.left_subjecttype).title))    
                    memlist.append(o)
                    for i in o.get_members:
                        memlist.append(i)
    else:
        if r.left_subjecttype_id == memid:
            if righttype == "OB":
                memlist.append(Gbobject.objects.get(id = r.right_subjecttype_id))

            else :
                o = Objecttype.objects.get(title = NID.objects.get(title=(r.right_subjecttype).title)) 
                memlist.append(o)
                for i in o.get_members:
                    memlist.append(i)

        else:
            if lefttype == "OB":
                memlist.append(Gbobject.objects.get(id = r.left_subjecttype_id))

            else : 
                o = Objecttype.objects.get(title = NID.objects.get(title=(r.left_subjecttype).title)) 
                memlist.append(o)
                for i in o.get_members:
                    memlist.append(i)

    memdict = {} #converting list into dict and to set id of right member as hidden field
    for i in memlist:
        memdict.update({i.id:i})
        

    template="objectapp/fillRT.html"
    context = RequestContext(request,{'memdict':memdict})
    return render_to_response(template,context)

def context_save(request,leftmem, reltype, rightmem):
    try:
        leftmem = int(leftmem)
        reltype = int(reltype)
        rightmem = int(rightmem)

        relation = Relationtype.objects.get(id = reltype)
        rightrole = relation.right_subjecttype_id
        leftrole = relation.left_subjecttype_id
        flag = 1
        if Objecttype.objects.filter(id = leftmem):
            if leftmem == leftrole :
                flag = 0
                print "Objecttype flag = 0 "
            else:
                print "Objecttype flag = 1 "
        elif Gbobject.objects.filter(id = leftmem):
            gb = Gbobject.objects.get(id = leftmem)
            pt = gb.objecttypes.all()
            for i in range(len(pt)):
                if leftmem == leftrole or pt[i].id == leftrole:
                    flag = 0
                    print "Object flag = 0"
                else:
                    print "Object flag = 1"
        if flag == 0:
            savedict = {'title':relation, 'slug':relation, 'left_subject_id':leftmem, 'right_subject_id':rightmem, 'relationtype_id':reltype, 'left_subject_scope':' ', 'right_subject_scope':' ', 'relationtype_scope':' ' }
        else:
            savedict = {'title':relation, 'slug':relation, 'left_subject_id':rightmem, 'right_subject_id':leftmem, 'relationtype_id':reltype, 'left_subject_scope':' ', 'right_subject_scope':' ', 'relationtype_scope':' '}
        
        rtt = Relation.objects.create(**savedict)
        rtt.save()
        print "leftmem"+ str(leftmem) + "   rightmem" + str(rightmem) + "    reltype" +str(reltype)+ "    leftrole"+ str(leftrole) +  "   rightrole " + str(rightrole)
        print savedict
    
        return HttpResponseRedirect("/nodetypes/")
        #return savedict
    
    except IntegrityError: #Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails, duplicate key, etc.
        raise Http404()
        #pass

