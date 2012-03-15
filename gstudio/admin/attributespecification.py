
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _ 

from gstudio.admin.forms import AttributeSpecificationAdminForm
import reversion

class AttributeSpecificationAdmin(reversion.VersionAdmin):
    pass
