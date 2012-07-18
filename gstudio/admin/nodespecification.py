from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from gstudio.admin.forms import NodeSpecificationAdminForm
import reversion
from gstudio.settings import GSTUDIO_VERSIONING
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class NodeSpecificationAdmin(parent_class):
    fieldsets=((_('NodeSpecification'),{'fields': ('metatypes','title','relations','attributes','subject','slug')}),
               )
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request,nodespecification, form, change):
        #nodespecification.title = nodespecification.composed_subject                                                                                
        nodespecification.slug =   slugify(nodespecification.title)
        nodespecification.save()
    
