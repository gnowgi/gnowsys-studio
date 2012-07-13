from objectapp.models import *
from gstudio.models import *
from django.template.defaultfilters import slugify
import inflect

def get_cnlgb_list(self):	
	z = []
	k = get_lex_sentence(self)
	if not k:
		pass
	else:
		z.extend(k)
        l = get_lex_sentence_optional(self)
	if not l:
		pass
	else:
		z.extend(l)
	m = get_CNL_dependency(self)
	if not m:
		pass
	else:
		z.extend(m)
	n = membership_sentence(self)
	if not n:
		pass
	else:
		z.extend(n)
        o = get_attr_sentence(self)
	if not o:
		pass
	else:
		z.extend(o)
        rel = get_rel(self)
        if not rel:
             pass
        else:
             z.extend(rel)
	return z

def advanced_cnlgb(self):
	zz=[]
	p = get_CNL_sentence_authors(self)
	if not p:
		pass
	else:
		zz.extend(p)
        """Generates CNL sentence for RT/R"""
        rt = get_RT_sentence(self)
        if not rt:
           pass
        else:
           zz.extend(rt)
	return zz


def get_lex_sentence(self): 
    if not self.ref.__class__.__name__ is 'Gbobject':
        pass
    else:      
      cns=self.get_nbh
      d=[]
      for k in cns:
          if k=='title':
            title = str(cns['title'])
       	    title_slug = slugify(title)
            if not cns[k]:
                     pass
            else:     
                     g=str(title_slug)+" is a proper-noun."
                     d.append(g.capitalize())
      return d


def get_lex_sentence_optional(self):   
    if not self.ref.__class__.__name__ is 'Gbobject':
        pass
    else: 
      cns=self.get_nbh
      title = str(cns['title'])
      title_slug = slugify(title)
      d=[]
      for k in cns:
        if k =='altnames':
            alt_name = str(cns['altnames'])
            alt_slug = slugify(alt_name)
            if not cns[k]:
                     pass
            else:             
                     i=str(cns[k])+" is an alternate name for "+str(title_slug)+"."
                     d.append(i.capitalize())

        elif k == 'plural':
            if not cns[k]:
                     pass
            else:  
                     pl = str(cns[k])
                     pl_slug = slugify(pl)           
                     m = str(pl_slug)+" is a plural of "+str(title_slug)+"."
                     d.append(m.capitalize())
        return d


      
def get_CNL_sentence_authors(self):
    if not self.ref.__class__.__name__ is 'Gbobject':
        pass
    else:   
      title = self.title
      title_slug = slugify(title)
      d=[]
      if self.authors.all():
                   auth = []
                   auth = self.authors.all() 
 	           len_auth=len(auth)                   
                   if len_auth == 1:
                     for each in auth:                     
                       aut=slugify(each)                                         
                       e=str(aut).title()+" is an author to "+str(title_slug).title()+"."
                       d.append(e)
                                         
                   else:
                       ##print "len not 1"                       
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

                          e = str(sen).title()+" are all chosen authors to "+str(title_slug).title()+"."                       
                       d.append(e)
                       
      return d


def get_CNL_dependency(self):    
    if not self.ref.__class__.__name__ is 'Gbobject':  
      pass
    else:    
      title = self.title
      title_slug = slugify(title)
      d=[]                          
      if self.prior_nodes.all():
                   p_n_a = [] 
                   p_n_a = self.prior_nodes.all()
                   len_pna=len(p_n_a)                   
                   if len_pna == 1:
                     for each in p_n_a:                     
                       pn=slugify(each)                                       
                       h=str(pn).title()+" is a prior_node for "+str(title_slug).title()+"."+str(title_slug).title()+" depends upon "+str(pn).title()+"."
                       d.append(h) 
                   else:                       
                       sen = dependency_plural(p_n_a)
                       h = str(sen)+". It is the prior_node and required for the meaning of "+str(title_slug).title()+"." 
                       d.append(h)
      
      if self.posterior_nodes.all():                
                   p_n_a = []
                   p_n_a = self.posterior_nodes.all() 
                   len_pna=len(p_n_a)                   
                   if len_pna == 1:
                     for each in p_n_a:                     
                       pn = slugify(each)                                         
                       p = str(pn).title()+" is a posterior_node for "+str(title_slug).title()+"."+str(title_slug).title()+" is required for the meaning of "+str(pn).title()+"."
                       d.append(p) 
                   else:                      
		       sen = dependency_plural(p_n_a)
                       p = str(sen)+". It is the posterior_node and depends on the meaning of "+str(title_slug).title()+"."
                       d.append(p)
      return d

