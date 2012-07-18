from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from gstudio.settings import GSTUDIO_VERSIONING
from gstudio.admin.forms import AttributeCharFieldAdminForm
from django.template.defaultfilters import slugify
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeCharFieldAdmin(parent_class):
    fieldsets=((_('AttributeCharField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value',)} 
    class Media:
        js = ("gstudio/js/attribute.js",)
    def save_model(self, request, attributecharfield, form, change):
    	attributecharfield.title = attributecharfield.composed_sentence
        attributecharfield.slug =   slugify(attributecharfield.title)
        attributecharfield.save()
 
