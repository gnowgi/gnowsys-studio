
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

"""Views for Gstudio forms"""
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from gstudio.forms import *


def addmetatype(request):
    if request.method == 'POST':
        formset = MetatypeForm(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect("/nodetypes/")
 
 
        
    else:
       
        formset = MetatypeForm()


    variables = RequestContext(request,{'formset':formset})
    template = "gstudioforms/gstudiometatypeform.html"
    return render_to_response(template, variables)

    

def addobjecttype(request):
        if request.method == 'POST':
            formset = ObjecttypeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
 
            
                    
        else:

            formset = ObjecttypeForm()

        template = "gstudioforms/gstudioobjecttypeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)



def addrelationtype(request):
        if request.method == 'POST':
            formset = RelationtypeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = RelationtypeForm()

        template = "gstudioforms/gstudiorelationtypeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)



def addattributetype(request):
        if request.method == 'POST':
            formset = AttributetypeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = AttributetypeForm()

        template = "gstudioforms/gstudioattributetypeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addsystemtype(request):
        if request.method == 'POST':
            formset = SystemtypeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = SystemtypeForm()

        template = "gstudioforms/gstudiosystemtypeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addprocesstype(request):
        if request.method == 'POST':
            formset = ProcesstypeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = ProcesstypeForm()

        template = "gstudioforms/gstudioprocesstypeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addattribute(request):
        if request.method == 'POST':
            formset = AttributeForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = AttributeForm()

        template = "gstudioforms/gstudioattributeform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addrelation(request):
        if request.method == 'POST':
            formset = RelationForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = RelationForm()

        template = "gstudioforms/gstudiorelationform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addcomplement(request):
        if request.method == 'POST':
            formset = ComplementForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = ComplementForm()

        template = "gstudioforms/gstudiocomplementform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addunion(request):
        if request.method == 'POST':
            formset = UnionForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = UnionForm()

        template = "gstudioforms/gstudiounionform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)


def addintersection(request):
        if request.method == 'POST':
            formset = IntersectionForm(request.POST)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect("/nodetypes/")
            
                    
        else:

            formset = IntersectionForm()

        template = "gstudioforms/gstudiointersectionform.html"
        variables = RequestContext(request,{'formset':formset})
        return render_to_response(template, variables)












