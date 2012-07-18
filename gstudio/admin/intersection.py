from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import IntersectionAdminForm
import reversion
from gstudio.settings import GSTUDIO_VERSIONING
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class IntersectionAdmin(parent_class):
    fieldsets=((_('Intersection'),{'fields': ('metatypes','title','nodetypes','slug')}),
               )
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request,intersection, form, change):
        #intersection.title = intersection.composed_subject
        intersection.slug =   slugify(intersection.title)
        intersection.save()

