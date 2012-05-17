from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from gstudio.settings import GSTUDIO_VERSIONING
from gstudio.admin.forms import AttributeCharFieldAdminForm
import reversion
if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeCharFieldAdmin(parent_class):
    pass
 
