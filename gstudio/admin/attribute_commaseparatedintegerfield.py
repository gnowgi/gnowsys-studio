from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeCommaSeparatedIntegerFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeCommaSeparatedIntegerFieldAdmin(parent_class):
    fieldsets=((_('AttributeCommaSeparatedIntegerField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
    prepopulated_fields = {'svalue': ('value',)}  
    def save_model(self, request, attributecommaseperatedintegerfield, form, change):
    	attributecommaseperatedintegerfield.title = attributecommaseperatedintegerfield.composed_sentence
        attributecommaseperatedintegerfield.slug =   slugify(attributecommaseperatedintegerfield.title)
        attributecommaseperatedintegerfield.save()
