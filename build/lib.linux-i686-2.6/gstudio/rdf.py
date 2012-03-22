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


# This project incorporates work covered by the following copyright and permission notice:  

#    Copyright (c) 2009, Julien Fache
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:

#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of the author nor the names of other
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE.


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

