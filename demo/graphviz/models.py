
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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Graph(models.Model):
    """ the object defined by the generic relation should have
        a method gv_links(graph) that returns a sequence of links.
        a method gv_nodes(graph) that returns a sequence of nodes.

        a link should have a method gv_ends(graph) that returns a sequence
        of nodes [start, end].
        
        a link may have a method gv_visual(graph) that returns a ArrowVisual instance or None

        a node may have a method gv_visual(graph) that returns
        a NodeVisual instance or None.
        
        links may have a gv_link_label(graph) method
        nodes may have a gv_node_label(graph) method
        
        see also interfaces.py module.
    """
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def view_dot_file(self):
        return '<a href=/graphviz/dot_view/%s/>view</a>' % self.slug
    view_dot_file.allow_tags = True
    
    def download_dot_file(self):
        return '<a href=/graphviz/dot_file/%s/>download</a>' % self.slug
    download_dot_file.allow_tags = True
    
    def download_image(self):
        return '<a href=/graphviz/image_file/%s/>download (TODO)</a>' % self.slug
    download_image.allow_tags = True
    
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Graphes'

NODE_SHAPE_CHOICES = (('box','Box'),
                      ('circle','Circle'),
                      ('doublecircle','Double circle'),
                      ('box3d','Box 3D'),
                      ('diamond','Diamond'),
                      )
class NodeVisual(models.Model):
    """ the content_type attribute is used to define the default Node
        when no method gv_node is provided.
    """
    shape = models.CharField(max_length=50, default='circle', choices=NODE_SHAPE_CHOICES)
    graph = models.ForeignKey(Graph)
    content_type = models.ForeignKey(ContentType)
    
    def __unicode__(self):
        return self.shape

ARROW_SHAPE_CHOICES = (('box','box'),
                       ('crow','crow'),
                       ('diamond','diamond'),
                       ('dot','dot'),
                       ('inv','inv'),
                       ('none','none'),
                       ('normal','normal'),
                       ('tee','tee'),
                       ('vee','vee'),
                       )
ARROW_MODIFIER_CHOICES = (('l','left'),
                          ('r','right'),
                          ('o','non-filled'),
                          )
class ArrowVisual(models.Model):
    """ the content_type attribute is used to define the default Arrow
        when no method gv_arrow is provided.
    """
    shape = models.CharField(max_length=50, default='normal', choices=ARROW_SHAPE_CHOICES)
    modifier = models.CharField(max_length=1, default='r', choices=ARROW_MODIFIER_CHOICES)
    graph = models.ForeignKey(Graph)
    content_type = models.ForeignKey(ContentType)
    
    def __unicode__(self):
        return self.shape

class CacheImage(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)
    graph = models.ForeignKey(Graph)
    file = models.ImageField(upload_to='graph_images')
    
    def graphic(self):
        return '<img name=image%d src=%s>' % (self.pk, self.file.url)
    graphic.allow_tags = True
            
    def __unicode__(self):
        return self.graph.name
    class Meta:
        verbose_name_plural = 'Caches images'
