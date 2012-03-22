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


"""Forms for Objectapp admin"""
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

import reversion
from objectapp.models import Gbobject
from objectapp.models import Objecttype
from objectapp.models import System
from objectapp.models import Process
from objectapp.models import Systemtype
from gstudio.models import Edge
from gstudio.models import Node
from gstudio.models import Relation
from gstudio.models import Attribute
from gstudio.models import Processtype
from gstudio.models import Nodetype
from gstudio.models import Metatype

from objectapp.admin.widgets import TreeNodeChoiceField
from objectapp.admin.widgets import MPTTFilteredSelectMultiple
from objectapp.admin.widgets import MPTTModelMultipleChoiceField


class ProcessAdminForm(forms.ModelForm):

    class Meta:
        """SystemAdminForm's Meta"""
        model = Process

class SystemAdminForm(forms.ModelForm):

    class Meta:
        """SystemAdminForm's Meta"""
        model = System



class ObjecttypeAdminForm(forms.ModelForm):
    """Form for Objecttype's Admin"""
    parent = TreeNodeChoiceField(
        label=_('parent Objecttype').capitalize(),
        required=False, empty_label=_('No parent Objecttype'),
        queryset=Objecttype.tree.all())

    def __init__(self, *args, **kwargs):
        super(ObjecttypeAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(Objecttype, 'id')
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget, rel, self.admin_site)

    def clean_parent(self):
        """Check if Objecttype parent is not selfish"""
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A Objecttype cannot be parent of itself.'))
        return data

    class Meta:
        """ObjecttypeAdminForm's Meta"""
        model = Objecttype


class GbobjectAdminForm(forms.ModelForm):
    """Form for Gbobject's Admin"""
    objecttypes = MPTTModelMultipleChoiceField(
        label=_('Objecttypes'), required=False,
        queryset=Objecttype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('objecttypes'), False,
                                          attrs={'rows': '10'}))


    def __init__(self, *args, **kwargs):
        super(GbobjectAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToManyRel(Objecttype, 'id')

        self.fields['objecttypes'].widget = RelatedFieldWidgetWrapper(
            self.fields['objecttypes'].widget, rel, self.admin_site)


        self.fields['sites'].initial = [Site.objects.get_current()]

    class Meta:
        """GbobjectAdminForm's Meta"""
        model = Gbobject
