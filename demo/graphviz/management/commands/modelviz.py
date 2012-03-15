
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


#!/usr/bin/env python
import getopt, sys

from optparse import make_option

from django.template import Template, Context
from django.db import models
from django.db.models import get_models
from django.db.models.fields.related import \
    ForeignKey, OneToOneField, ManyToManyField

from django.core.management.base import AppCommand

try:
    from django.db.models.fields.generic import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

head_template = """
digraph name {
  fontname = "Helvetica"
  fontsize = 8

  node [
    fontname = "Helvetica"
    fontsize = 8
    shape = "plaintext"
  ]
   edge [
    fontname = "Helvetica"
    fontsize = 8
  ]

"""

body_template = """
  {% for model in models %}
    {% for relation in model.relations %}
    {{ relation.target }} [label=<
        <TABLE BGCOLOR="palegoldenrod" BORDER="0" CELLBORDER="0" CELLSPACING="0">
        <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER" BGCOLOR="olivedrab4"
        ><FONT FACE="Helvetica Bold" COLOR="white"
        >{{ relation.target }}</FONT></TD></TR>
        </TABLE>
        >]
    {{ model.name }} -> {{ relation.target }}
    [label="{{ relation.name }}"] {{ relation.arrows }};
    {% endfor %}
  {% endfor %}

  {% for model in models %}
    {{ model.name }} [label=<
    <TABLE BGCOLOR="palegoldenrod" BORDER="0" CELLBORDER="0" CELLSPACING="0">
     <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER" BGCOLOR="olivedrab4"
     ><FONT FACE="Helvetica Bold" COLOR="white"
     >{{ model.name }}</FONT></TD></TR>

    {% if not disable_fields %}
        {% for field in model.fields %}
        <TR><TD ALIGN="LEFT" BORDER="0"
        ><FONT {% if field.blank %}COLOR="#7B7B7B" {% endif %}FACE="Helvetica Bold">{{ field.name }}</FONT
        ></TD>
        <TD ALIGN="LEFT"
        ><FONT {% if field.blank %}COLOR="#7B7B7B" {% endif %}FACE="Helvetica Bold">{{ field.type }}</FONT
        ></TD></TR>
        {% endfor %}
    {% endif %}
    </TABLE>
    >]
  {% endfor %}
"""

tail_template = """
}
"""

def generate_dot(app_labels, **kwargs):
    disable_fields = kwargs.get('disable_fields', False)

    dot = head_template

    for app_label in app_labels:
        app = models.get_app(app_label)
        graph = Context({
            'name': '"%s"' % app.__name__,
            'disable_fields': disable_fields,
            'models': []
            })

        for appmodel in get_models(app):
            model = {
                'name': appmodel.__name__,
                'fields': [],
                'relations': []
                }

            # model attributes
            def add_attributes():
                model['fields'].append({
                    'name': field.name,
                    'type': type(field).__name__,
                    'blank': field.blank
                    })

            for field in appmodel._meta.fields:
                add_attributes()

            if appmodel._meta.many_to_many:
                for field in appmodel._meta.many_to_many:
                    add_attributes()

            # relations
            def add_relation(extras=""):
                _rel = {
                    'target': field.rel.to.__name__,
                    'type': type(field).__name__,
                    'name': field.name,
                    'arrows': extras
                    }
                if _rel not in model['relations']:
                    model['relations'].append(_rel)

            for field in appmodel._meta.fields:
                if isinstance(field, ForeignKey):
                    add_relation()
                elif isinstance(field, OneToOneField):
                    add_relation("[arrowhead=none arrowtail=none]")

            if appmodel._meta.many_to_many:
                for field in appmodel._meta.many_to_many:
                    if isinstance(field, ManyToManyField):
                        add_relation("[arrowhead=normal arrowtail=normal]")
                    elif isinstance(field, GenericRelation):
                        add_relation(
                            '[style="dotted"] [arrowhead=normal arrowtail=normal]')
            graph['models'].append(model)

        t = Template(body_template)
        dot += '\n' + t.render(graph)

    dot += '\n' + tail_template

    return dot

class Command(AppCommand):
    option_list = AppCommand.option_list + (
        make_option('--disable_fields', default=False, dest='disable_fields',
            help='Hide fields.'),
    )
    help = "Prints a Graphviz .dot file from models ."
    
    def handle(self, *app_labels, **options):
        disable_fields = options.get('disable_fields', False)
        return generate_dot(app_labels, **options)


