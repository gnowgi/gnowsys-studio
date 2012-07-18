from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from django.template.defaultfilters import slugify
from gstudio.admin.forms import ComplementAdminForm
import reversion
from gstudio.settings import GSTUDIO_VERSIONING
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class ComplementAdmin(parent_class):
    fieldsets=((_('Complement'),{'fields':('title','nodetypes','metatypes','slug')}),)
    
    def save_model(self, request, complement, form, change):
        #complement.title=self.composed_subject
        complement.slug=slugify(complement.title)
        complement.save()
