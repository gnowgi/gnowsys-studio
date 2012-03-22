from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import AttributeEmailFieldAdminForm
import reversion

class AttributeEmailFieldAdmin(reversion.VersionAdmin):
    pass
