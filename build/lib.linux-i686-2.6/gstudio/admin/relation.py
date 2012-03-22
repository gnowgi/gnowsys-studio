"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import RelationAdminForm
import reversion

class RelationAdmin(reversion.VersionAdmin):
    def save_model(self, request, relation, form, change):
        relation.title = relation.composed_sentence
        relation.save()

