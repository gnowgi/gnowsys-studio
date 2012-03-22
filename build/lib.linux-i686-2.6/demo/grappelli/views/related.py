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


# coding: utf-8

# PYTHON IMPORTS
import operator

# DJANGO IMPORTS
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.db import models
from django.db.models.query import QuerySet
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import smart_str
import django.utils.simplejson as simplejson


def returnattr(obj, attr):
    if callable(getattr(obj, attr)):
        return getattr(obj, attr)()
    return getattr(obj, attr)


def get_label(f):
    if getattr(f, "related_label", None):
        return f.related_label()
    return f.__unicode__()


@never_cache
def related_lookup(request):
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponseForbidden('<h1>Permission denied</h1>')
    data = []
    if request.method == 'GET':
        if request.GET.has_key('object_id') and request.GET.has_key('app_label') and request.GET.has_key('model_name'):
            object_id = request.GET.get('object_id')
            app_label = request.GET.get('app_label')
            model_name = request.GET.get('model_name')
            if object_id:
                try:
                    model = models.get_model(app_label, model_name)
                    obj = model.objects.get(pk=object_id)
                    data.append({"value":obj.id,"label":get_label(obj)})
                    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
                except:
                    pass
    data = [{"value":None,"label":""}]
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')


@never_cache
def m2m_lookup(request):
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponseForbidden('<h1>Permission denied</h1>')
    data = []
    if request.method == 'GET':
        if request.GET.has_key('object_id') and request.GET.has_key('app_label') and request.GET.has_key('model_name'):
            object_ids = request.GET.get('object_id').split(',')
            app_label = request.GET.get('app_label')
            model_name = request.GET.get('model_name')
            model = models.get_model(app_label, model_name)
            data = []
            if len(object_ids):
                for obj_id in object_ids:
                    if obj_id:
                        try:
                            obj = model.objects.get(pk=obj_id)
                            data.append({"value":obj.id,"label":get_label(obj)})
                        except:
                            data.append({"value":obj_id,"label":_("?")})
            return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
    data = [{"value":None,"label":""}]
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')


@never_cache
def autocomplete_lookup(request):
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponseForbidden('<h1>Permission denied</h1>')
    data = []
    if request.method == 'GET':
        if request.GET.has_key('term') and request.GET.has_key('app_label') and request.GET.has_key('model_name'):
            term = request.GET.get("term")
            app_label = request.GET.get('app_label')
            model_name = request.GET.get('model_name')
            model = models.get_model(app_label, model_name)
            filters = {}
            # FILTER
            if request.GET.get('query_string', None):
                for item in request.GET.get('query_string').split("&"):
                    if item.split("=")[0] != "t":
                        filters[smart_str(item.split("=")[0])]=smart_str(item.split("=")[1])
            # SEARCH
            qs = model._default_manager.all()
            for bit in term.split():
                search = [models.Q(**{smart_str(item):smart_str(bit)}) for item in model.autocomplete_search_fields()]
                search_qs = QuerySet(model)
                search_qs.dup_select_related(qs)
                search_qs = search_qs.filter(reduce(operator.or_, search))
                qs = qs & search_qs
            data = [{"value":f.pk,"label":u'%s' % get_label(f)} for f in qs[:10]]
            label = ungettext(
                '%(counter)s result',
                '%(counter)s results',
            len(data)) % {
                'counter': len(data),
            }
            #data.insert(0, {"value":None,"label":label})
            return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
    data = [{"value":None,"label":_("Server error")}]
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')


