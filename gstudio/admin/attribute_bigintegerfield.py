from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from gstudio.settings import GSTUDIO_VERSIONING

from gstudio.admin.forms import AttributeBigIntegerFieldAdminForm
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
   parent_class = admin.ModelAdmin
class AttributeBigIntegerFieldAdmin(parent_class):
    pass
