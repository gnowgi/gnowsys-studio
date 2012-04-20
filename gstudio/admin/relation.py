"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import RelationAdminForm
import reversion

class RelationAdmin(reversion.VersionAdmin):
    fieldsets=((_('Relation'),{'fields': ('title','last_update','creation_date','relationtype_scope','relationtype','left_subject_scope','left_subject' ,'right_subject_scope','right_subject')}),

)
    def save_model(self, request, relation, form, change):
        relation.title = relation.composed_sentence
        relation.save()

