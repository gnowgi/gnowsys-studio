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



from django.http import *
from reversion.models import *
from gstudio.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.date_based import object_detail
from reversion.helpers import *
import pprint
from gstudio.models import *
from reversion.models import *
from gstudio.views.decorators import protect_nodetype
from gstudio.views.decorators import update_queryset
import ast

def history(request,ssid,version_no):
   # iden=request.GET["id"]
    nt1=Version.objects.get(id=ssid)
    nt=nt1.object.ref
    ver_dict=nt.version_info(ssid)
    ver_nbh=ver_dict['nbhood']
    ver_nbh_dict=ast.literal_eval(ver_nbh) 
    content=ver_dict['content']
    content=content[3:-4]
    ver_nbh_dict['content']=content
	
    variables = RequestContext(request,{'ver_nbh_dict':ver_nbh_dict ,'nt':nt,'ssid':ssid,'version_no':version_no})
    template="gstudio/display.html"
    return render_to_response(template,variables)

def get_version_counter(value):
    counter1=str(value)
    index=counter1.rfind(".")
    counter1=counter1[index+1:]
    version_no=int(counter1)
    return version_no
	

def get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,field):
    ver_new=""
    ver_old=""    
    diffs=""
    if ver_new_nbh_dict[field] or ver_old_nbh_dict[field]:
		for each in ver_new_nbh_dict[field]:
			ver_new+=str(each)+","
		ver_new=ver_new[0:-1]
		for each in ver_old_nbh_dict[field]:
			ver_old+=str(each)+","
		ver_old=ver_old[0:-1]
		diffs = dmp.diff_main(ver_new, ver_old)
    return diffs
	
