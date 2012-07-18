from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeNullBooleanFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeNullBooleanFieldAdmin(parent_class):
    fieldsets=((_('AttributeNullBooleanField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value', )} 
    def save_model(self, request, attributenullbooleanfield, form, change):
    	attributenullbooleanfield.title = attributenullbooleanfield.composed_sentence
        attributenullbooleanfield.slug =   slugify(attributenullbooleanfield.title)
        attributenullbooleanfield.save()

