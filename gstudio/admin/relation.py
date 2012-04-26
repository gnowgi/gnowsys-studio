"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import RelationAdminForm
import reversion
from django.template.defaultfilters import slugify

class RelationAdmin(reversion.VersionAdmin):
    fieldsets=((_('Relation'),{'fields': ('relationtype','relationtype_scope','left_subject' ,'left_subject_scope','right_subject','right_subject_scope','last_update','creation_date')}),

)
    
    def get_title(self, edge):
        """Return the title with word count and number of comments"""
        title = _('%(title)s (%(word_count)i words)') % \
                {'title': nodetype.title, 'word_count': nodetype.word_count}
        comments = nodetype.comments.count()
        if comments:
            return _('%(title)s (%(comments)i comments)') % \
                   {'title': title, 'comments': comments}
        return title
    get_title.short_description = _('title')
    def save_model(self, request, relation, form, change):
        relation.title = relation.composed_sentence
        relation.slug = slugify(relation.title)
        relation.save()