def compare_history(request,ssid):
    ssid1=ssid
    
    version_counter1=request.GET["group1"]
    version_no1=get_version_counter(version_counter1)
    version_counter2=request.GET["group2"]
    version_no2=get_version_counter(version_counter2)
    counter2=float(version_counter2)
    ssid2=int(counter2)

    ver_obj=Version.objects.get(id=ssid1)
    ot=ver_obj.object.ref
    pp=pprint.PrettyPrinter(indent=4)
    
    ver_new_dict=ot.version_info(ssid1)
    content=str(ver_new_dict['content'])
    content=content[3:-4]
    ver_new_dict['content']=content

    ver_old_dict=ot.version_info(ssid2)
    content=str(ver_old_dict['content'])
    content=content[3:-4]
    ver_old_dict['content']=content
    
    ver_new_nbh=ver_new_dict['nbhood']
    ver_new_nbh_dict=ast.literal_eval(ver_new_nbh)
    
    ver_old_nbh=ver_old_dict['nbhood']
    ver_old_nbh_dict=ast.literal_eval(ver_old_nbh)

    compare_dict={}
    for each in ver_new_nbh_dict:
	 ver_new=""
         ver_old=""
	 if each=='altnames':
		if ver_new_nbh_dict['altnames'] or ver_old_nbh_dict['altnames']:
         		ver_new+=ver_new_nbh_dict['altnames']
			ver_old+=ver_old_nbh_dict['altnames']  
		  	diffs = dmp.diff_main(ver_new, ver_old)
			compare_dict['altnames']=dmp.diff_prettyHtml(diffs)
	
    		
         elif each=='title':
		if ver_new_nbh_dict['title'] or ver_old_nbh_dict['title']:
			ver_new+=ver_new_nbh_dict['title']
			ver_old+=ver_old_nbh_dict['title'] 
			diffs = dmp.diff_main(ver_new, ver_old)
    			compare_dict['title']=dmp.diff_prettyHtml(diffs)
	 elif each =='plural':
		if ver_new_nbh_dict['plural'] or ver_old_nbh_dict['plural']:
         		ver_new+=ver_new_nbh_dict['plural']
			ver_old+=ver_old_nbh_dict['plural'] 
			diffs = dmp.diff_main(ver_new, ver_old)
    			compare_dict['plural']=dmp.diff_prettyHtml(diffs)
	 elif each =='contains_members':
	        diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['contains_members']=dmp.diff_prettyHtml(diffs)
	 elif each =='leftroles':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['leftroles']=dmp.diff_prettyHtml(diffs)
	 elif each =='ats':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['ats']=dmp.diff_prettyHtml(diffs)
	 elif each =='rightroles':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['rightroles']=dmp.diff_prettyHtml(diffs)
	 elif each =='attributes':
		compare_rel_new={}
		compare_rel_old={}
		compare={}
		for rkey,rvalue in ver_new_nbh_dict[each].items():
			ver_new=""
        		for relvalue in rvalue:
				ver_new+=str(relvalue) + ","
                	ver_new=ver_new[0:-1]
	        	compare_rel_new[str(rkey)]=ver_new
    		for rkey,rvalue in ver_old_nbh_dict[each].items():
			ver_old=""
        		for rv in rvalue:
				ver_old+=str(rv) + ","
                	ver_old=ver_old[0:-1]
	        	compare_rel_old[str(rkey)]=ver_old
    		if len(compare_rel_new) >= len(compare_rel_old): 
        		for rkey,rvalue in compare_rel_new.items():
				if compare_rel_old.has_key(rkey):
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
			
				else:
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],"")		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
    		else: 
			for rkey,rvalue in compare_rel_old.items():
				if compare_rel_new.has_key(rkey):
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
				else:	
					diffs=dmp.diff_main("",compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
		compare_dict['attributes']=compare
    	  
	 elif each =='relations':

		ver_new=""
    		ver_old=""
   	 	compare_rel_new={}
    		compare_rel_old={}
    		compare={}
    		for rkey,rvalue in ver_new_nbh_dict[each].items():
			ver_new=""
        		for relk,relvalue in rvalue.items():
				ver_new+=str(relk) + ","
                		ver_new=ver_new[0:-1]
	        		compare_rel_new[str(rkey)]=ver_new
    		for rkey,rvalue in ver_old_nbh_dict[each].items():
			ver_old=""
        		for relk,relvalue in rvalue.items():
				ver_old+=str(relk) + ","
                		ver_old=ver_old[0:-1]
	        		compare_rel_old[str(rkey)]=ver_old
    		if len(compare_rel_new) >= len(compare_rel_old): 
        		for rkey,rvalue in compare_rel_new.items():
				if compare_rel_old.has_key(rkey):
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
			
				else:
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],"")		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
    		else: 
			for rkey,rvalue in compare_rel_old.items():
				if compare_rel_new.has_key(rkey):
					diffs=dmp.diff_main(compare_rel_new[str(rkey)],compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
				else:	
					diffs=dmp.diff_main("",compare_rel_old[str(rkey)])		
  					compare[str(rkey)]=dmp.diff_prettyHtml(diffs)
		compare_dict['relations']=compare
	 elif each =='priornodes':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['priornodes']=dmp.diff_prettyHtml(diffs)
	 elif each =='posteriornodes':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['posteriornodes']=dmp.diff_prettyHtml(diffs)
	 elif each =='type_of':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['type_of']=dmp.diff_prettyHtml(diffs)
	 elif each =='contains_subtypes':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['contains_subtypes']=dmp.diff_prettyHtml(diffs)
	 elif each =='member_of_metatypes':
		diffs=get_diff_from_dict(ver_new_nbh_dict,ver_old_nbh_dict,each)
    		compare_dict['member_of_metatypes']=dmp.diff_prettyHtml(diffs)
	
 
    ver_new=""
    ver_old=""
    ver_new+=ver_new_dict['content']
    ver_old+=ver_old_dict['content']
    diffs = dmp.diff_main(ver_new, ver_old)
    compare_dict['content']=dmp.diff_prettyHtml(diffs)
    ver_new_nbh_dict['content']=ver_new_dict['content']
    ver_old_nbh_dict['content']=ver_old_dict['content']

    

    variables=RequestContext(request,{'nt':ot,'ver_old_dict':ver_old_dict,'ver_new_dict':ver_new_dict,'compare_dict':compare_dict ,'ssid1':ssid1,'ssid2':ssid2,'version_no1':version_no1,'version_no2':version_no2,'ver_new_nbh_dict':ver_new_nbh_dict,'ver_old_nbh_dict':ver_old_nbh_dict})
    template="gstudio/version_diff.html"
    return render_to_response(template,variables)


def set_objecttype_field(obj,ver_merge):
     # setting the objecttypes fields	
     obj.slug = ver_merge['slug']
     obj.altnames=ver_merge['altnames']
     obj.rght = ver_merge['rght']
     obj.nodemodel = ver_merge['nodemodel']
     obj.lft = ver_merge['lft']
     obj.comment_enabled = ver_merge['comment_enabled']
     obj.title = ver_merge['title']
     obj.sites = ver_merge['sites']
     obj.content = ver_merge['content']
     obj.template = ver_merge['template']
     obj.tree_id = ver_merge['tree_id']
     obj.plural = ver_merge['plural']
     obj.status = ver_merge['status']
     obj.nid_ptr = NID.objects.get(id=ver_merge['nid_ptr'])
     
    # obj.nbh=ver_merge['nbh']
     obj.id = ver_merge['id']
     obj.pingback_enabled = ver_merge['pingback_enabled']
     			
     return obj
def set_attributetype_field(obj,ver_merge):
     # setting the objecttypes fields	
     obj.subjecttype = NID.objects.get(id=ver_merge['nid_ptr'])
     obj.applicable_nodetypes=ver_merge['applicable_nodetypes']
     obj.dataType = ver_merge['dataType']
     obj.verbose_name = ver_merge['verbose_name']
     obj.null = ver_merge['null']
     obj.blank = ver_merge['blank']
     obj.help_text = ver_merge['help_text']
    # obj.max_digits = ver_merge['max_digits']
    # obj.decimal_places = ver_merge['decimal_places']
     obj.auto_now = ver_merge['auto_now']
     obj.auto_now_add = ver_merge['auto_now_add']
     obj.upload_to = ver_merge['upload_to']
     obj.path = ver_merge['path']
     obj.verify_exists =  ver_merge['verify_exists']
    # obj.min_length= ver_merge['min_length']
     obj.required= ver_merge['required']
     obj.label = ver_merge['label']
     obj.unique = ver_merge['unique']
    # obj.validators= ver_merge['validators']
     obj.default= ver_merge['default']
     obj.editable= ver_merge['editable']
    # return HttpResponse(ver_merge)
     return obj
def set_relationtype_field(obj,ver_merge):

  
     # setting the  relationtype types fields	
     obj.inverse = ver_merge['inverse']
     obj.left_subjecttype=ver_merge['left_subjecttype']
     obj.left_applicable_nodetypes= ver_merge['left_applicable_nodetypes']
     obj.left_cardinality = ver_merge['left_cardinality']
     obj.right_subjecttype= ver_merge['right_subjecttype']
     obj.right_cadinality= ver_merge['right_cadinality']
     obj.right_cadinality= ver_merge['right_cadinality']
     obj.is_symmetrical= ver_merge['is_symmetrical']
     obj.is_reflexive= ver_merge['is_reflexive']
     obj.is_transitive= ver_merge['is_transitive']
     
     return obj

def set_processtype_field(obj,ver_merge):
     # setting the  processtype types fields	
     obj.changing_attributetype_set = ver_merge['']
     obj.changing_relationtype_set=ver_merge['']
     return obj

def set_systemtype_field(obj,ver_merge):
     # setting the systemtype types fields	
     obj.nodetype_set = ver_merge['nodetype_set']
     obj.relationtype_set=ver_merge['relationtype_set']
     obj.attributetype_set= ver_merge['attributetype_set']
     obj.metatype_set = ver_merge['metatype_set']
     obj.processtype_set= ver_merge['processtype_set']
     return obj

def get_merge_dict(ssid1,ssid2,direction):
     ver_merge={}
     ot=Version.objects.get(id=ssid1)
     obj=ot.object.ref
     ver_left_dict=obj.version_info(ssid1)
     ver_right_dict=obj.version_info(ssid2)

    
     
     if direction =='right':
        # swap left and right  
	 temp_dict={}
	 temp_dict=ver_left_dict
	 ver_left_dict=ver_right_dict
	 ver_right_dict=temp_dict
        # swap ssid1 and ssid2 for managing nbhood history
         temp=int(ssid1)
         ssid1=int(ssid2)
         ssid2=temp
     ver_left_nbh_dict=ast.literal_eval(ver_left_dict['nbhood'])
     ver_right_nbh_dict=ast.literal_eval(ver_right_dict['nbhood'])
     # By default value of content is removed 
     if ver_left_dict['content']=='<br />':
	 ver_left_dict['content']=''
     if ver_right_dict['content']=='<br />':
	 ver_right_dict['content']=''
     # Getting merged dictionary
     for each in ver_left_dict:
         if ver_left_dict[each] and ver_right_dict[each]:
         	ver_merge[each]=ver_right_dict[each]
         elif ver_left_dict[each]:
                  if not ver_right_dict[each]:
         		ver_merge[each]=ver_left_dict[each]
         elif ver_right_dict[each]:
         	 if not ver_left_dict[each]:
         		ver_merge[each]=ver_right_dict[each]
         else:
		 if not ver_left_dict[each]:
		 	if not ver_right_dict[each]:
                        	ver_merge[each]=ver_right_dict[each]
     ver_merge_nbh_dict={}    
     # processing nbhood for merged version
     for each in ver_left_nbh_dict:
         if isinstance(ver_left_nbh_dict[each],dict):
         	if ver_left_nbh_dict[each] and ver_right_nbh_dict[each]:
			ver_merge_nbh_dict[each]=dict(ver_left_nbh_dict[each].items()+ver_right_nbh_dict[each].items())
                elif ver_left_nbh_dict[each]:
			if not ver_right_nbh_dict[each]:
				ver_merge_nbh_dict[each]=ver_left_nbh_dict[each]
		elif ver_right_nbh_dict[each]:
			if not ver_left_nbh_dict[each]:
				ver_merge_nbh_dict[each]=ver_right_nbh_dict[each]
		else:
			if not ver_left_nbh_dict[each]: 
				if not ver_right_nbh_dict[each]:
					ver_merge_nbh_dict[each]=ver_right_nbh_dict[each]
         else:
		if ver_left_nbh_dict[each] and ver_right_nbh_dict[each]:
         		ver_merge_nbh_dict[each]=ver_right_nbh_dict[each]
         	elif ver_left_nbh_dict[each]:
                  	if not ver_right_nbh_dict[each]:
         			ver_merge_nbh_dict[each]=ver_left_nbh_dict[each]
         	elif ver_right_nbh_dict[each]:
         		if not ver_left_nbh_dict[each]:
         			ver_merge_nbh_dict[each]=ver_right_nbh_dict[each]
         	else:
			if not ver_left_nbh_dict[each]:
			  	if not ver_right_nbh_dict[each]:
                        		ver_merge_nbh_dict[each]=ver_right_nbh_dict[each]
		 
     # Removing auto generated fields
     del(ver_merge['start_publication'])
     del(ver_merge['end_publication'])
     del(ver_merge['creation_date'])
     del(ver_merge['last_update'])

     history_left_list=[]
     history_right_list=[]
     history_merged_list=[]

     history_left_list=ver_left_nbh_dict['history']
     history_left_list.append(ssid1)
     history_right_list=ver_right_nbh_dict['history']
     history_right_list.append(ssid2)
     history_merged_list.append(history_left_list)
     history_merged_list.append(history_right_list)
     ver_merge_nbh_dict['history']=history_merged_list

     obj.nbhood = unicode(ver_merge_nbh_dict)
     if isinstance(obj,Objecttype):
		obj=set_objecttype_field(obj,ver_merge)
     if isinstance(obj,Attributetype):
                obj=set_objecttype_field(obj,ver_merge)
                obj=set_attributetype_field(obj,ver_merge)
     if isinstance(obj,Relationtype):
                obj=set_objecttype_field(obj,ver_merge)
                obj=set_relationtype_field(obj,ver_merge)
     if isinstance(obj,Processtype):
                obj=set_objecttype_field(obj,ver_merge)
                obj=set_processtype_field(obj,ver_merge)
     if isinstance(obj,Systemtype):
                obj=set_objecttype_field(obj,ver_merge)
                obj=set_systemtype_field(obj,ver_merge)
     
     
     obj.save_revert_or_merge()	
     content=ver_merge['content']
     content=content[3:-4]
     ver_merge['content']= content 
     return ver_merge
     

def merge_version(request,ssid1,ssid2):
     direction=""
     ver_merge={}
     for each in request.GET:
	 direction=each
     ot=Version.objects.get(id=ssid1)
     obj=ot.object.ref
     ver_merge=get_merge_dict(ssid1,ssid2,direction)
     slist=[]
     slist=obj.get_ssid
     version_counter=len(slist)
     merged_ver_ssid=slist[version_counter-1]
     ver_merged_dict=obj.version_info(merged_ver_ssid)
     ver_merged_nbh_dict=ast.literal_eval(ver_merged_dict['nbhood'])
     ver_merged_nbh_dict['content']=ver_merge['content']
     variables = RequestContext(request,{'ver_nbh_dict':ver_merged_nbh_dict ,'nt':obj,'ssid':merged_ver_ssid,'version_no':version_counter})
     template="gstudio/display.html"
     return render_to_response(template,variables)

def revert(ssid):
     ver_revert={}
     ot=Version.objects.get(id=ssid)
     obj=ot.object.ref
     ver_revert=obj.version_info(ssid)
     
     # Removing auto generated fields
     del(ver_revert['start_publication'])
     del(ver_revert['end_publication'])
     del(ver_revert['creation_date'])
     del(ver_revert['last_update'])
     history=[]
     ver_revert_nbh_dict=ast.literal_eval(ver_revert['nbhood'])
     
     history=ver_revert_nbh_dict['history']
     history.append(ssid)
     ver_revert_nbh_dict['history']=history
     
     
  #   ver_revert_nbh_dict['history']=ver_revert_nbh_history.append(ssid)
     ver_revert['nbhood']=unicode(ver_revert_nbh_dict)
     obj.nbhood=ver_revert['nbhood']
     if isinstance(obj,Objecttype):
		obj=set_objecttype_field(obj,ver_revert)
     if isinstance(obj,Attributetype):
                obj=set_objecttype_field(obj,ver_revert)
                obj=set_attributetype_field(obj,ver_revert)
     if isinstance(obj,Relationtype):
                obj=set_objecttype_field(obj,ver_revert)
                obj=set_relationtype_field(obj,ver_revert)
     if isinstance(obj,Processtype):
                obj=set_objecttype_field(obj,ver_revert)
                obj=set_processtype_field(obj,ver_revert)
     if isinstance(obj,Systemtype):
                obj=set_objecttype_field(obj,ver_revert)
                obj=set_systemtype_field(obj,ver_revert)
     
     obj.save_revert_or_merge()	
     
     # formatting content field
     content=ver_revert['content']
     content=content[3:-4]
     ver_revert['content']= content 			
      
     return ver_revert
     
def revert_version(request):
     ver_revert={}
     for each in request.GET:
     	   ssid=each
     ssid=int(ssid)
     ot=Version.objects.get(id=ssid)
     obj=ot.object.ref
     
     ver_revert=revert(ssid)
     ver_revert['nbhood']
     slist=[]
     slist=obj.get_ssid
     version_counter=len(slist)
     revert_ver_ssid=slist[version_counter-1]
     ver_revert_dict=obj.version_info(revert_ver_ssid)
     ver_revert_nbh_dict=ast.literal_eval(ver_revert_dict['nbhood'])
     ver_revert_nbh_dict['content']=ver_revert['content']

     variables = RequestContext(request,{'ver_nbh_dict':ver_revert_nbh_dict ,'nt':obj,'ssid':revert_ver_ssid,'version_no':version_counter})
     template="gstudio/display.html"
     return render_to_response(template,variables)
    # return HttpResponse(ver_revert['nbhood'])
         

