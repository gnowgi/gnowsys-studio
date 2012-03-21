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


"""Test cases for Objectapp's Objecttype"""
from django.test import TestCase
from django.contrib.sites.models import Site

from objectapp.models import Gbobject
from objectapp.models import Objecttype
from objectapp.managers import PUBLISHED


class ObjecttypeTestCase(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.objecttypes = [Objecttype.objects.create(title='Objecttype 1',
                                                   slug='Objecttype-1'),
                           Objecttype.objects.create(title='Objecttype 2',
                                                   slug='Objecttype-2')]
        params = {'title': 'My gbobject',
                  'content': 'My content',
                  'tags': 'objectapp, test',
                  'slug': 'my-gbobject'}

        self.gbobject = Gbobject.objects.create(**params)
        self.gbobject.objecttypes.add(*self.objecttypes)
        self.gbobject.sites.add(self.site)

    def test_gbobjects_published(self):
        Objecttype = self.objecttypes[0]
        self.assertEqual(Objecttype.gbobjects_published().count(), 0)
        self.gbobject.status = PUBLISHED
        self.gbobject.save()
        self.assertEqual(Objecttype.gbobjects_published().count(), 1)

        params = {'title': 'My second gbobject',
                  'content': 'My second content',
                  'tags': 'objectapp, test',
                  'status': PUBLISHED,
                  'slug': 'my-second-gbobject'}

        new_gbobject = Gbobject.objects.create(**params)
        new_gbobject.sites.add(self.site)
        new_gbobject.objecttypes.add(self.objecttypes[0])

        self.assertEqual(self.objecttypes[0].gbobjects_published().count(), 2)
        self.assertEqual(self.objecttypes[1].gbobjects_published().count(), 1)

    def test_gbobjects_tree_path(self):
        self.assertEqual(self.objecttypes[0].tree_path, 'Objecttype-1')
        self.assertEqual(self.objecttypes[1].tree_path, 'Objecttype-2')
        self.objecttypes[1].parent = self.objecttypes[0]
        self.objecttypes[1].save()
        self.assertEqual(self.objecttypes[1].tree_path, 'Objecttype-1/Objecttype-2')
