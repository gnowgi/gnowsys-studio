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


"""Test cases for Gstudio's Metatype"""
from django.test import TestCase
from django.contrib.sites.models import Site

from gstudio.models import Nodetype
from gstudio.models import Metatype
from gstudio.managers import PUBLISHED


class MetatypeTestCase(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.metatypes = [Metatype.objects.create(title='Metatype 1',
                                                   slug='metatype-1'),
                           Metatype.objects.create(title='Metatype 2',
                                                   slug='metatype-2')]
        params = {'title': 'My nodetype',
                  'content': 'My content',
                  'tags': 'gstudio, test',
                  'slug': 'my-nodetype'}

        self.nodetype = Nodetype.objects.create(**params)
        self.nodetype.metatypes.add(*self.metatypes)
        self.nodetype.sites.add(self.site)

    def test_nodetypes_published(self):
        metatype = self.metatypes[0]
        self.assertEqual(metatype.nodetypes_published().count(), 0)
        self.nodetype.status = PUBLISHED
        self.nodetype.save()
        self.assertEqual(metatype.nodetypes_published().count(), 1)

        params = {'title': 'My second nodetype',
                  'content': 'My second content',
                  'tags': 'gstudio, test',
                  'status': PUBLISHED,
                  'slug': 'my-second-nodetype'}

        new_nodetype = Nodetype.objects.create(**params)
        new_nodetype.sites.add(self.site)
        new_nodetype.metatypes.add(self.metatypes[0])

        self.assertEqual(self.metatypes[0].nodetypes_published().count(), 2)
        self.assertEqual(self.metatypes[1].nodetypes_published().count(), 1)

    def test_nodetypes_tree_path(self):
        self.assertEqual(self.metatypes[0].tree_path, 'metatype-1')
        self.assertEqual(self.metatypes[1].tree_path, 'metatype-2')
        self.metatypes[1].parent = self.metatypes[0]
        self.metatypes[1].save()
        self.assertEqual(self.metatypes[1].tree_path, 'metatype-1/metatype-2')
