============
Installation
============

.. module:: gnowsys-studio

.. _dependencies:

Dependencies
============

Make sure to install these packages prior to installation :

* `Python 2.x`_ >= 2.5
* `Django`_ >= 1.3
* `django-mptt`_ >= 0.4.2
* `django-tagging`_ >= 0.3.1
* `BeautifulSoup`_ >= 3.2.0
* `django-xmlrpc`_ >= 0.1.3
* `pyparsing`_ >= 1.5.5
* `django-reversion`_ >= 1.5.1
* `django-grappelli`_ >= 2.3.4
* `django-ratings`_ >= 0.3.6
* `rdflib`_ >= 3.0.0
* `django-registration`_ >=0.8
* `django-4store`_ >= 0.3
* `HTTP4Store`_ >= 0.2
* `html5lib`_ >=  0.95
* `PIL`_ >= 1.1.7
* `diff-match-patch`_ >= 20120106


Note that all the dependencies will be resolved if you install
gnowsys-studio with :program:`pip` or :program:`easy_install`,
excepting Django.

.. _getting-the-code:

Getting the code
================

.. highlight:: console

For the latest version of Gstudio use :program:`easy_install`: ::

  $ easy_install gnowsys-studio

or use :program:`pip`: ::

  $ pip install gnowsys-studio

You could also retrieve the last sources from
https://github.com/gnowgi/django-gstudio. Clone the repository
using :program:`git` and run the installation script: ::

  $ git clone git://github.com/gnowgi/gnowsys-studio.git
  $ cd gnowsys-studio
  $ python setup.py install

or more easily via :program:`pip`: ::

  $ pip install -e git://github.com/gnowgi/gnowsys-studio.git#egg=gnowsys-studio

.. _applications:

Applications
============

.. highlight:: python

Then register :mod:`gstudio`, `objectapp`, and these following
applications in the :setting:`INSTALLED_APPS` section of your
project's settings. ::

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'mptt',
    'reversion',
    'tagging',
    'django_xmlrpc',
    'grappelli.dashboard',
    'grappelli',
    'gstudio',
    'objectapp',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'djangoratings',
    'registration',
    'graphviz',
    'demo',
    'fourstore',
    'HTTP4Store',
    'html5lib',
    # Uncomment the south entry to activate south for database migrations
    # Please do install south before uncommenting
    # command: sudo pip install south 
    # 'south',
    )

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
site.

Note that the default gnowsys-studio URLset is provided for convenient
usage, but you can customize your URLs if you want. Here's how: ::

urlpatterns = patterns(
    '',
    (r'^$', 'django.views.generic.simple.redirect_to',
     {'url': '/home/'}),
    url(r'^home/', home_view),
    url(r'^more/',more_view),
    url(r'^nodetypes/', include('gstudio.urls')),
    url(r'^objects/', include('objectapp.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    #URL for XMLRPC
    url(r'^xmlrpc/$','django_xmlrpc.views.handle_xmlrpc'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/gstudio/', include('gstudio.urls.ajaxurls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^objects/admin/', include(admin.site.urls)),
    url(r'^nodetypes/admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/register/$', register, {'backend': 'gstudio.regbackend.MyBackend','form_class': UserRegistrationForm}, name='registration_register'),

    url(r'^accounts/', include('registration.urls')),

    url(r'^$', 'django.views.generic.simple.redirect_to',
            { 'template': 'index.html' }, 'index'),
    )

.. _static-files:

Static Files
============

Since the version 1.3 of Django, gnowsys-studio uses the
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
