"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import ExpressionAdminForm
import reversion

class ExpressionAdmin(reversion.VersionAdmin):
    def save_model(self, request, expression, form, change):
        expression.title = expression.composed_sentence
        expression.save()

