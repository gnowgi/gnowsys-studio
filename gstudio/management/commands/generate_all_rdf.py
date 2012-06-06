
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
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand




def rdf_description(name,notation='xml' ):
    """
    Funtion takes  title of node, and rdf notation.
    """
    valid_formats = ["xml", "n3", "ntriples", "trix"]
    default_graph_uri = "http://gstudio.gnowledge.org/rdfstore"
   # default_graph_uri = "http://example.com/"
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
    #rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    graph.bind("gstudio", "http://gnowledge.org/")
    exclusion_fields = ["id", "rght", "node_ptr_id", "image", "lft", "_state", "_altnames_cache", "_tags_cache", "nid_ptr_id", "_mptt_cached_fields"]

    #verifies the type of node 
    
    
    node=NID.objects.get(title=name)
    node_type=node.reftype
    
    

    if (node_type=='Gbobject' ):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
    elif (node_type=='None'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)  
		   
    elif (node_type=='Processes'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
		  
    elif (node_type=='System'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
		
    elif (node_type=='Objecttype'):
    	node=Objecttype.objects.get(title=name)
    	rdflib=link(node)

    elif (node_type=='Attributetype'):
    	node=Attributetype.objects.get(title=name)
        rdflib=link(node)
    	
    elif (node_type=='Complement'):
    	node=Complement.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='Union'):
    	node=Union.objects.get(title=name)
    	rdflib=link(node)
    	
    elif (node_type=='Intersection'):
    	node=Intersection.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='Expression'):
    	node=Expression.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='Processtype'):
    	node=Processtype.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='Systemtype'):
    	node=Systemtype.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='AttributeSpecification'):
    	node=AttributeSpecification.objects.get(title=name)
    	rdflib=link(node) 	 
    
    elif (node_type=='RelationSpecification'):
    	node=RelationSpecification.objects.get(title=name)
    	rdflib=link(node) 	 
    
    elif(node_type=='Attribute'):
    	node=Attribute.objects.get(title=name)
    	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    
    elif(node_type=='Relationtype' ):
    	node=Relationtype.objects.get(title=name)
    	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    
    elif(node_type=='Metatype'):
    	node=Metatype.objects.get(title=name)
    	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    else:
	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
		
        
    
    node_dict=node.__dict__

    subject=str(node_dict['id'])
    for key in node_dict:
        if key not in exclusion_fields:
            predicate=str(key)
            pobject=str(node_dict[predicate])
            graph.add((rdflib[subject], rdflib[predicate], Literal(pobject)))

     
    rdf_code=graph.serialize(format=notation)
    
    graph.commit()
    print rdf_code
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







class Command(BaseCommand):
	def handle(self,*args,**options):
		
                # verifies and pass  the node rdf_discription() to display the rdf accordingly.
		
		inr=0
		
		object_list=NID.objects.all()
		for each in object_list:
    			rdf_description(object_list[inr],*args)
    			inr=inr+1





