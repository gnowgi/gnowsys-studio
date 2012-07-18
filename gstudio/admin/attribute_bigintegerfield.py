from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from gstudio.settings import GSTUDIO_VERSIONING
from django.template.defaultfilters import slugify

from gstudio.admin.forms import AttributeBigIntegerFieldAdminForm
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
   parent_class = admin.ModelAdmin
class AttributeBigIntegerFieldAdmin(parent_class):

   fieldsets=((_('AttributeBigIntegerField'),{'fields': ('metatypes','attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope','value')}),

)
   prepopulated_fields = {'svalue': ('value', )} 
   def save_model(self, request, attributebigintegerfield, form, change):
   	attributebigintegerfield.title = attributebigintegerfield.composed_sentence
        attributebigintegerfield.slug =   slugify(attributebigintegerfield.title)
        attributebigintegerfield.save()

