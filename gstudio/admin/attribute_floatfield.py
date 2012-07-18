from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeFloatFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeFloatFieldAdmin(parent_class):
    fieldsets=((_('AttributeFloatField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value', )}
    def save_model(self, request, attributefloatfield, form, change):
    	attributefloatfield.title = attributefloatfield.composed_sentence
        attributefloatfield.slug =   slugify(attributefloatfield.title)
        attributefloatfield.save()

