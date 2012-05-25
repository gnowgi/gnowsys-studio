
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




def get_nodetype(name):
    """
    returns the model the id belongs to.  
    """    
    try:
        """ 
        ALGO:     get object id, go to version model, return for the given id.
        """
        node = NID.objects.get(title=str(name))
        # Retrieving only the relevant tupleset for the versioned objects
        vrs = Version.objects.filter(type=0 , object_id=node.id) 
        # Returned value is a list, so splice it .
        vrs =  vrs[0]
       
    except Error:
        return "The item was not found."
    if (str(vrs.object)=='None'):
	return str(vrs.object)
    else:	    
    	return vrs.object._meta.module_name   
    

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
    
    
    #node=NID.objects.get(title=name)
    node_type=get_nodetype(name)
    
    

    if (node_type=='gbobject'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
    if (node_type=='None'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)  
		   
    elif (node_type=='processes'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
		  
    elif (node_type=='system'):
    	node=Gbobject.objects.get(title=name)
    	rdflib=link(node)
		
    elif (node_type=='objecttype'):
    	node=Objecttype.objects.get(title=name)
    	rdflib=link(node)

    elif (node_type=='attributetype'):
    	node=Attributetype.objects.get(title=name)
        rdflib=link(node)
    	
    elif (node_type=='complement'):
    	node=Complement.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='union'):
    	node=Union.objects.get(title=name)
    	rdflib=link(node)
    	
    elif (node_type=='intersection'):
    	node=Intersection.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='expression'):
    	node=Expression.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='processtype'):
    	node=Processtype.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='systemtype'):
    	node=Systemtype.objects.get(title=name)
    	rdflib=link(node)
    
    elif (node_type=='attributespecification'):
    	node=AttributeSpecification.objects.get(title=name)
    	rdflib=link(node) 	 
    
    elif (node_type=='relationspecification'):
    	node=RelationSpecification.objects.get(title=name)
    	rdflib=link(node) 	 
    
    elif(node_type=='attribute'):
    	node=Attribute.objects.get(title=name)
    	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    
    elif(node_type=='relationtype' ):
    	node=Relationtype.objects.get(title=name)
    	rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    
    elif(node_type=='metatype'):
    	node=Metatype.objects.get(title=name)
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
    make_file(name,rdf_code)





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


#makes individual rdf file for nodes.
def make_file(name,rdf_code):
    	x=str(name)
	temp_path = '/home/labadmin/dev/gnowsys-studio/demo/rdffiles/' + x + '.rdf'
	file = open(temp_path, 'w')
	file.write(rdf_code)
	file.close()
        print "executed"




class Command(BaseCommand):
	def handle(self,*args,**options):
		
                # verify the type of the node and pass the node to display the rdf accordingly.
		
		inr=0
		
		object_list=NID.objects.all()
		for each in object_list:
    			rdf_description(object_list[inr],*args)
    			inr=inr+1





