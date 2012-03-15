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




"""Calendar module for Gstudio templatetags"""
from datetime import date
from calendar import HTMLCalendar

from django.utils.dates import MONTHS
from django.utils.dates import WEEKDAYS_ABBR
from django.utils.formats import get_format
from django.core.urlresolvers import reverse

from gstudio.models import Nodetype

AMERICAN_TO_EUROPEAN_WEEK_DAYS = [6, 0, 1, 2, 3, 4, 5]


class GstudioCalendar(HTMLCalendar):
    """Override of HTMLCalendar"""

    def __init__(self):
        """Retrieve and convert the localized first week day
        at initialization"""
        HTMLCalendar.__init__(self, AMERICAN_TO_EUROPEAN_WEEK_DAYS[
            get_format('FIRST_DAY_OF_WEEK')])

    def formatday(self, day, weekday):
        """Return a day as a table cell with a link
        if nodetypes are published this day"""
        if day and day in self.day_nodetypes:
            day_date = date(self.current_year, self.current_month, day)
            archive_day_url = reverse('gstudio_nodetype_archive_day',
                                      args=[day_date.strftime('%Y'),
                                            day_date.strftime('%m'),
                                            day_date.strftime('%d')])
            return '<td class="%s nodetype"><a href="%s" '\
                   'rel="archives">%d</a></td>' % (
                self.cssclasses[weekday], archive_day_url, day)

        return super(GstudioCalendar, self).formatday(day, weekday)

    def formatmonth(self, theyear, themonth, withyear=True):
        """Return a formatted month as a table with
        new attributes computed for formatting a day"""
        self.current_year = theyear
        self.current_month = themonth
        self.day_nodetypes = [nodetypes.creation_date.day for nodetypes in
                            Nodetype.published.filter(
                                creation_date__year=theyear,
                                creation_date__month=themonth)]

        return super(GstudioCalendar, self).formatmonth(
            theyear, themonth, withyear)

    def formatweekday(self, day):
        """Return a weekday name translated
        as a table header."""
        return '<th class="%s">%s</th>' % (self.cssclasses[day],
                                           WEEKDAYS_ABBR[day].title())

    def formatmonthname(self, theyear, themonth, withyear=True):
        """Return a month name translated
        as a table row."""
        monthname = '%s %s' % (MONTHS[themonth].title(), theyear)
        return '<tr><th colspan="7" class="month">%s</th></tr>' % monthname
