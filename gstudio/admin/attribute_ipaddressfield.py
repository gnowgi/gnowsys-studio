from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from gstudio.admin.forms import AttributeIPAddressFieldAdminForm
from gstudio.settings import GSTUDIO_VERSIONING
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeIPAddressFieldAdmin(parent_class):
    pass
