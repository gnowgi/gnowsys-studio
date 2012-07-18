from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeIPAddressFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeIPAddressFieldAdmin(parent_class):
    fieldsets=((_('AttributeIPAddressField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value', )}  
    def save_model(self, request, attributeipaddressfield, form, change):
    	attributeipaddressfield.title = attributeipaddressfield.composed_sentence
        attributeipaddressfield.slug =   slugify(attributeipaddresfield.title)
        attributeipaddressfield.save()

