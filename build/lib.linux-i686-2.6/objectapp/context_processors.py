"""Context Processors for Objectapp"""
from objectapp import __version__


def version(request):
    """Adds version of Objectapp to the context"""
    return {'OBJECTAPP_VERSION': __version__}
