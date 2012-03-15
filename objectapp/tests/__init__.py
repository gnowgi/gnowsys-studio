# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


# This project incorporates work covered by the following copyright and permission notice:  

#    Copyright (c) 2009, Julien Fache
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:

#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of the author nor the names of other
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE.
"""Unit tests for Objectapp"""
from unittest import TestSuite
from unittest import TestLoader
from django.conf import settings

from objectapp.tests.gbobject import GbobjectTestCase  # ~0.2s
from objectapp.tests.gbobject import GbobjectHtmlContentTestCase  # ~0.5s
from objectapp.tests.gbobject import GbobjectGetBaseModelTestCase
from objectapp.tests.signals import SignalsTestCase
from objectapp.tests.Objecttype import ObjecttypeTestCase
from objectapp.tests.admin import GbobjectAdminTestCase
from objectapp.tests.admin import ObjecttypeAdminTestCase
from objectapp.tests.managers import ManagersTestCase  # ~1.2s
from objectapp.tests.feeds import ObjectappFeedsTestCase  # ~0.4s
from objectapp.tests.views import ObjectappViewsTestCase  # ~1.5s ouch...
from objectapp.tests.views import ObjectappCustomDetailViews  # ~0.3s
from objectapp.tests.pingback import PingBackTestCase  # ~0.3s
from objectapp.tests.metaweblog import MetaWeblogTestCase  # ~0.6s
from objectapp.tests.comparison import ComparisonTestCase
from objectapp.tests.quick_gbobject import QuickGbobjectTestCase  # ~0.4s
from objectapp.tests.sitemaps import ObjectappSitemapsTestCase  # ~0.3s
from objectapp.tests.ping import DirectoryPingerTestCase
from objectapp.tests.ping import ExternalUrlsPingerTestCase
from objectapp.tests.templatetags import TemplateTagsTestCase  # ~0.4s
from objectapp.tests.moderator import GbobjectCommentModeratorTestCase  # ~0.1s
from objectapp.tests.spam_checker import SpamCheckerTestCase
from objectapp.tests.url_shortener import URLShortenerTestCase
from objectapp.signals import disconnect_objectapp_signals
# TOTAL ~ 6.6s


def suite():
    """Suite of TestCases for Django"""
    suite = TestSuite()
    loader = TestLoader()

    test_cases = (ManagersTestCase, GbobjectTestCase,
                  GbobjectGetBaseModelTestCase, SignalsTestCase,
                  GbobjectHtmlContentTestCase, ObjecttypeTestCase,
                  ObjectappViewsTestCase, ObjectappFeedsTestCase,
                  ObjectappSitemapsTestCase, ComparisonTestCase,
                  DirectoryPingerTestCase, ExternalUrlsPingerTestCase,
                  TemplateTagsTestCase, QuickGbobjectTestCase,
                  URLShortenerTestCase, GbobjectCommentModeratorTestCase,
                  ObjectappCustomDetailViews, SpamCheckerTestCase,
                  GbobjectAdminTestCase, ObjecttypeAdminTestCase)

    if 'django_xmlrpc' in settings.INSTALLED_APPS:
        test_cases += (PingBackTestCase, MetaWeblogTestCase)

    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite

disconnect_objectapp_signals()
