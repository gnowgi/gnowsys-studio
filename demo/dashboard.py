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


"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'demo.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for atlas.gnowledge.org
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=False,
            children = [
                modules.AppList(
                        _('Gstudio (Basic)'),
                        column=1,
                        collapsible=False,
                        models=(
                                'objectapp.models.Gbobject',
				'objectapp.models.System',
                            	'gstudio.models.Relation',
                            	'gstudio.models.Attribute',
                                

                            ),
                        ),

                modules.AppList(


                        #Gstudio models here ( other than attribute datatype and collapsible ones)
                        _('Gstudio (Advanced)'),
                        column=1,
                        collapsible=True,
                        models=(
			    'gstudio.models.Objecttype',	
                            'gstudio.models.Attributetype',
                            'gstudio.models.Relationtype',
                            'gstudio.models.Metatype',
                            'gstudio.models.Systemtype',
                            'gstudio.models.Processtype',
                            'gstudio.models.AttributeSpecification',
                            'gstudio.models.RelationSpecification',
                            'gstudio.models.NodeSpecification',
                            'gstudio.models.Union',
                            'gstudio.models.Complement',
                            'gstudio.models.Intersection',
                            'gstudio.models.Expression',
                            'gstudio.models.Peer',
                            ),

                        ),
                #Object App models here
                modules.AppList(
                        _('Object App (Advanced)'),
                        column=1,
                        collapsible=True,
                        models=(
                            'objectapp.models.Process',
                           
                            ),
                        ),







                # Gstudio Attribute datatype models here

                modules.AppList(
                        _('Attribute Manager'),
                        column=1,
                        collapsible=True,
                        models=(
                            'gstudio.models.AttributeCharField',
                            'gstudio.models.AttributeTextField',
                            'gstudio.models.AttributeIntegerField',
                            'gstudio.models.AttributeCommaSeparatedIntegerField',
                            'gstudio.models.AttributeBigIntegerField',
                            'gstudio.models.AttributePositiveIntegerField',
                            'gstudio.models.AttributeDecimalField',
                            'gstudio.models.AttributeFloatField',
                            'gstudio.models.AttributeBooleanField',
                            'gstudio.models.AttributeNullBooleanField',
                            'gstudio.models.AttributeDateField',
                            'gstudio.models.AttributeDateTimeField',
                            'gstudio.models.AttributeTimeField',
                            'gstudio.models.AttributeEmailField',
                            'gstudio.models.AttributeFileField',
                            'gstudio.models.AttributeFilePathField',
                            'gstudio.models.AttributeImageField',
                            'gstudio.models.AttributeURLField',

                            ),
                        ),


                modules.AppList(
                    _('Other Applications'),
                    column=1,
#                    css_classes=('collapse closed',),
                    exclude=('django.contrib.*','gstudio.models.*','objectapp.models.*'),),
                modules.AppList(
                        _('Administration'),
                        column=1,
                        collapsible=False,
                        models=('django.contrib.*',),
                        ),




                
                        ]
                ))
        


        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('AppList: Applications'),
            collapsible=False,
            column=2,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))

        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('ModelList: Administration'),
            column=2,
            collapsible=False,
            models=('django.contrib.*',),
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]

        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


