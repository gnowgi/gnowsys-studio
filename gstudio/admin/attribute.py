"""MetatypeAdmin for Gstudio"""
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from gstudio.admin.forms import AttributeAdminForm
from gstudio.models import *
import reversion
from django.template.defaultfilters import slugify

class AttributeAdmin(reversion.VersionAdmin):
    fieldsets=((_('Attribute'),{'fields': ('subject','subject_scope','attributetype','attributetype_scope','svalue','value_scope','last_update','creation_date')}),

)
    
    
    class Media:
        js = ("gstudio/js/gstudiojs.js",)
    
    def save_model(self, request, attribute, form, change):
        attribute.title = attribute.composed_sentence
        attribute.slug =   slugify(attribute.title)
        attribute.save()





