
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


from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Graph

from django.template import Template

from os import system
from django.conf import settings

import os
from os.path import join
_tmpdir = '/tmp' #os.environ['TMP']

class TEdge:
    def __init__(self, data, graph):
        self.start_node, self.end_node = data.gv_ends(graph)
        self.start_node_label = self.start_node.gv_node_label(graph)
        self.end_node_label = self.end_node.gv_node_label(graph)
        self.label = data.gv_edge_label(graph)
class TGraph:
    def __init__(self, graph):
        self.edges = []
        for e in graph.content_object.gv_edges(graph):
            self.edges.append(TEdge(e, graph))

def dot_file(request, slug, view=False, template='graphviz/dot_file.dot'):
    graph = Graph.objects.get(slug=slug)
    context = {'graph':TGraph(graph)}
    response = render_to_response(template, context, mimetype='text/plain',
                                  context_instance=RequestContext(request))
    if not view:
        response['Content-Disposition'] = 'attachment; filename=%s.dot' % slug
    return response

def image_file(request, slug, template='graphviz/dot_file.html'):
    resp = dot_file(request, slug, template)
    path_dot = join(_tmpdir, 'graphviz_tmp.dot')
    tdot = open(path_dot, 'w')
    tdot.write(resp.content)
    tdot.close()
    system('%s %s Tpng -o %s.png' % (settings.GRAPHVIZ_DOT_CMD, path_dot, path_dot))
    
    return HttpResponse('image '+path_dot+'.png')
