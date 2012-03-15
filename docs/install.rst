============
Installation
============

.. module:: gstudio

.. _dependencies:

Dependencies
============

Make sure to install these packages prior to installation :

* `Python 2.x`_ >= 2.5
* `Django`_ >= 1.3
* `django-mptt`_ >= 0.4.2
* `django-tagging`_ >= 0.3.1
* `BeautifulSoup`_ >= 3.2.0

The packages below are optionnal but needed for run the full test suite.

* `pyparsing`_ >= 1.5.5
* `django-xmlrpc`_ >= 0.1.3

Note that all the dependencies will be resolved if you install
Gstudio with :program:`pip` or :program:`easy_install`, excepting Django.

.. _getting-the-code:

Getting the code
================

.. highlight:: console

For the latest stable version of Gstudio use :program:`easy_install`: ::

  $ easy_install django-gstudio

or use :program:`pip`: ::

  $ pip install django-gstudio

You could also retrieve the last sources from
https://github.com/gnowgi/django-gstudio. Clone the repository
using :program:`git` and run the installation script: ::

  $ git clone git://github.com/gnowgi/django-gstudio.git
  $ cd django-gstudio
  $ python setup.py install

or more easily via :program:`pip`: ::

  $ pip install -e git://github.com/gnowgi/django-gstudio.git#egg=django-gstudio

.. _applications:

Applications
============

.. highlight:: python

Then register :mod:`gstudio`, and these following applications in the
:setting:`INSTALLED_APPS` section of your project's settings. ::

  INSTALLED_APPS = (
    # Your favorite apps
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging',
    'mptt',
    'gstudio',)

.. _template-context-processors:

Template Context Processors
===========================

Add these following
:setting:`template context processors<TEMPLATE_CONTEXT_PROCESSORS>` if not
already present. ::

  TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'gstudio.context_processors.version',) # Optional

.. _urls:

URLs
====

Add the following lines to your project's urls.py in order to display the
blog. ::

  url(r'^gstudio/', include('gstudio.urls')),
  url(r'^comments/', include('django.contrib.comments.urls')),

Note that the default gstudio URLset is provided for convenient usage, but
you can customize your URLs if you want. Here's how: ::

  url(r'^', include('gstudio.urls.capabilities')),
  url(r'^search/', include('gstudio.urls.search')),
  url(r'^sitemap/', include('gstudio.urls.sitemap')),
  url(r'^trackback/', include('gstudio.urls.trackback')),
  url(r'^gstudio/tags/', include('gstudio.urls.tags')),
  url(r'^gstudio/feeds/', include('gstudio.urls.feeds')),
  url(r'^gstudio/authors/', include('gstudio.urls.authors')),
  url(r'^gstudio/categories/', include('gstudio.urls.categories')),
  url(r'^gstudio/discussions/', include('gstudio.urls.discussions')),
  url(r'^gstudio/', include('gstudio.urls.quick_entry')),
  url(r'^gstudio/', include('gstudio.urls.entries')),
  url(r'^comments/', include('django.contrib.comments.urls')),

.. _static-files:

Static Files
============

Since the version 1.3 of Django, Gstudio uses the
:mod:`django.contrib.staticfiles` application to serve the static files
needed. Please refer to
https://docs.djangoproject.com/en/dev/howto/static-files/ for more
informations about serving static files.

.. _`Python 2.x`: http://www.python.org/
.. _`Django`: https://www.djangoproject.com/
.. _`django-mptt`: https://github.com/django-mptt/django-mptt/
.. _`django-tagging`: https://code.google.com/p/django-tagging/
.. _`BeautifulSoup`: http://www.crummy.com/software/BeautifulSoup/
.. _`pyparsing`: http://pyparsing.wikispaces.com/
.. _`django-xmlrpc`: https://github.com/Fantomas42/django-xmlrpc