#Generates dependency sentence for plural
def dependency_plural(p_n_a):  
   for each in p_n_a:   
      a = each	
      each_r = each.ref.__class__.__name__      
      
      a_slug = slugify(a)
      y=[]
      for a_slug in p_n_a: 
            if len(y) == 0:
                  #print "If Y is empty, for first item"
                  if each_r == 'Relationtype':
                        b_slug = str(a_slug).title()+" is an adjective" 
                  else:
                        b_slug = str(a_slug).title()+" is a proper-noun"
                  y.append(b_slug)
            else:
                  if each_r != 'Relationtype':
                        #print "Its not a relation_type, but a proper-noun"
                        aa_slug = str(a_slug).title()+" is a proper-noun"
                        y.append(aa_slug)
                  else:
                        #print "It is a relationtype"
                        ab_slug = str(a_slug).title()+" is an adjective"
                        y.append(ab_slug)                             
      for e_i in y:                             
                 if y.index(e_i) == 0:
                           sen = str(e_i)
                 else:                                                               
                           sen = str(sen)+" and "+str(e_i)      
   return sen         
   


def membership_sentence(self):
    """Returns CNL sentences for membership"""
    if not self.ref.__class__.__name__ is 'Gbobject':
        pass
    else:       
      cns=self.get_nbh
      title = str(cns['title'])
      title_slug = slugify(title)
      d=[]
      for k in cns:
        if self.ref.__class__.__name__ is 'Gbobject':
	  if k=='member_of':
                 if not cns[k]:
                     pass
                 else:
                   cmm = []
                   cmm = self.objecttypes.all()
 	           len_cmm=len(cmm)                   
                   if len_cmm == 1:
                     for each in cmm:                     
                       cm=slugify(each)                                         
                       j=str(title_slug)+" is a member of a "+str(cm)+"."
                       d.append(j.capitalize())
                                         
                   else:
                       #print "len not 1"
                       y=[]
                       for each in self.objecttypes.all():                             
                             a=each
                             a_slug=slugify(a)
                             y.append(a_slug)
                       for e_i in y:                             
                             if y.index(e_i) == 0:
                                sen = str(e_i)
                             else:
                                sen = str(sen)+" and a "+str(e_i)                   

                       j= str(title_slug)+" is a member of a "+sen+"."                 
                       d.append(j.capitalize())
                   
      return d


#Returns attributes for the given Gbobject
def get_attr_sentence(self):
  if not self.ref.__class__.__name__ is 'Gbobject':
        pass
  else: 
     at = Gbobject.get_attributes(self)
     if at:
       a = []
       title = self.title
       for k,v in at.iteritems():
             attr = k
             for each in v:
                  value = each
       sen = "The "+str(attr)+" of "+str(title)+" is "+str(value)+"."
       a.append(sen)
       return a


