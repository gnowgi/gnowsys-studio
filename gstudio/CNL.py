from gstudio.models import *
from django.template.defaultfilters import slugify
import inflect
import os

def get_CNL_list(self):
	x = []
	a = get_lex_sentence(self)
	if not a:
		pass
	else:
		x.extend(a)
	b = lex_sentence_optional(self)
	if not b:
		pass
	else:
		x.extend(b)
	c = contains_subtypes_sentence(self)
        if not c:
		pass
	else:
		x.extend(c)
	d = typeof_sentence(self)
	if not d:
		pass
	else:
		x.extend(d)
	e = get_CNL_dependency(self)
	if not e:
		pass
	else:
		x.extend(e)
	f = get_rel(self)
	if not f:
		pass
	else:
		x.extend(f)
	g = get_attr_sentence(self)
	if not g:		
		pass
	else:
		x.extend(g)
	return x


def advanced_CNL(self):
	y = []
	h = get_leftST_sentence(self)	
	if not h:                
		pass
	else:
		y.extend(h)
	i = get_rightST_sentence(self)
	if not i:
		pass
	else:
		y.extend(i)
        j = get_ST_sentence(self)
	if not j:
		pass
	else:
		y.extend(j)
	k = get_CNL_sentence_authors(self)
	if not k:
		pass
	else:
		y.extend(k)
        """To generate CNL data about RT/R"""	
        a = get_RT_sentence(self)
        if not a:
               pass
        else:
               y.extend(a)
	return y

#Returns lex sentence - Title 
def get_lex_sentence(self):  
    if self.ref.__class__.__name__ is 'Relationtype' or self.ref.__class__.__name__ is 'Attribute':
       pass
    else:      
       # If AT or RT       
       at = []
       g = ""
       if self.title:
           title = slugify(self.title)
           title_slug = slugify(title)
           if self.ref.__class__.__name__ is 'Attributetype' or self.ref.__class__.__name__ is 'Objecttype':
                g = "A "+str(title_slug).lower()+" is a common-noun."                       
           elif self.ref.__class__.__name__ is 'Metatype':                 
                g = "A "+str(title_slug).lower()+" is a metatype."    
              
           at.append(g)        
       return at

#Returns CNL sentences - Plural & Alternate names
def lex_sentence_optional(self): 
      
      # If AT, MT or OT
      a = []
      if self.ref.__class__.__name__ is 'Attribute' or self.ref.__class__.__name__ is 'Relationtype':
	pass
      elif self.ref.__class__.__name__ is 'Attributetype' or self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Metatype':
         title_slug = slugify(self.title)
         if self.altnames:
           alt = self.altnames
           alt_slug = slugify(alt)
           e = "A "+str(alt_slug)+" is an alternate name for it."
           a.append(e.capitalize())
      
      # If MT or OT
      if self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Metatype':
         if self.plural:
           plu_slug = slugify(self.plural)
           m="Some "+str(plu_slug)+" are a plural of a "+str(title_slug)+"."
           a.append(m.capitalize())
      return a    

#Generates CNL sentence for RT for which OT or MT is the left-subjecttype
def get_leftST_sentence(self):    
    if self.ref.__class__.__name__ is 'Attributetype' or self.ref.__class__.__name__ is 'Relationtype' or self.ref.__class__.__name__ is 'Attribute':
         pass     
    else:
      #If OT or MT
      cns=self.ref.get_nbh
      d = []
      for k in cns:
         title = str(cns['title'])
         title_slug = slugify(title)
         if self.ref.__class__.__name__ is 'Objecttype' or 'Metatype':
           if k == 'left_subjecttype_of':
               if not cns[k]:
                     pass
               else:                 
                   l_s_a = []
                   l_s_a = self.left_subjecttype_of.all() 
                   len_lsa=len(l_s_a)                   
                   if len_lsa == 1:
                     #If singular:
                     for each in l_s_a:                     
                       al=slugify(each) 
                       #A person is a n:left_subjecttype of a n:relation_type a:teaches and a:student-of and a:sibling-of and a:friend-of.    
                       if self.ref.__class__.__name__ is 'Objecttype':                                    
                          c = "A "+str(title_slug)+" is a left_subjecttype of a relation_type "+str(al)+"."  
                       elif self.ref.__class__.__name__ is 'Metatype':
                          c = "A "+str(title_slug)+" is a left_subjecttype of a relation_type "+str(al)+"." 
                       d.append(c.capitalize())
                                         
                   else:                     
                       #If plural:
                       y=[]
                       for each in self.left_subjecttype_of.all():                             
                             a=each
                             a_slug=slugify(a)
                             y.append(a_slug)
                       for e_i in y:                            
                             if y.index(e_i) == 0:
                                sen = str(e_i)
                             else:
                                sen = str(sen)+" and "+str(e_i)                  
                       if self.ref.__class__.__name__ is 'Objecttype':
                            c = "A "+str(title_slug)+" is a left_subjecttype of a relation_type "+sen+"."                       
                       elif self.ref.__class__.__name__ is 'Metatype':
                            c = "A "+str(title_slug)+" is a left_subjecttype of a relation_type "+sen+"."     
                       
                       d.append(c.capitalize())
      return d   

