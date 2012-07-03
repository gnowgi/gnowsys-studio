===============
Import / Export
===============

.. highlightlang:: console

As the codebase of gnowsys-studio is based on a blog application, we
inherited some import/export features.  The following features have
not been tested thoroughly.  Each published node is considered in this
documentation as a blog.

If you already have a blog, Gstudio has the ability to import your posts
from other blogging platforms. Useful for rapid migration.  Since
Gstudio is a semantic blogging application, all the data that goes to
your blog may not look like a regular blog,  though importing from a
regular blog should work as any blog site.  We will improve the
documentation as and when we know what to write here.

.. _wordpress2gstudio:

From WordPress to Gstudio
========================

Gstudio provides a command for importing export files from WordPress.

http://codex.wordpress.org/Tools_Export_SubPanel

Once you have the XML file, you simply have to do this. ::

  $ python manage.py wp2gstudio path/to/your/wordpress.xml

This command will associate the post's authors to User and
import the tags, categories, post and comments.

For the options execute this. ::

  $ python manage.py help wp2gstudio

.. _gstudio2wordpress:

From Gstudio to WordPress
========================

Gstudio also provides a command for exporting your blog to WordPress in the
case you want to migrate on it.

Simply execute this command: ::

  $ python manage.py gstudio2wp > export.xml

Once you have the XML export, you can import it into your WordPress site.

http://codex.wordpress.org/Importing_Content

.. _blogger2gstudio:

From Blogger to Gstudio
======================

If you are comming from Blogger, you can import your posts and comments
with this simple command: ::

  $ python manage.py blogger2gstudio

For the options execute this. ::

  $ python manage.py help blogger2gstudio

Note that you need to install the `gdata`_ package to run the importation.

.. _feed2gstudio:

From Feed to Gstudio
===================

If you don't have the possibility to export your posts but have a RSS or Atom
feed on your Weblog, Gstudio can import it. This command is the most generic
way to import content into Gstudio. Simply execute this command: ::

  $ python manage.py feed2gstudio http://url.of/the/feed

For the options execute this. ::

  $ python manage.py help feed2gstudio

Note that you need to install the `feedparser`_ package to run the
importation.


.. _`gdata`: https://code.google.com/p/gdata-python-client/
.. _`feedparser`: https://code.google.com/p/feedparser/
