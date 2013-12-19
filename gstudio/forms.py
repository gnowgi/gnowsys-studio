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



from gstudio.models import *
from django.forms import ModelForm
from django.forms import *
from django.contrib.admin import widgets  
from registration.forms import *
from recaptcha import fields as recaptcha_fields

from registration.forms import RegistrationForm

class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = recaptcha_fields.ReCaptchaField()


class UserRegistrationForm(RegistrationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    recaptcha = recaptcha_fields.ReCaptchaField()

class MetatypeForm(ModelForm):

    class Meta:
        model = Metatype

class ObjecttypeForm(ModelForm):                 






    class Meta:
        model = Objecttype
        fields = ('title', 'altnames','plural','parent','slug','metatypes','tags',
                      'status','content','prior_nodes','posterior_nodes','password','login_required','sites')

class AttributetypeForm(ModelForm):

    class Meta:
         model = Attributetype
         fields =('title','altnames','subjecttype','applicable_nodetypes','dataType',
		  'slug','status','content','prior_nodes','posterior_nodes','password','login_required','sites')

class RelationtypeForm(ModelForm):

    class Meta:
         model = Relationtype
         fields =('title','altnames','slug','inverse','left_subjecttype','left_applicable_nodetypes','right_subjecttype',
		 'right_applicable_nodetypes','content','prior_nodes','posterior_nodes','sites')
class SystemtypeForm(ModelForm):

    class Meta:
         model =Systemtype
         fields =('title','altnames','content','parent','slug','status','nodetype_set','relationtype_set','attributetype_set','metatype_set','processtype_set',
		 'prior_nodes','posterior_nodes','sites')


class ProcesstypeForm(ModelForm):

    class Meta:
         model =Processtype
         fields =('title','altnames','content','parent','slug','status','changing_attributetype_set','changing_relationtype_set',
		 'prior_nodes','posterior_nodes','sites')


class RelationForm(ModelForm):
    class Meta:
        model = Relation

class AttributeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttributeForm, self).__init__(*args, **kwargs)
        self.fields['last_update'].widget = widgets.AdminSplitDateTime()
        self.fields['creation_date'].widget = widgets.AdminSplitDateTime()

    class Meta:
        model = Attribute


class ComplementForm(ModelForm):
    class Meta:
        model = Complement

class UnionForm(ModelForm):
    class Meta:
        model = Union

class IntersectionForm(ModelForm):
    class Meta:
        model = Intersection


