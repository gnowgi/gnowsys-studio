
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _ 
from django.template.defaultfilters import slugify

from gstudio.admin.forms import AttributeSpecificationAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeSpecificationAdmin(parent_class):
    fieldsets=((_('AttributeSpecification'),{'fields': ('metatypes','title','attributetype','subjects','slug')}),

)
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request, attributespecification, form, change):
        #attributespecification.title = attributespecification.composed_subject
        attributespecification.slug =   slugify(attributespecification.title)
        attributespecification.save()
    
