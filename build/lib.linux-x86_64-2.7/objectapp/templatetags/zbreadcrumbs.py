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
"""Breadcrumb module for Objectapp templatetags"""
import re
from datetime import datetime

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


class Crumb(object):
    """Part of the Breadcrumbs"""
    def __init__(self, name, url=None):
        self.name = name
        self.url = url


def year_crumb(creation_date):
    """Crumb for a year"""
    year = creation_date.strftime('%Y')
    return Crumb(year, reverse('objectapp_gbobject_archive_year',
                               args=[year]))


def month_crumb(creation_date):
    """Crumb for a month"""
    year = creation_date.strftime('%Y')
    month = creation_date.strftime('%m')
    month_text = creation_date.strftime('%b').capitalize()
    return Crumb(month_text, reverse('objectapp_gbobject_archive_month',
                                     args=[year, month]))


def day_crumb(creation_date):
    """Crumb for a day"""
    year = creation_date.strftime('%Y')
    month = creation_date.strftime('%m')
    day = creation_date.strftime('%d')
    return Crumb(day, reverse('objectapp_gbobject_archive_day',
                              args=[year, month, day]))


OBJECTAPP_ROOT_URL = lambda: reverse('objectapp_gbobject_archive_index')

MODEL_BREADCRUMBS = {'Tag': lambda x: [Crumb(_('Tags'),
                                             reverse('objectapp_tag_list')),
                                       Crumb(x.name)],
                     'Author': lambda x: [Crumb(_('Authors'),
                                              reverse('objectapp_author_list')),
                                        Crumb(x.username)],
                     'Objecttype': lambda x: [Crumb(
                         _('Objecttypes'), reverse('objectapp_Objecttype_list'))] + \
                     [Crumb(anc.title, anc.get_absolute_url())
                      for anc in x.get_ancestors()] + [Crumb(x.title)],
                     'Gbobject': lambda x: [year_crumb(x.creation_date),
                                         month_crumb(x.creation_date),
                                         day_crumb(x.creation_date),
                                         Crumb(x.title)]}

DATE_REGEXP = re.compile(
    r'.*(?P<year>\d{4})/(?P<month>\d{2})?/(?P<day>\d{2})?.*')


def retrieve_breadcrumbs(path, model_instance, root_name=''):
    """Build a semi-hardcoded breadcrumbs
    based of the model's url handled by Objectapp"""
    breadcrumbs = []

    if root_name:
        breadcrumbs.append(Crumb(root_name, OBJECTAPP_ROOT_URL()))

    if model_instance is not None:
        key = model_instance.__class__.__name__
        if key in MODEL_BREADCRUMBS:
            breadcrumbs.extend(MODEL_BREADCRUMBS[key](model_instance))
            return breadcrumbs

    date_match = DATE_REGEXP.match(path)
    if date_match:
        date_dict = date_match.groupdict()
        path_date = datetime(
            int(date_dict['year']),
            date_dict.get('month') is not None and \
            int(date_dict.get('month')) or 1,
            date_dict.get('day') is not None and \
            int(date_dict.get('day')) or 1)

        date_breadcrumbs = [year_crumb(path_date)]
        if date_dict['month']:
            date_breadcrumbs.append(month_crumb(path_date))
        if date_dict['day']:
            date_breadcrumbs.append(day_crumb(path_date))
        breadcrumbs.extend(date_breadcrumbs)

        return breadcrumbs

    url_components = [comp for comp in
                      path.replace(OBJECTAPP_ROOT_URL(), '').split('/') if comp]
    if len(url_components):
        breadcrumbs.append(Crumb(_(url_components[-1].capitalize())))

    return breadcrumbs
