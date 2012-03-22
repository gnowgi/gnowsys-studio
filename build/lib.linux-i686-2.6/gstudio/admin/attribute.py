"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from gstudio.admin.forms import AttributeAdminForm
from gstudio.models import *
import reversion

class AttributeAdmin(reversion.VersionAdmin):
    class Media:
        js = ("gstudio/js/gstudiojs.js",)
    
    def save_model(self, request, attribute, form, change):
        attribute.title = attribute.composed_attribution
        attribute.save()




