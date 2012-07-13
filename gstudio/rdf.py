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

def rdf_description(name, notation='xml' ):
    """
    Funtion takes  title of node, and rdf notation.
    """
    valid_formats = ["xml", "n3", "ntriples", "trix"]
    default_graph_uri = "http://gstudio.gnowledge.org/rdfstore"
    configString = "/var/tmp/rdfstore"

    # Get the Sleepycat plugin.
    store = plugin.get('Sleepycat', Store)('rdfstore')

    # Open previously created store, or create it if it doesn't exist yet
    graph = Graph(store="Sleepycat",
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
    node=Objecttype.objects.get(title=name)
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

