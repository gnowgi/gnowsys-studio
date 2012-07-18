from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from gstudio.admin.forms import UnionAdminForm
from gstudio.settings import GSTUDIO_VERSIONING

import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class UnionAdmin(parent_class):
    fieldsets=((_('Union'),{'fields': ('metatypes','title','nodetypes','slug')}),
               )
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request,union, form, change):
        #union.title = union.composed_sentence
        union.slug =   slugify(union.title)
        union.save()
