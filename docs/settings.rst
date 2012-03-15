================
List of settings
================

.. module:: gstudio.settings

Gstudio has a lot of parameters to configure the application accordingly to
your needs. Knowing this list of settings can save you a lot of time.

Here's a full list of all available settings, and their default values.

All settings described here can be found in :file:`gstudio/settings.py`.

.. contents::
    :local:
    :depth: 1

.. _settings-entry:

Entry
=====

.. setting:: GSTUDIO_ENTRY_TEMPLATES

GSTUDIO_ENTRY_TEMPLATES
----------------------
**Default value:** ``()`` (Empty tuple)

List of tuple for extending the list of templates availables for
rendering the entry. By using this setting, you can change the look and
feel of an entry directly in the admin interface. Example: ::

  GSTUDIO_ENTRY_TEMPLATES = (('gstudio/entry_detail_alternate.html',
                             gettext('Alternative template')),)

.. setting:: GSTUDIO_ENTRY_BASE_MODEL

GSTUDIO_ENTRY_BASE_MODEL
-----------------------
**Default value:** ``''`` (Empty string)

String defining the base model path for the Entry model. See
:doc:`extending_entry_model` for more informations.

.. setting:: GSTUDIO_UPLOAD_TO

GSTUDIO_UPLOAD_TO
----------------
**Default value:** ``'uploads'``

String setting that tells Gstudio where to upload entries' images.

.. _settings-edition:

Edition
=======

.. setting:: GSTUDIO_MARKUP_LANGUAGE

GSTUDIO_MARKUP_LANGUAGE
----------------------
**Default value:** ``'html'``

String determining the markup language used for writing the entries.
You can use one of these values: ::

    ['html', 'markdown', 'restructuredtext', 'textile']

The value of this variable will alter the value of :setting:`GSTUDIO_WYSIWYG`
if you don't set it.

.. setting:: GSTUDIO_MARKDOWN_EXTENSIONS

GSTUDIO_MARKDOWN_EXTENSIONS
--------------------------
**Default value:** ``''`` (Empty string)

Extensions names to be used for rendering the entries in MarkDown. Example:
::

  GSTUDIO_MARKDOWN_EXTENSIONS = 'extension1_name,extension2_name...'

.. setting:: GSTUDIO_WYSIWYG

GSTUDIO_WYSIWYG
--------------
**Default value:** ::

    WYSIWYG_MARKUP_MAPPING = {
        'textile': 'markitup',
        'markdown': 'markitup',
        'restructuredtext': 'markitup',
        'html': 'tinymce' in settings.INSTALLED_APPS and \
                    'tinymce' or 'wymeditor'}

    WYSIWYG = getattr(settings, 'GSTUDIO_WYSIWYG',
                      WYSIWYG_MARKUP_MAPPING.get(GSTUDIO_MARKUP_LANGUAGE))

Determining the WYSIWYG editor used for editing an entry.
So if MarkDown, Textile or reStructuredText are used, the value will be
``'markitup'``, but if you use HTML, TinyMCE will be used if
:ref:`django-tinymce is installed<gstudio-tinymce>`, else WYMEditor will be
used.

This setting can also be used for disabling the WYSIWYG
functionnality. Example: ::

  GSTUDIO_WYSIWYG = None

.. _settings-views:

Views
=====

.. setting:: GSTUDIO_PAGINATION

GSTUDIO_PAGINATION
-----------------

**Default value:** ``10``

Integer used to paginate the entries. So by default you will have 10
entries displayed per page on the Weblog.

.. setting:: GSTUDIO_ALLOW_EMPTY

GSTUDIO_ALLOW_EMPTY
------------------
**Default value:** ``True``

Used for archives views, raise a 404 error if no entries are present at
a specified date.

.. setting:: GSTUDIO_ALLOW_FUTURE

GSTUDIO_ALLOW_FUTURE
-------------------
**Default value:** ``True``

Used for allowing archives views in the future.

.. _settings-feeds:

Feeds
=====

.. setting:: GSTUDIO_FEEDS_FORMAT

GSTUDIO_FEEDS_FORMAT
-------------------
**Default value:** ``'rss'``

String determining the format of the syndication feeds. You can use
``'atom'`` if your prefer Atom feeds.

.. setting:: GSTUDIO_FEEDS_MAX_ITEMS

GSTUDIO_FEEDS_MAX_ITEMS
----------------------
**Default value:** ``15``

Integer used to define the maximum items provided in the syndication feeds.
So by default you will have 15 entries displayed on the feeds.

.. _settings-urls:

URLs
====

.. setting:: GSTUDIO_URL_SHORTENER_BACKEND

GSTUDIO_URL_SHORTENER_BACKEND
----------------------------
**Default value:** ``'gstudio.url_shortener.backends.default'``

String representing the module path to the URL shortener backend.

.. setting:: GSTUDIO_PROTOCOL

GSTUDIO_PROTOCOL
---------------
**Default value:** ``'http'``

String representing the protocol of the site. If your Web site uses HTTPS,
set this setting to ``https``.

.. _settings-comments:

Comment moderation
==================

