"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import MetatypeAdminForm
import reversion

class MetatypeAdmin(reversion.VersionAdmin):
    """Admin for Metatype model"""
    form = MetatypeAdminForm
    fields = ('title','altnames', 'parent', 'description', 'slug')
    list_display = ('title', 'slug', 'get_tree_path', 'description')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')
    list_filter = ('parent',)

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(MetatypeAdmin, self).__init__(model, admin_site)

    def get_tree_path(self, metatype):
        """Return the metatype's tree path in HTML"""
        try:
            return '<a href="%s" target="blank">/%s/</a>' % \
                   (metatype.get_absolute_url(), metatype.tree_path)
        except NoReverseMatch:
            return '/%s/' % metatype.tree_path
    get_tree_path.allow_tags = True
    get_tree_path.short_description = _('tree path')
