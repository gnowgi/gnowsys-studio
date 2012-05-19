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



"""Views for Gstudio nodetypes"""
from django.shortcuts import redirect 
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from gstudio.gnowql import *
#import networkx as nx
#import d3 
import json
import os
from gstudio.views.decorators import protect_nodetype
from gstudio.views.decorators import update_queryset



	
def graph_json(request, node_id): 
    
    if(node_id=='189087228'):
        jsonFile = open( os.path.join(os.path.dirname(__file__), '../static/gstudio/js/egonet.json'), "r")
        testjson = json.loads(jsonFile)

        return HttpResponse(str(jsonFile.read()), "application/json")

    try:
        node = NID.objects.get(id=node_id)
        node = node.ref 
    except:
	
        return HttpResponse("node not found", "text/html")

    return HttpResponse(node.get_graph_json(), "application/json")
   




def force_graph(request, node_id):
    return render_to_response('gstudio/graph1.html',{'node_id': node_id })

def version_graph_json(request,ssid):
	
    if(ssid=='189087228'):
        jsonFile = open( os.path.join(os.path.dirname(__file__), '../static/gstudio/js/egonet.json'), "r")
        #testjson = json.loads(jsonFile)

        return HttpResponse(str(jsonFile.read()), "application/json")

    try:
        node = Version.objects.get(id=ssid)
	
        node = node.object.ref     
    except:
        return HttpResponse("Node not found.", "text/html")

    return HttpResponse(node.get_Version_graph_json(ssid), "application/json")

#node = get_node(str(object_id))
#ot = Objecttype.objects.get(title='place')
#G = ot.get_radial_graph_json()
#    
#    G = nx.DiGraph()
#    
#    G.add_node(node)
#    
#    for key in node.get_nbh.keys():
#        # is null
#        if isinstance(node[key],list):
#           G.add_nodes_from(node[key])
#
#            for item in node[key]:
#                G.add_edge()                
#    


#    return ast(nodetype, permanent=True)
