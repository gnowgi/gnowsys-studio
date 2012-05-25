"""AttributeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from gstudio.admin.forms import AttributeAdminForm
from gstudio.models import *
import reversion
from django.template.defaultfilters import slugify
from gstudio.settings import GSTUDIO_VERSIONING

if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class AttributeAdmin(parent_class):
    fieldsets=((_('Attribute'),{'fields': ('attributetype','attributetype_scope','subject','subject_scope','svalue','value_scope')}),

)
    
    

    class Media:
        js = ("gstudio/js/gstudio.js",)
    
    def save_model(self, request, attribute, form, change):
        attribute.title = attribute.composed_sentence
        attribute.slug =   slugify(attribute.title)
        attribute.save()





