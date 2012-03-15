"""Custom spam checker backend for testing Objectapp"""
from django.core.exceptions import ImproperlyConfigured


raise ImproperlyConfigured('This backend only exists for testing')


def backend(gbobject):
    """Custom spam checker backend for testing Objectapp"""
    return False