#Generates CNL sentence for RT for which OT or MT is the right-subjecttype
def get_rightST_sentence(self):    
    if self.ref.__class__.__name__ is 'Attributetype' or self.ref.__class__.__name__ is 'Relationtype' or self.ref.__class__.__name__ is 'Attribute':
         pass     
    else:
      #If OT or MT
      cns=self.ref.get_nbh
      d = []
      for k in cns:
          title = str(cns['title'])
          title_slug = slugify(title)
          if self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Metatype':
            if k == 'right_subjecttype_of':
               if not cns[k]:
                     pass
               else:                 
                   r_s_a = []
                   r_s_a = self.right_subjecttype_of.all() 
                   len_rsa=len(r_s_a)                   
                   if len_rsa == 1:
                     #If singular:
                     for each in r_s_a:                     
                       al=slugify(each)     
                       if self.ref.__class__.__name__ is 'Objecttype':                                    
                          c = "A "+str(title_slug)+" is a right_subjecttype of a relation_type "+str(al)+"."  
                       elif self.ref.__class__.__name__ is 'Metatype':
                          c = "A "+str(title_slug)+" is a right_subjecttype of a relation_type "+str(al)+"." 
                       d.append(c.capitalize())
                                         
                   else:
                     #If plural:
                       y=[]
                       for each in self.right_subjecttype_of.all():                             
                             a=each
                             a_slug=slugify(a)
                             y.append(a_slug)
                       for e_i in y:                            
                             if y.index(e_i) == 0:
                                sen = str(e_i)
                             else:
                                sen = str(sen)+" and "+str(e_i)                  
                       if self.ref.__class__.__name__ is 'Objecttype':
                            c = "A "+str(title_slug)+" is a right_subjecttype of a relation_type "+sen+"."                       
                       elif self.ref.__class__.__name__ is 'Metatype':
                            c = "A "+str(title_slug)+" is a right_subjecttype of a relation_type "+sen+"."     
                       
                       d.append(c.capitalize())
      return d   

#Generates Subject-type sentence for AT
def get_ST_sentence(self):
     if self.ref.__class__.__name__ is 'Attribute':
	pass
     elif self.ref.__class__.__name__ is 'Attributetype':
        a = []
        if self.subjecttype:     
           subjecttype = self.subjecttype
           st_type = subjecttype.ref.__class__.__name__
           if st_type == 'Gbobject':
              c = str(subjecttype)+" is a subject_type_name for it."
           else:
              c = "A "+str(subjecttype)+" is a subject_type_name for it."
           a.append(c.capitalize())
        return a 


#Generates contains-subtypes for MT or OT
def contains_subtypes_sentence(self):          
    if self.ref.__class__.__name__ is 'Metatype' or self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Attribute':
	pass
    elif self.ref.__class__.__name__ is 'Metatype' or self.ref.__class__.__name__ is 'Objecttype':
        #print "is a mt or OT"
	#print "it just entered the loop"
        cns=self.ref.get_nbh
        d = []
        for k in cns:
          title = str(cns['title'])
          title_slug = slugify(title)
          if k=='contains_subtypes':              
                 if not cns[k]:
                    pass
                 else:
                    if self.ref.__class__.__name__ is 'Metatype':
                       nof=self.children.get_query_set()                    
                    elif self.ref.__class__.__name__ is 'Objecttype':       
                       nof=Nodetype.objects.filter(parent=self.id)         
 	            len_nof=len(nof)
                    #print "nof----" ,nof   
                    #print len_nof, "len - nof"                                 
                    if len_nof == 1:
                      for each in nof:                     
                        nf=slugify(each) 
                        l = "A "+str(nf)+" is a subtype of a "+str(title_slug)+"."
                        d.append(l.capitalize())                                        
                    else:
                       #print "len not 1"
                       y=[]
                       for each in nof:                             
                             a=each
                             a_slug=slugify(a)
                             y.append(a_slug)
                       for e_i in y:                             
                             if y.index(e_i) == 0:
                                sen = str(e_i)
                             else:
                                sen = str(sen)+" and a "+str(e_i)                 

                       l = "A "+sen+" are some subtypes of "+str(title_slug)+"."                      
                       d.append(l.capitalize())
        return d  

