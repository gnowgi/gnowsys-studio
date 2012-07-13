from gstudio.models import *
from objectapp.models import *
from django.template.defaultfilters import slugify
import inflect


def get_lex_author(self):
         """
         Generating lexicon file for authors-Proper name
         """
         author=self.authors.all()
         author_list=[]
         for each in author:              
              author_each=str(each).capitalize()
              aut="pn_sg('"+author_each+"', '"+author_each+"', neutr)."
              author_list.append(aut)
         return author_list 



def get_lex_GB(self):
    if self.ref.__class__.__name__ is 'Gbobject':
         a=[]            
         title=self.title
         title_slug=slugify(title)
         
         alt=self.altnames 
         alt_slug=slugify(alt)  
         singular="pn_sg('"+title_slug.title()+"', '"+title_slug.title()+"', neutr)."   
         a.append(singular)
         
         if alt:
           alts="pn_sg('"+str(alt_slug).title()+"', '"+str(alt_slug).title()+"', neutr)." 
           a.append(alts)
         return a  



def get_lex_RT(self):
     if self.ref.__class__.__name__ is 'Relationtype':
         p = inflect.engine()   
         a=[]
         title=self.title
         st=str(title)
         rst=slugify(st)
         if '-' in rst:
           i=rst.index('-')
           j=i+1           
           l=len(rst)         
           ss=rst[j:l]                
           lext = "adj_tr('"+rst+"', '"+rst+"', "+ss+")."           
           a.append(lext)
           lex_p = "prep("+ss+", "+ss+")."
           a.append(lex_p)
         else:
           if rst[-1] == 's':
             rst_sing = p.singular_noun(rst)             
             lex_tv = "tv_finsg("+rst+", "+rst_sing+")."             
             a.append(lex_tv)
           else:
             lexa = "adj_tr('"+rst+"', '"+rst+"', -)."             
             a.append(lexa)
         inverse=self.inverse
         if title!=inverse:           
           sti=str(inverse)
           rsti=slugify(sti)           
           if '-' in rsti:
             ii=rsti.index('-')
             ji=ii+1
             li=len(rsti)              
             ssi=rsti[ji:li]               
             lexi="adj_tr('"+rsti+"', '"+rsti+"', "+ssi+")."             
             a.append(lexi)
             lex_pi = "prep("+ssi+", "+ssi+")."             
             a.append(lex_pi)
           else:
            if rsti[-1] == 's':
              rsti_sing = p.singular_noun(rsti)              
              lex_tvi = "tv_finsg("+rsti+", "+rsti_sing+")."             
              a.append(lex_tvi)
            else:
              lexi_a = "adj_tr('"+rsti+"', '"+rsti+"', -)."                 
              a.append(lexi_a)    
         return a 


def get_lex_AT(self):
      if self.ref.__class__.__name__ is 'Attributetype':
         """Generates Lexicon entries for AT"""
         a=[]
         title = self.title
         st=str(title)         
         rst=slugify(st)                        
         singular="noun_sg("+rst+", "+rst+", neutr)."                    
         a.append(singular)
         alt=self.altnames 
         if alt:  
           st_a=str(alt)           
           rst_a=slugify(st_a)                         
           singular_a="noun_sg("+rst_a+", "+rst_a+", neutr)."                    
           a.append(singular_a)
         return a


def get_lex_MT(self):
    if self.ref.__class__.__name__ is 'Metatype':
         a=[]
         from django.template.defaultfilters import slugify   
         title=self.title
         title_slug=slugify(title)
         plural=self.plural
         plural_slug=slugify(plural) 
         alt=self.altnames 
         alt_slug=slugify(alt)  
         singular="noun_sg("+title_slug+", "+title_slug+", neutr)."                    
         a.append(singular)
         if plural:         
           pl="noun_pl("+str(plural_slug)+", "+str(title_slug)+", neutr)."  
           a.append(pl)
         if alt:
           alts="noun_sg("+str(alt_slug)+", "+str(alt_slug)+", neutr)." 
           a.append(alts)
         return a 



def get_lex_OT(self):
         """
         Generating lexicon file for Objecttype-Noun singular, plural
         """
         a=[]
         title=self.title
         slug_title=slugify(title)         
         plural=self.plural
         slug_plural=slugify(plural)    
         alt=self.altnames
         slug_alt=slugify(alt)
         singular="noun_sg("+slug_title+", "+slug_title+", neutr)."                    
         a.append(singular)
         if plural:
            pl="noun_pl("+str(slug_plural)+", "+str(slug_title)+", neutr)."  
            a.append(pl)
         if alt:
            alts="noun_sg("+str(slug_alt)+", "+str(slug_alt)+", neutr)." 
            a.append(alts)
         
         return a 
