from gstudio.lex import *

def lex(self):
	destination = open( "/home/user/gnowsys-studio/demo/aFile.pl", "a+"  )        
        f = destination.read()
        ##print "f---" ,f
        b = []
        c = []
        r = []
        source_r = []
        """
        strpos=f.find("one")
        ##print strpos
        """
        
        #Updates lexicon file with each Objecttype as noun singular and plural
        for each in Objecttype.objects.all():
             source=get_lex_OT(each)
             for e_i in source:
                        strpos=f.find(e_i)
                        #print strpos
                        if strpos == -1:
                             #print "Going to write --", e_i
                             destination.write(str(e_i) + '\n')
                        else:
                             pass
             
        #Updates lexicon file with Gbobject and author of each Nodetype and stores them as Proper noun
        for each in Nodetype.objects.all():
             for a in get_lex_author(each):
                  b.append(a)
        

        for each in Gbobject.objects.all():
            for a in get_lex_GB(each):
                  b.append(a)

        
        #Compares each of the entries of author & Gbobject, to make a unique list
        for each in b:
            if each not in c:
                    c.append(each)

        for e_i in c:
                 strpos=f.find(e_i)
                 #print strpos
                 if strpos == -1:
                          #print "Going to write --", e_i
                          destination.write(str(e_i) + '\n')
                 else:
                          pass
        
        #Updates lexicon file with each Relationtype as an intransitive adjective or transitive verb  
        for each in Relationtype.objects.all():
              for e_i in get_lex_RT(each):
                    r.append(e_i)
        ##print " r---(will contain all rts, may contain repetition of prepositions)"
         
        #Compares each of the entries to ensure preposition entries are unique        
        for each_r in r:
            if each_r not in source_r:
                 source_r.append(each_r) 
                 
        ###print "source_r, should not contain any rep"    
                           
        for e_ir in source_r:
                        strpos=f.find(e_ir)
                        #print strpos
                        if strpos == -1:
                             ##print "Going to write the above statement",e_i
                             destination.write(str(e_ir) + '\n')
                        else:
                             pass

        #Updates lexicon file with each Metatype as noun singular and plural
        for each in Metatype.objects.all():
              source_m=get_lex_MT(each)
              for e_im in source_m:
                        strpos=f.find(e_im)
                        #print strpos
                        if strpos == -1:
                             ##print "Going to write the above statement",e_i
                             destination.write(str(e_im) + '\n')
                        else:
                             pass
         
        #Updates lexicon file with each Attributetype as noun singular and plural
        for each in Attributetype.objects.all():
              source_a=get_lex_AT(each)
              for e_ia in source_a:
                        strpos=f.find(e_ia)
                        #print strpos
                        if strpos == -1:
                             ##print "Going to write the above statement",e_i
                             destination.write(str(e_ia) + '\n')
                        else:
                             pass
         
        
        destination.close()          