.. setting:: GSTUDIO_AUTO_MODERATE_COMMENTS

GSTUDIO_AUTO_MODERATE_COMMENTS
-----------------------------
**Default value:** ``False``

Determine if a new comment should be allowed to show up
immediately or should be marked non-public and await approval.

.. setting:: GSTUDIO_AUTO_CLOSE_COMMENTS_AFTER

GSTUDIO_AUTO_CLOSE_COMMENTS_AFTER
--------------------------------
**Default value:** ``None``

Determine the number of days where comments are open. If you set this
setting to ``10`` the comments will be closed automaticaly 10 days after
the publication date of your entries.

.. setting:: GSTUDIO_MAIL_COMMENT_REPLY

GSTUDIO_MAIL_COMMENT_REPLY
-------------------------
**Default value:** ``False``

Boolean used for sending an email to comment's authors
when a new comment is posted.

.. setting:: GSTUDIO_MAIL_COMMENT_AUTHORS

GSTUDIO_MAIL_COMMENT_AUTHORS
---------------------------
**Default value:** ``True``

Boolean used for sending an email to entry authors
when a new comment is posted.

.. setting:: GSTUDIO_MAIL_COMMENT_NOTIFICATION_RECIPIENTS

GSTUDIO_MAIL_COMMENT_NOTIFICATION_RECIPIENTS
-------------------------------------------
**Default value:** ::

    [manager_tuple[1] for manager_tuple in settings.MANAGERS]

List of emails used for sending a notification when a
new public comment has been posted.

.. setting:: GSTUDIO_SPAM_CHECKER_BACKENDS

GSTUDIO_SPAM_CHECKER_BACKENDS
----------------------------
**Default value:** ``()`` (Empty tuple)

List of strings representing the module path to a spam checker backend.
See :doc:`spam_checker` for more informations about this setting.

.. _settings-pinging:

Pinging
=======

.. setting:: GSTUDIO_PING_DIRECTORIES

GSTUDIO_PING_DIRECTORIES
-----------------------
**Default value:** ``('http://django-blog-gstudio.com/xmlrpc/',)``

List of the directories you want to ping.

.. setting:: GSTUDIO_PING_EXTERNAL_URLS

GSTUDIO_PING_EXTERNAL_URLS
-------------------------
**Default value:** ``True``

Boolean setting for telling if you want to ping external URLs when saving
an entry.

.. setting:: GSTUDIO_SAVE_PING_DIRECTORIES

GSTUDIO_SAVE_PING_DIRECTORIES
----------------------------
**Default value:** ``bool(GSTUDIO_PING_DIRECTORIES)``

Boolean setting for telling if you want to ping directories when saving
an entry.

.. setting:: GSTUDIO_PINGBACK_CONTENT_LENGTH

GSTUDIO_PINGBACK_CONTENT_LENGTH
------------------------------
**Default value:** ``300``

Size of the excerpt generated on pingback.

.. _settings-similarity:

Similarity
==========

.. setting:: GSTUDIO_F_MIN

GSTUDIO_F_MIN
------------
**Default value:** ``0.1``

Float setting of the minimal word frequency for similar entries.

.. setting:: GSTUDIO_F_MAX

GSTUDIO_F_MAX
------------
**Default value:** ``1.0``

Float setting of the minimal word frequency for similar entries.

.. _settings-misc:

Miscellaneous
=============

.. setting:: GSTUDIO_COPYRIGHT

GSTUDIO_COPYRIGHT
----------------
**Default value:** ``'Gstudio'``

String used for copyrighting your entries, used in the syndication feeds
and in the opensearch document.

.. setting:: GSTUDIO_STOP_WORDS

GSTUDIO_STOP_WORDS
-----------------
**Default value:** See :file:`gstudio/settings.py`

List of common words excluded from the advanced search engine
to optimize the search querying and the results.

.. setting:: GSTUDIO_USE_TWITTER

GSTUDIO_USE_TWITTER
------------------
**Default value:** ``True if python-twitter is in the PYTHONPATH``

Boolean telling if Gstudio can use Twitter.

.. _settings-cms:

CMS
===

All the settings related to the CMS can be found in :file:`gstudio/plugins/settings.py`.

.. setting:: GSTUDIO_APP_MENUS

GSTUDIO_APP_MENUS
----------------
**Default value:** ::

  ('gstudio.plugins.menu.EntryMenu',
   'gstudio.plugins.menu.CategoryMenu',
   'gstudio.plugins.menu.TagMenu',
   'gstudio.plugins.menu.AuthorMenu')

List of strings representing the path to the Menu class provided for the
Gstudio AppHook.

.. setting:: GSTUDIO_HIDE_ENTRY_MENU

GSTUDIO_HIDE_ENTRY_MENU
----------------------
**Default value:** ``True``

Boolean used for displaying or not the entries in the EntryMenu object.

.. setting:: GSTUDIO_PLUGINS_TEMPLATES

GSTUDIO_PLUGINS_TEMPLATES
------------------------
**Default value:** ``()`` (Empty tuple)

List of tuple for extending the CMS's plugins rendering templates.
