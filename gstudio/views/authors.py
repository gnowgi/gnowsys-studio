
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


"""Views for Gstudio authors"""
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from gstudio.models import Author
from gstudio.settings import PAGINATION
from gstudio.views.decorators import update_queryset
from gstudio.views.decorators import template_name_for_nodetype_queryset_filtered


author_list = update_queryset(object_list, Author.published.all)


def author_detail(request, username, page=None, **kwargs):
    """Display the nodetypes of an author"""
    extra_context = kwargs.pop('extra_context', {})

    author = get_object_or_404(Author, username=username)
    if not kwargs.get('template_name'):
        kwargs['template_name'] = template_name_for_nodetype_queryset_filtered(
            'author', author.username)

    extra_context.update({'author': author})
    kwargs['extra_context'] = extra_context

    return object_list(request, queryset=author.nodetypes_published(),
                       paginate_by=PAGINATION, page=page,
                       **kwargs)