#Generates Type-Of sentence for OT or MT
#get_nbh type_of --- Metatype
def typeof_sentence(self):       
   d = []
   if self.ref.__class__.__name__ is 'Relationtype' or self.ref.__class__.__name__ is 'Attributetype' or self.ref.__class__.__name__ is 'Attribute':
     pass
   elif self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Metatype':
     #print "mt or ot"
     cns = self.ref.get_nbh
     for k in cns:
       title = str(cns['title'])
       title_slug = slugify(title)
       if k=='type_of':
                 if not cns[k]:
                     pass
                 else:                   
                   if self.ref.__class__.__name__ is 'Objecttype':                     
                     n = self.parent
		     n_slug=slugify(n)
                   elif self.ref.__class__.__name__ is 'Metatype':                      
                     n = str(cns[k])                    
                     n_slug=slugify(n)
                   an = "A "+str(title_slug)+" is a type of a "+str(n_slug)+"."                   
                   d.append(an.capitalize())
                 return d

#Generates CNL Sentence - Prior & Posterior Nodes
def get_CNL_dependency(self): 
    if self.ref.__class__.__name__ is 'Attribute':
	pass   
    elif self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Attributetype' :      
      title = self.title
      title_slug = slugify(title)
      d=[]                          
      if self.prior_nodes.all():
                   p_n_a = [] 
                   p_n_a = self.prior_nodes.all()
                   #print len(p_n_a)
                   len_pna=len(p_n_a)                   
                   if len_pna == 1:
                     for each in p_n_a:                     
                       pn=slugify(each)                                       
                       h="A "+str(title_slug)+" depends on a "+str(pn)+"."
                       d.append(h.capitalize()) 
                   else:                       
                       sen = dependency_plural(p_n_a)
                       h = "A "+str(sen)+". It is required for the meaning of a "+str(title_slug)+"."
                       d.append(h)
      
      if self.posterior_nodes.all():                
                   p_n_a = []
                   p_n_a = self.posterior_nodes.all() 
                   #print "length of posterior nodes-----" ,len(p_n_a)
                   len_pna=len(p_n_a)                   
                   if len_pna == 1:
                     for each in p_n_a:                     
                       pn = slugify(each)                                         
                       p = "A "+str(title_slug)+" is required for the meaning of a "+str(pn)+"."
                       d.append(p.capitalize()) 
                   else:                      
		       sen = dependency_plural(p_n_a)
                       p = "A "+str(sen)+". It depends on "+str(title_slug)+"."
                       d.append(p)
      return d

#Generates dependency sentence for plural
def dependency_plural(p_n_a):                                              
                      y=[]
                      #print "len not 1"
                      for each in p_n_a:
                         each_r = each.ref.__class__.__name__
                         apn = each
                         apn_slug = slugify(apn)
                         if len(y) == 0:
                                "If Y is empty, for first item"
                                if each_r == 'Relationtype':
                                    b_slug = str(apn_slug)+" is an adjective" 
                                else:
                                    b_slug = str(apn_slug)+" is a common-noun"
                                y.append(b_slug)
                         else:
                                if each_r != 'Relationtype':
                                   #print "Its not a relation_type, but a noun, so appending an 'a' "
                                   aa_slug = "a "+str(apn_slug)+" is a common-noun"
                                   y.append(aa_slug)
                                else:
                                   #print "It is a relationtype"
                                   ab_slug = str(apn_slug)+" is an adjective"
                                   y.append(ab_slug)
                      for e_i in y:
                             if y.index(e_i) == 0:
                                sen = str(e_i).lower()
                             else:                             
                                sen = str(sen)+" and "+str(e_i).lower()  
                      return sen 



