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


import rdflib
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.namespace import Namespace
from rdflib.term import Literal
from rdflib.term import URIRef
from tempfile import mkdtemp
from gstudio.models import *
from objectapp.models import *
import settings
import os.path
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand
from pprint import pprint

import subprocess
from HTTP4Store import HTTP4Store


def rdf_all(notation='xml'):
    """
    Funtion takes  title of node, and rdf notation.
    """
    valid_formats = ["xml", "n3", "ntriples", "trix"]
    default_graph_uri = "http://gstudio.gnowledge.org/rdfstore"
  
    configString = "/var/tmp/rdfstore"

    # Get the IOMemory plugin.
    store = plugin.get('IOMemory', Store)('rdfstore')
   


    # Open previously created store, or create it if it doesn't exist yet
    graph = Graph(store="IOMemory",
               identifier = URIRef(default_graph_uri))
    path = mkdtemp()
    rt = graph.open(path, create=False)
    if rt == NO_STORE:
    
        graph.open(path, create=True)
    else:
        assert rt == VALID_STORE, "The underlying store is corrupt"


    # Now we'll add some triples to the graph & commit the changes
    
    graph.bind("gstudio", "http://gnowledge.org/")
    exclusion_fields = ["id", "rght", "node_ptr_id", "image", "lft", "_state", "_altnames_cache", "_tags_cache", "nid_ptr_id", "_mptt_cached_fields"]

    for node in NID.objects.all():
    	    node_dict=node.ref.__dict__
    	    node_type = node.reftype
            try:       
            
           	 if (node_type=='Gbobject'):
    	    		node=Gbobject.objects.get(title=node)
    		
    	    	 elif (node_type=='None'):
    			node=Gbobject.objects.get(title=node)
    		 
            	 elif (node_type=='Processes'):
    			node=Gbobject.objects.get(title=node)
    			 
            	 elif (node_type=='System'):
    			node=Gbobject.objects.get(title=node)
    			rdflib=link(node)
			url_addr=link1(node)
                	a=fstore_dump(url_addr) 
            	 elif (node_type=='Objecttype'):
    			node=Objecttype.objects.get(title=node)
    			
    	    	 elif (node_type=='Attributetype'):
    			node=Attributetype.objects.get(title=node)
    	        	 
    	    	 elif (node_type=='Complement'):
    			node=Complement.objects.get(title=node)
    			
            	 elif (node_type=='Union'):
    	   		node=Union.objects.get(title=node)
    			 
            	 elif (node_type=='Intersection'):
    			node=Intersection.objects.get(title=node)
    	
            	 elif (node_type=='Expression'):
    			node=Expression.objects.get(title=node)
    		
            	 elif (node_type=='Processtype'):
    			node=Processtype.objects.get(title=node)
    		 
            	 elif (node_type=='Systemtype'):
    	 		node=Systemtype.objects.get(title=node)
    			
            	 elif (node_type=='AttributeSpecification'):
    			node=AttributeSpecification.objects.get(title=node)
    			
            	 elif (node_type=='RelationSpecification'):
    			node=RelationSpecification.objects.get(title=node)
    		 rdflib=link(node) 	 
                 url_addr=link1(node)
                 a=fstore_dump(url_addr) 
            	 if(node_type=='Attribute'):
    			node=Attribute.objects.get(title=node)
    			rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
              	
            	 elif(node_type=='Relationtype' ):
    			node=Relationtype.objects.get(title=node)
    			rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
                
    	    	 elif(node_type=='Metatype'):
    			node=Metatype.objects.get(title=node)
    			rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
                 url_addr='http://sbox.gnowledge.org/gstudio/'
                 a=fstore_dump(url_addr) 
            except:
            	if(node_type=='Attribute'):
                	rdflib= Namespace('http://sbox.gnowledge.org/gstudio/')
    
            	if(node_type=='Relationtype' ):
                	rdflib= Namespace('http://sbox.gnowledge.org/gstudio/')
                    
            	if(node_type=='Metatype'):
                	rdflib= Namespace('http://sbox.gnowledge.org/gstudio/')
            	
           
    subject=str(node_dict['id'])
    for key in node_dict:
        if key not in exclusion_fields:
           predicate=str(key)
           pobject=str(node_dict[predicate])
           graph.add((rdflib[subject], rdflib[predicate], Literal(pobject)))                        
        
    rdf_code=graph.serialize(format=notation)
               #path to store the rdf in a file
    
    #x = os.path.join(os.path.dirname(__file__), 'rdffiles.rdf')
    
    graph.commit()
    graph.close()
    


#provides the url address of particular node.
def link(node):
	node_url=node.get_absolute_url()
    	site_addr= node.sites.all() 
    	a=site_addr[0]
    	host_name=a.name
   
    	link='http://'
    	#Concatenating the above variables will give the url address.

    	url_addr=link+host_name+node_url
    	rdflib=Namespace(url_addr) 
        return rdflib

def link1(node):
	node_url=node.get_absolute_url()
    	site_addr= node.sites.all() 
    	a=site_addr[0]
    	host_name=a.name
   
    	link='http://'
    	#Concatenating the above variables will give the url address.

    	url_addr=link+host_name+node_url
    	
        return url_addr
  
def fstore_dump(url_addr):
	
	store = HTTP4Store('http://localhost:8067')
	status = store.status()
	response = store.add_from_uri('http://example.com/nodetypes/2012/05/25/mouse/')
        return response

    	
	
    	
	
	
	
       



class Command(BaseCommand):
	def handle(self,*args,**options):		
                # verify the type of the node and pass the node to display the rdf accordingly.		
	
    		rdf_all(*args)






