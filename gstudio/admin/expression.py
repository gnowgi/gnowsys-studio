"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from gstudio.admin.forms import ExpressionAdminForm
import reversion
from gstudio.settings import GSTUDIO_VERSIONING
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class ExpressionAdmin(parent_class):
    fieldsets=((_('Expression'),{'fields': ('metatypes','title','left_term','relationtype','right_term','slug')}),
               )
    prepopulated_fields = {'slug': ('title', )}
    def save_model(self, request,expression, form, change):
        expression.title = expression.composed_sentence
        expression.slug =   slugify(expression.title)
        expression.save()