#Generates CNL sentence for authors, in OT and AT
def get_CNL_sentence_authors(self):      
      title = self.title
      title_slug = slugify(title)
      d=[]
      if self.ref.__class__.__name__ is 'Attribute':
	pass
      elif self.ref.__class__.__name__ is 'Objecttype' or self.ref.__class__.__name__ is 'Attributetype':
        if self.authors.all():
                   auth = []
                   auth = self.authors.all() 
 	           len_auth=len(auth)                   
                   if len_auth == 1:
                     for each in auth:                     
                       aut=slugify(each)                                         
                       e=str(aut).title()+" is an author to a "+str(title_slug)+"."
                       d.append(e.capitalize())                                         
                   else:
                       #print "len not 1"                       
                       y=[]
                       for each in self.authors.all():                             
                          a=each
                          a_slug=slugify(a)
                          y.append(a_slug)
                          for e_i in y:                             
                             if y.index(e_i) == 0:
                                sen = str(e_i)
                             else:
                                sen = str(sen)+" and "+str(e_i)

                          e = str(sen).title()+" are all chosen authors to a "+str(title_slug)+"."                       
                       d.append(e.capitalize())                       
      return d


    
         
	 

#Checks if RT-title is a transitive verb finite singular or an iterative adjective
def istv_title(self):        
        p = inflect.engine()
        from django.template.defaultfilters import slugify
        destination = open( "/home/user/gnowsys-studio/demo/aFile.pl", "r+"  )        
        f = destination.read()
        a_t = self.title
        a = slugify(a_t)               
        if '-' not in a:
            if a[-1] == 's':
                  a_s = p.singular_noun(a)
                  a_lex = "tv_finsg("+a+", "+str(a_s)+")."
                  strpos = f.find(a_lex)
                  if strpos != -1: 
                       return True
                  else:
                       return False

#Checks if RT-inverse is a transitive verb finite singular or an iterative adjective
def istv_inverse(self):
        p = inflect.engine()        
        destination = open( os.path.join(os.getcwd(),'aFile.pl'), "r+"  )        
        f = destination.read()
        a_t = self.inverse
        a = slugify(a_t)               
        if '-' not in a:
            if a[-1] == 's':
                  a_s = p.singular_noun(a)
                  a_lex = "tv_finsg("+a+", "+str(a_s)+")."
                  strpos = f.find(a_lex)
                  if strpos != -1: 
                       return True
                  else:
                       return False


#Returns attributes for the given OT
def get_attr_sentence(self):
   if self.ref.__class__.__name__ is 'Objecttype':
     from django.template.defaultfilters import slugify
     ot = self.get_attributes
     if not ot:
          pass
     else:
       a = []
       title = self.title
       title_slug = slugify(title)
       for k,v in ot.iteritems():
             attr = k
             for each in v:
                  value = each
       attr_slug = slugify(attr)
       sen = "The "+str(attr_slug)+" of a "+str(title_slug)+" is "+str(value)+"."
       a.append(sen)
       return a
   else:
     pass


def get_list_relation(self, lr):
      """Returns the list of relations"""     
      gbr = self.get_rendered_relations
      if not gbr:
            pass
      else:
          for k,v in gbr.iteritems():
               if k == 'lrelations':
                    val_l = v
               if k == 'rrelations':
                    val_r = v
          
          if lr == 0:
                return val_l
          elif lr == 1:
                return val_r

