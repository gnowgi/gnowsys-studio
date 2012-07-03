====================
Testing and Coverage
====================


.. module:: gstudio.tests

.. highlightlang:: console

Writing tests is important, maybe more important than coding.

And this for a lot of reasons, but I'm not here to convince you about
the benefits of software testing, some prophets will do it better than me.

* http://en.wikipedia.org/wiki/Software_testing
* https://docs.djangoproject.com/en/dev/topics/testing/

Of course gnowsys-studio has a testing framework. However, we were
impatient and developed several hasty features, without writing
unit-tests. You have been warned.  Please contribute if you have a
zeal to write test cases to match the software requirements and use
cases.

 All the tests belong in the directory :file:`gstudio/tests/` and
 `objectapp/tests`.

.. _lauching-test-suite:

Launching the test suite
========================

If you have :ref:`run the buildout script<running-the-buildout>`
bundled in gnowsys-studio, the tests are run under `nose`_ by
launching this command: ::

  $ ./bin/test

But the tests can also be launched within a Django project with the default
test runner: ::

  $ django-admin.py test gstudio --settings=gstudio.testsettings
  $ django-admin.py test objectapp --settings=gstudio.testsettings

Using the ``./bin/test`` script is usefull when you develop because
the tests are calibrated to run fast, but testing gnowsys-studio
within a Django project even if it's slow, can prevent some
integration issues.

If you want to make some speed optimizations or compare with your
tests results, you can check the actual execution time of the tests at
this URL:

http://django-blog-gstudio.com/documentation/xunit/

.. _coverage:

Coverage
========

We need help here. Any body there?


.. _`unittest`: http://docs.python.org/library/unittest.html
.. _`nose`: http://somethingaboutorange.com/mrl/projects/nose/
