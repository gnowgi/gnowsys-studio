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


"""Widgets for Objectapp admin"""
from itertools import chain

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.html import escape
from django.utils.html import conditional_escape
from django.utils.encoding import smart_unicode
from django.utils.encoding import force_unicode


class TreeNodeChoiceField(forms.ModelChoiceField):
    """Duplicating the TreeNodeChoiceField bundled in django-mptt
    to avoid conflict with the TreeNodeChoiceField bundled in django-cms..."""
    def __init__(self, level_indicator=u'|--', *args, **kwargs):
        self.level_indicator = level_indicator
        if kwargs.get('required', True) and not 'empty_label' in kwargs:
            kwargs['empty_label'] = None
        super(TreeNodeChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """Creates labels which represent the tree level of each node
        when generating option labels."""
        return u'%s %s' % (self.level_indicator * getattr(
            obj, obj._mptt_meta.level_attr), smart_unicode(obj))


class MPTTModelChoiceIterator(forms.models.ModelChoiceIterator):
    """MPTT version of ModelChoiceIterator"""
    def choice(self, obj):
        """Overriding choice method"""
        tree_id = getattr(obj, self.queryset.model._mptt_meta.tree_id_attr, 0)
        left = getattr(obj, self.queryset.model._mptt_meta.left_attr, 0)
        return super(MPTTModelChoiceIterator,
                     self).choice(obj) + ((tree_id, left),)


class MPTTModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """MPTT version of ModelMultipleChoiceField"""
    def __init__(self, level_indicator=u'|--', *args, **kwargs):
        self.level_indicator = level_indicator
        super(MPTTModelMultipleChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """Creates labels which represent the tree level of each node
        when generating option labels."""
        return u'%s %s' % (self.level_indicator * getattr(
            obj, obj._mptt_meta.level_attr), smart_unicode(obj))

    def _get_choices(self):
        """Overriding _get_choices"""
        if hasattr(self, '_choices'):
            return self._choices
        return MPTTModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class MPTTFilteredSelectMultiple(widgets.FilteredSelectMultiple):
    """MPTT version of FilteredSelectMultiple"""
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        super(MPTTFilteredSelectMultiple, self).__init__(
            verbose_name, is_stacked, attrs, choices)

    def render_options(self, choices, selected_choices):
        """
        This is copy'n'pasted from django.forms.widgets Select(Widget)
        change to the for loop and render_option so they will unpack
        and use our extra tuple of mptt sort fields (if you pass in
        some default choices for this field, make sure they have the
        extra tuple too!)
        """
        def render_option(option_value, option_label, sort_fields):
            """Inner scope render_option"""
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) \
                            and u' selected="selected"' or ''
            return u'<option value="%s" data-tree-id="%s" ' \
                   'data-left-value="%s"%s>%s</option>' % (
                escape(option_value),
                sort_fields[0],
                sort_fields[1],
                selected_html,
                conditional_escape(force_unicode(option_label)),
                )
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, sort_fields in chain(
            self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(
                    force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label,
                                            sort_fields))
        return u'\n'.join(output)

    class Media:
        """MPTTFilteredSelectMultiple's Media"""
        js = (settings.ADMIN_MEDIA_PREFIX + 'js/core.js',
              settings.STATIC_URL + 'objectapp/js/mptt_m2m_selectbox.js',
              settings.ADMIN_MEDIA_PREFIX + 'js/SelectFilter2.js',)