#Generating CNL for RT and Relations:
#(**Execute get_lex property to update new RT's in lexicon before executing CNL sentences.)
def get_CNL_sentence_RT(self, lst, rst, detail_level):      
      if self.ref.__class__.__name__ is 'Relationtype':
         core = [] #core data list
         core_t = []
         core_i = []
         reflexive = []
	 adv = [] # advanced data list             
         title=self.title
         title_slug=slugify(title)
         inverse=self.inverse
         inverse_slug=slugify(inverse)
         is_symmetrical=self.is_symmetrical
         is_reflexive=self.is_reflexive
         llist = []
         rlist = []
         llist = lst
         rlist = rst
         #print "lst",llist
         #print "rst",rlist
         #Flag variable that checks if plural or not
         plural_l = 0
         plural_r = 0
         #print "ll--",llist 
         #print "rr---",rlist
         if isinstance(llist,list):
            """If llist is a list"""
            ll = []
            for each in llist:                
                if each.ref.__class__.__name__ is not 'Gbobject':
                    """Common-noun"""
                    lst = "a "+str(each).lower()
                else:
                    """Proper-noun"""
                    lst = str(each).title()
                ll.append(lst)
		#print "ll",ll
            if len(ll) == 1:
                   for e in ll: 
                       left_subtype = e
		       #print "e in ll",left_subtype
            else: 
                   plural_l = 1 
                   for e in ll:
                        if ll.index(e)==0:
                             sen = str(e)
                        else:
                             sen = str(sen)+" and "+str(e)
                   left_subtype = sen                    
         else:
                 """If llist is not a list"""
                 lst=NID.objects.get(title=lst)
                 if lst.ref.__class__.__name__ is 'Gbobject':  
                     left_subtype = lst
                 else:
                     left_subtype = "a "+str(lst) 
         #print "left_subtype---",left_subtype  
         
         if isinstance(rlist,list):
            """If rlist is a list"""
            rl = []
            for each in rlist:                
                if each.ref.__class__.__name__ is not 'Gbobject':
                    """Common-noun"""
                    rst = "a "+str(each)
                else:
                    rst = each
                rl.append(rst)
            if len(rl) == 1:
                   for e in rl: 
                       right_subtype = e
                       #print "rst in e---",right_subtype
            else:  
                   plural_r = 1
                   for e in rl:
                        if rl.index(e)==0:
                             sen = str(e)
                        else:
                             sen = str(sen)+" and "+str(e)
                   right_subtype = sen                    
         else:
                 """If Rlist is not a list"""
                 if rst.ref.__class__.__name__ is 'Gbobject':
                    right_subtype = rst 
                 else:
                    right_subtype = "a "+str(rst)     
         #print "right_subtype---",right_subtype   
         
         
         #Core sentence - title       
         
         rel = rel_CNL(self, left_subtype, right_subtype, plural_l)
         #print rel, "the sentence"
         #print left_subtype
         #print right_subtype
         core_t.extend(rel)               
         
        
         rlex = rel_lex_sentence(self)
         adv.extend(rlex)
         #print "rlex---",rlex
 
         app_NT = get_app_NT(self)
         adv.extend(app_NT)
         #print "app_NT",app_NT
         
         st = get_RT_subjecttype(self, left_subtype, right_subtype)
         adv.extend(st)
         #print "st---",st
         
        
    
         #Is symmetrical
         if is_symmetrical:
            symm = is_symmetrical_RT(self, left_subtype, right_subtype, plural_r)
            core_i.extend(symm)               
            #print "symm---",symm
         
         else:
            asymm = is_asymmetrical_RT(self, left_subtype, right_subtype, plural_r)
            core_i.extend(asymm)
            #print "asymm--",asymm
         #Is reflexive 
         if is_reflexive:
           if detail_level == 1 or plural_l == 1:
                 st = right_subtype
           else:
                 st = left_subtype
           is_refl = is_reflexive_sentence(self, st)          
           core.extend(is_refl)
           reflexive.extend(is_refl)                              
           #print "is_refl" ,is_refl            
                    
         if detail_level==0:
               #Title,Reflexive
               for e in core_t:
                   a = e
               reflexive.insert(0, a)
               return reflexive
	 elif detail_level==1:
               #Inverse,reflexive
	       for e in core_i:
                    a = e
               reflexive.insert(0,a)
               return reflexive
         elif detail_level==2:
               #Title, Inverse & Reflexive
               core.extend(core_t)
               core.extend(core_i)
               core.extend(reflexive)
               return core
         elif detail_level==3:
               #Return advanced grammatical information
	       return adv
	 elif detail_level==4:
                #Return all info - Core & Advanced Info
	 	newlist = []
	 	newlist.extend(core)
	 	newlist.extend(adv)
	  	return newlist

def rel_CNL(self, left_subtype, right_subtype, plural_l):
   """To generate sentence for relation"""
   title = self.title
   title_slug = slugify(title)
   if self.ref.__class__.__name__ is 'Relationtype':
     rel = []
     if istv_title(self):
           st = str(left_subtype)+" "+str(title).lower()+" "+str(right_subtype)+"."
     else: 
        if plural_l == 0:
              st = str(left_subtype)+" is "+str(title).lower()+" "+str(right_subtype)+"."
        elif plural_l == 1:
              st = str(left_subtype)+" are "+str(title).lower()+" "+str(right_subtype)+"."
     rel.append(st.capitalize())
   return rel  
         
         
def is_reflexive_sentence(self, st):
      refl = []
      title = self.title
      title_slug = slugify(title)
      if istv_title(self): 
         j= "It is a reflexive sentence. "+str(st).title()+" "+str(title)+" "+str(st)+"."
      else:
         j= "It is a reflexive sentence. "+str(st).title()+" is "+str(title)+" "+str(st)+"."
      refl.append(j)  
      return refl