def get_list_relation(self, lr):
      """Returns the list of relations"""
      lst = []
      gbr = self.get_relations1
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
         #Flag variable that checks if plural-left,right
         plural_l = 0
         plural_r = 0
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
            if len(ll) == 1:
                   for e in ll: 
                       left_subtype = e
            else: 
                   """Since left-ST is plural, flag value assigned 1 """
                   plural_l = 1 
                   for e in ll:
                        if ll.index(e)==0:
                             sen = str(e)
                        else:
                             sen = str(sen)+" and "+str(e)
                   left_subtype = sen                    
         else:
                 """If llist is not a list"""
                 if lst.ref.__class__.__name__ is 'Gbobject':  
                     left_subtype = lst
                 else:
                     left_subtype = "a "+str(lst) 
         
         if isinstance(rlist,list):
            """If rlist is a list"""
            rl = []
            #print "Is a list"
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
            else:  
                   """Since right-ST is plural, flag value assigned 1 """
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
                       
         #Core sentence - title       
         
         rel = rel_CNL(self, left_subtype, right_subtype, plural_l)
         core_t.extend(rel)               
        
         rlex = rel_lex_sentence(self)
         adv.extend(rlex)        
 
         app_NT = get_app_NT(self)
         adv.extend(app_NT)
         
         st = get_RT_subjecttype(self, left_subtype, right_subtype)
         adv.extend(st)
    
         #Is symmetrical
         if is_symmetrical:
            symm = is_symmetrical_RT(self, left_subtype, right_subtype, plural_r)
            core_i.extend(symm)         
         else:
            asymm = is_asymmetrical_RT(self, left_subtype, right_subtype, plural_r)
            core_i.extend(asymm)            
            #Is reflexive 
         if not is_reflexive:
             pass
         else:
           if detail_level == 1 or plural_l == 1:
                 st = right_subtype
           else:
                 st = left_subtype
           is_refl = is_reflexive_sentence(self, st)        
           reflexive.extend(is_refl)                              
                    
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
               reflexive.insert(0, a)
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
        destination = open( "/home/user/gnowsys-studio/demo/aFile.pl", "r+"  )        
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
     rel.append(st)
   return rel  
         
         
def is_reflexive_sentence(self, st):
      """Generates reflexive sentence"""
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
          #if (type_lst == 'Gbobject' and type_rst == 'Gbobject'):
          if istv_title(self):
             g = str(right_subtype).title()+" "+str(title)+" "+str(left_subtype).title()+"."
          else:
            if plural_r == 0:
               g = str(right_subtype).title()+" is "+str(title)+" "+str(left_subtype).title()+"."  
            else:
               g = str(right_subtype).title()+" are "+str(title)+" "+str(left_subtype).title()+"."  
          symm.append(g)
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
      asymm.append(g)          
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
       #Generates CNL Sentences in RT in detail
       if self.ref.__class__.__name__ is 'Relationtype':
          sentence = get_CNL_sentence_RT(self, self.left_subjecttype, self.right_subjecttype, 4)
          return sentence

       #Generates CNL sentences in Relation in detail
       elif self.ref.__class__.__name__ is 'Relation':
          sentence = get_CNL_sentence_RT(self.relationtype, self.left_subject, self.right_subject, 4)
          return sentence




#Get relations for the Gbobject:Singular, plural
def get_rel(self):
    sen = []
    sentence = []
    lr = Relation.objects.filter(left_subject = self.id)
    rr = Relation.objects.filter(right_subject = self.id)
    
       
    if lr:
      """List which stores each right subject"""
      lst = get_list_relation(self, 0)
      
      for k,v in lst.iteritems():      
          rel = Relationtype.objects.filter(title = k)
          val = v   
          for rt in rel:  
             sen = get_CNL_sentence_RT(rt, self, val, 0)
             sentence.extend(sen)
          
    if rr:
       """List which stores each left subject"""
       lst = get_list_relation(self, 1)
      
       for k,v in lst.iteritems():      
          rel = Relationtype.objects.filter(inverse = k)
          val = v   
          for rt in rel:  
             sen = get_CNL_sentence_RT(rt, val, self,1)
             sentence.extend(sen)     
    return sentence



def get_RT_subjecttype(self, left_subtype, right_subtype):
   """Returns CNL sentence of left & right subject type of RT"""
   if self.ref.__class__.__name__ is 'Relationtype':
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



	

      

