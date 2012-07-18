from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from gstudio.admin.forms import RelationSpecificationAdminForm
import reversion
from gstudio.settings import GSTUDIO_VERSIONING

if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class RelationSpecificationAdmin(parent_class):
    fieldsets=((_('RelationSpecification'),{'fields': ('metatypes','title','relationtype','subjects','slug')}),
               )
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request,relationspecification, form, change):
        #relationspecification.title = relationspecification.composed_subject                                                                              
        relationspecification.slug =   slugify(relationspecification.title)
        relationspecification.save()