def is_symmetrical_RT(self, left_subtype, right_subtype, plural_r):
          """Generates CNL Sentence for Relation/RT if symmetrical"""
          symm = []
          title = self.title
          title_slug = slugify(title)
          if istv_title(self):
             g = str(right_subtype).title()+" "+str(title)+" "+str(left_subtype).title()+"."
          else:
            if plural_r == 0:
               g = str(right_subtype).title()+" is "+str(title)+" "+str(left_subtype).title()+"."  
            else:
               g = str(right_subtype).title()+" are "+str(title)+" "+str(left_subtype).title()+"."  
          symm.append(g.capitalize())
          return symm

def is_asymmetrical_RT(self, left_subtype, right_subtype, plural_r):
      """Generates CNL Sentence for Relation/RT if symmetrical"""
      asymm = []
      inverse = self.inverse
      inverse_slug = slugify(inverse)
      if istv_inverse(self):
             g = str(right_subtype).title()+" "+str(inverse)+" "+str(left_subtype).title()+"."
      else:
         if plural_r == 0:
             g = str(right_subtype).title()+" is "+str(inverse)+" "+str(left_subtype).title()+"."
         elif plural_r == 1:
             g = str(right_subtype).title()+" is "+str(inverse)+" "+str(left_subtype).title()+"."
      asymm.append(g.capitalize())          
      return asymm


def rel_lex_sentence(self):
   """Generates RT's title & inverse sentence"""
   if self.ref.__class__.__name__ is 'Relationtype':
      rlex = []
      title=self.title
      title_slug=slugify(title)
      inverse=self.inverse
      inverse_slug=slugify(inverse)
      h="A relation_type's title is "+str(title_slug)+"."
      rlex.append(h.capitalize())
      
      if (title==inverse):
             b="Its title and its inverse are equal."
      else:
             b="Its inverse is "+str(inverse_slug)+"."
      rlex.append(b.capitalize())
      return rlex


def get_app_NT(self):
     """Generates CNL Sentences for left & right applicable NT for RT"""
     if self.ref.__class__.__name__ is 'Relationtype':
         a = []
         l_app = self.left_applicable_nodetypes         
         r_app=self.right_applicable_nodetypes   
         e = "Its left_applicable_nodetype is "+str(l_app).upper()+"."
         a.append(e)
         
         f = "Its right_applicable_nodetype is "+str(r_app).upper()+"."
         a.append(f) 
         return a     
         
         
        
def get_RT_sentence(self):
       #Generates CNL Sentences in RT
       if self.ref.__class__.__name__ is 'Relationtype':
          sentence = get_CNL_sentence_RT(self, self.left_subjecttype, self.right_subjecttype, 4)
          return sentence  

       #Generates CNL sentences in Relation
       elif self.ref.__class__.__name__ is 'Relation':
          sentence = get_CNL_sentence_RT(self.relationtype, self.left_subject, self.right_subject, 4)
          return sentence
       else:
         pass




def get_rel(self):
  if not self.ref.__class__.__name__ is 'Objecttype':
    pass
  else:
    sen = []
    sentence = []
    lr = Relation.objects.filter(left_subject = self.id)
    rr = Relation.objects.filter(right_subject = self.id)
    
       
    if lr:
      """List which stores each right subject"""
      lst = get_list_relation(self, 0)
      #print "LR",lst
      for k,v in lst.iteritems():      
          rel = Relationtype.objects.filter(title = k)
          val = v   
          for rt in rel:  
             sen = get_CNL_sentence_RT(rt, self, val, 0)
             #print "sen----lr",sen
             sentence.extend(sen)
      #print "sentence lr",sentence
          
    if rr:
       """List which stores each left subject"""
       lst = get_list_relation(self, 1)
       #print "RR",lst
       for k,v in lst.iteritems():      
          rel = Relationtype.objects.filter(inverse = k)
          val = v 
          #print "rel ",rel
          #print "v ",v  
          for rt in rel:  
             sen = get_CNL_sentence_RT(rt, val, self, 1)
             #print sen,"sen"
             sentence.extend(sen)     
    return sentence



def get_RT_subjecttype(self,lst,rst):
   """Returns CNL sentence of left & right subject type of RT"""
   if self.ref.__class__.__name__ is 'Relationtype':
       left_subtype = lst
       right_subtype = rst
       st = []
       ce = "Its left_subjecttype is "+str(left_subtype)+"."
       c = ce.capitalize()
       st.append(c)
        
       de = "Its right_subjecttype is "+str(right_subtype)+"."
       d = de.capitalize()
       st.append(d)
       return st
   else:
       pass    



	

      



