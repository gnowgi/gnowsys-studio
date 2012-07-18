"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from markitup.widgets import AdminMarkItUpWidget

from gstudio.admin.forms import RelationAdminForm
import reversion
from django.template.defaultfilters import slugify
from gstudio.settings import GSTUDIO_VERSIONING

if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class RelationAdmin(parent_class):
    fieldsets=((_('Relation'),{'fields': ('relationtype','relationtype_scope','left_subject' ,'left_subject_scope','right_subject','right_subject_scope','metatypes')}),

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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = AdminMarkItUpWidget()
        return super(RelationAdmin, self).formfield_for_dbfield(db_field, **kwargs)
