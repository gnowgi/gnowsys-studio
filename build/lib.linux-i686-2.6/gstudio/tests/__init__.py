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


"""Unit tests for Gstudio"""
from unittest import TestSuite
from unittest import TestLoader
from django.conf import settings

from gstudio.tests.nodetype import NodetypeTestCase  # ~0.2s
from gstudio.tests.nodetype import NodetypeHtmlContentTestCase  # ~0.5s
from gstudio.tests.nodetype import NodetypeGetBaseModelTestCase
from gstudio.tests.signals import SignalsTestCase
from gstudio.tests.metatype import MetatypeTestCase
from gstudio.tests.admin import NodetypeAdminTestCase
from gstudio.tests.admin import MetatypeAdminTestCase
from gstudio.tests.managers import ManagersTestCase  # ~1.2s
from gstudio.tests.feeds import GstudioFeedsTestCase  # ~0.4s
from gstudio.tests.views import GstudioViewsTestCase  # ~1.5s ouch...
from gstudio.tests.views import GstudioCustomDetailViews  # ~0.3s
from gstudio.tests.pingback import PingBackTestCase  # ~0.3s
from gstudio.tests.metaweblog import MetaWeblogTestCase  # ~0.6s
from gstudio.tests.comparison import ComparisonTestCase
from gstudio.tests.quick_nodetype import QuickNodetypeTestCase  # ~0.4s
from gstudio.tests.sitemaps import GstudioSitemapsTestCase  # ~0.3s
from gstudio.tests.ping import DirectoryPingerTestCase
from gstudio.tests.ping import ExternalUrlsPingerTestCase
from gstudio.tests.templatetags import TemplateTagsTestCase  # ~0.4s
from gstudio.tests.moderator import NodetypeCommentModeratorTestCase  # ~0.1s
from gstudio.tests.spam_checker import SpamCheckerTestCase
from gstudio.tests.url_shortener import URLShortenerTestCase
from gstudio.signals import disconnect_gstudio_signals
# TOTAL ~ 6.6s


def suite():
    """Suite of TestCases for Django"""
    suite = TestSuite()
    loader = TestLoader()

    test_cases = (ManagersTestCase, NodetypeTestCase,
                  NodetypeGetBaseModelTestCase, SignalsTestCase,
                  NodetypeHtmlContentTestCase, MetatypeTestCase,
                  GstudioViewsTestCase, GstudioFeedsTestCase,
                  GstudioSitemapsTestCase, ComparisonTestCase,
                  DirectoryPingerTestCase, ExternalUrlsPingerTestCase,
                  TemplateTagsTestCase, QuickNodetypeTestCase,
                  URLShortenerTestCase, NodetypeCommentModeratorTestCase,
                  GstudioCustomDetailViews, SpamCheckerTestCase,
                  NodetypeAdminTestCase, MetatypeAdminTestCase)

    if 'django_xmlrpc' in settings.INSTALLED_APPS:
        test_cases += (PingBackTestCase, MetaWeblogTestCase)

    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite

disconnect_gstudio_signals()
