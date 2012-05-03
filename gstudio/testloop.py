import rdflib
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.namespace import Namespace
from rdflib.term import Literal
from rdflib.term import URIRef
from tempfile import mkdtemp
from gstudio.models import *

def rdf_description(name, notation='xml' ):
    """
    Funtion takes  title of node, and rdf notation.
    """
    valid_formats = ["xml", "n3", "ntriples", "trix"]
    default_graph_uri = "http://gstudio.gnowledge.org/rdfstore"
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
    rdflib = Namespace('http://sbox.gnowledge.org/gstudio/')
    graph.bind("gstudio", "http://gnowledge.org/")
    exclusion_fields = ["id", "rght", "node_ptr_id", "image", "lft", "_state", "_altnames_cache", "_tags_cache", "nid_ptr_id", "_mptt_cached_fields"]
    node=NID.objects.get(title=name)
    node_dict=node.__dict__

    subject=str(node_dict['id'])
    for key in node_dict:
        if key not in exclusion_fields:
            predicate=str(key)
            pobject=str(node_dict[predicate])
            graph.add((rdflib[subject], rdflib[predicate], Literal(pobject)))
     
     
    graph.commit()

    print graph.serialize(format=notation)

    graph.close()
i=0
p=NID.objects.all()
for each in p:
	rdf_description(p[i])
	i=i+1
	
