from django.conf import settings
from django.utils.encoding import smart_str
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tagging.models import Tag

from gstudio import __version__
from gstudio.settings import PROTOCOL
from gstudio.models import Nodetype
from gstudio.models import Metatype

import urllib
import rdflib
from rdflib.events import Dispatcher, Event
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.namespace import Namespace
from rdflib.term import Literal
from rdflib.term import URIRef
from tempfile import mkdtemp
from gstudio.models import *
from objectapp.models import *
from reversion.models import Version
from optparse import make_option
from pprint import pprint
import httplib2
from urllib import urlencode

def get_nodetype():
	"""
    	returns the model the id belongs to.  
    	"""    
    	try:
        	""" 
        	ALGO:     get object id, go to version model, return for the given id.
        	"""
                name='student'
        	node = NID.objects.get(title=str(name))
        	# Retrieving only the relevant tupleset for the versioned objects
        	vrs = Version.objects.filter(type=0 , object_id=node.id) 
        	# Returned value is a list, so splice it .
        	vrs =  vrs[0]

    	except Error:
        	return "The item was not found."
        
    	return vrs.object._meta.module_name   
    

def rdf_description(notation='xml' ):
	"""
    	Funtion takes  title of node, and rdf notation.
    	"""
	name='student'
    	valid_formats = ["xml", "n3", "ntriples", "trix"]
    	default_graph_uri = "http://gstudio.gnowledge.org/rdfstore"
   	# default_graph_uri = "http://example.com/"
    	configString = "/var/tmp/rdfstore"

    	# Get the Sleepycat plugin.
    	store = plugin.get('IOMemory', Store)('rdfstore')
   


    	# Open previously created store, or create it if it doesn't exist yet
    	graph = Graph(store="IOMemory",
              	identifier = URIRef(default_graph_uri))
    	path = mkdtemp()
    	rt = graph.open(path, create=False)
    	if rt == NO_STORE:
    #There is no underlying Sleepycat infrastructure, create it
        	graph.open(path, create=True)
    	else:
        	assert rt == VALID_STORE, "The underlying store is corrupt"


    # Now we'll add some triples to the graph & commit the changes
   # rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    	graph.bind("gstudio", "http://gnowledge.org/")
    	exclusion_fields = ["id", "rght", "node_ptr_id", "image", "lft", "_state", "_altnames_cache", "_tags_cache", "nid_ptr_id", "_mptt_cached_fields"]
    	node_type=get_nodetype()
    	if (node_type=='gbobject'):
        	node=Gbobject.objects.get(title=name)
    	elif (node_type=='objecttype'):
       		node=Objecttype.objects.get(title=name)
  	elif (node_type=='metatype'):
        	node=Metatype.objects.get(title=name)
    	elif (node_type=='attributetype'):
       		node=Attributetype.objects.get(title=name)
   	elif (node_type=='relationtype'):
       		node=Relationtype.objects.get(title=name)
  	elif (node_type=='attribute'):
        	node=Attribute.objects.get(title=name)
    	elif (node_type=='complement'):
        	node=Complement.objects.get(title=name)
    	elif (node_type=='union'):
        	node=Union.objects.get(title=name)
    	elif (node_type=='intersection'):
        	node=Intersection.objects.get(title=name)
    	elif (node_type=='expression'):
        	node=Expression.objects.get(title=name)
    	elif (node_type=='processtype'):
        	node=Processtype.objects.get(title=name)
    	elif (node_type=='systemtype'):
        	node=Systemtype.objects.get(title=name)
   
   
    
   
    
    	node_url=node.get_absolute_url()
    	site_add= node.sites.all() 
    	a = site_add[0] 
    	host_name =a.name
    #host_name=name
    	link='http://'
    #Concatenating the above variables will give the url address.

    	url_add=link+host_name+node_url
    	rdflib = Namespace(url_add)
 # node=Objecttype.objects.get(title=name)

    	node_dict=node.__dict__

    	subject=str(node_dict['id'])
    	for key in node_dict:
        	if key not in exclusion_fields:
            		predicate=str(key)
            		pobject=str(node_dict[predicate])
            		graph.add((rdflib[subject], rdflib[predicate], Literal(pobject)))

     
    	rdf_code=graph.serialize(format=notation)

   

    


    #graph = rdflib.Graph("IOMemory")
    #graph.open("store", create=True)
    #graph.parse(rdf_code)

    # print out all the triples in the graph
   # for subject, predicate, object in graph:
      #  print subject, predicate, object
   # store.add(self,(subject, predicate, object),context)
     
     
    	graph.commit()
    	print rdf_code
    	graph.close()



class Command(NoArgsCommand):
    
    def handle(self, **options):
         

    	 get_nodetype()
	 rdf_description()
