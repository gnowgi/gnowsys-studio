
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


"""Views for Gstudio metatypes"""
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from gstudio.models import Metatype
from gstudio.settings import PAGINATION
from gstudio.views.decorators import template_name_for_nodetype_queryset_filtered


def get_metatype_or_404(path):
    """Retrieve a Metatype by a path"""
    path_bits = [p for p in path.split('/') if p]
    return get_object_or_404(Metatype, slug=path_bits[-1])


def metatype_detail(request, path, page=None, **kwargs):
    """Display the nodetypes of a metatype"""
    extra_context = kwargs.pop('extra_context', {})

    metatype = get_metatype_or_404(path)
    if not kwargs.get('template_name'):
        kwargs['template_name'] = template_name_for_nodetype_queryset_filtered(
            'metatype', metatype.slug)

    extra_context.update({'metatype': metatype})
    kwargs['extra_context'] = extra_context

    return object_list(request, queryset=metatype.nodetypes_published(),
                       paginate_by=PAGINATION, page=page,
                       **kwargs)
