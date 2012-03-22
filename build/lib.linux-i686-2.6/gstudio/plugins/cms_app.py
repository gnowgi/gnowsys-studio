"""Applications hooks for gstudio.plugins"""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from gstudio.plugins.settings import APP_MENUS


class GstudioApphook(CMSApp):
    """Gstudio's Apphook"""
    name = _('Gstudio App Hook')
    urls = ['gstudio.urls']
    menus = APP_MENUS

apphook_pool.register(GstudioApphook)
