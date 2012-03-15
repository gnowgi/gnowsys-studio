
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


"""
"""

   
class IGraphRoot:
    def gv_edges(self, graph):
        raise Exception('not implemented') 
    def gv_nodes(self, graph):
        raise Exception('not implemented') 

class INode:
    def gv_node_label(self, graph):
        return unicode(self)

class IEdge:
    def gv_ends(self, graph):
        ''' should returns (node_source, node_target)
        '''
        raise Exception('not implemented') 
    def gv_edge_label(self, graph):
        return unicode(self)
