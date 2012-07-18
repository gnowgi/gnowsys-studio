from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from gstudio.admin.forms import AttributeImageFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeImageFieldAdmin(parent_class):
    fieldsets=((_('AttributeImageField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

) 
    prepopulated_fields = {'svalue': ('value', )}
    def save_model(self, request, attributeimagefield, form, change):
    	attributeimagefield.title = attributeimagefield.composed_sentence
        attributeimagefield.slug =   slugify(attributeimagefield.title)
        attributeimagefield.save()

