from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeIntegerFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 


class AttributeIntegerFieldAdmin(parent_class):
    fieldsets=((_('AttributIntegerField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value', )}
    def save_model(self, request, attributeintegerfield, form, change):
    	attributeintegerfield.title = attributeintegerfield.composed_sentence
        attributeintegerfield.slug =   slugify(attributeintegerfield.title)
        attributeintegerfield.save()

