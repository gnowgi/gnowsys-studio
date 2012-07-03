
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


"""GbobjectAdmin for Objectapp"""
from datetime import datetime

from django.forms import Media
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
from django.conf import settings as project_settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, NoReverseMatch
import reversion
from tagging.models import Tag
from markitup.widgets import AdminMarkItUpWidget
from objectapp import settings
from objectapp.managers import HIDDEN
from objectapp.managers import PUBLISHED
from objectapp.ping import DirectoryPinger
from objectapp.admin.forms import GbobjectAdminForm


class GbobjectAdmin(reversion.VersionAdmin):
    """Admin for Gbobject model"""
    form = GbobjectAdminForm
    date_hierarchy = 'creation_date'
    fieldsets = ((_('Content'), {'fields': ('title', 'altnames', 'objecttypes','content',
                                            'image', 'status')}),
                 (_('Dependency'), {'fields': ('prior_nodes', 'posterior_nodes',),
                                 'classes': ('collapse', 'collapse-closed')}),

                 (_('Options'), {'fields': ('featured', 'excerpt', 'template',
                                             'authors',
                                             'rurl',
                                            'creation_date',
                                            'start_publication',
                                            'end_publication'),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Privacy'), {'fields': ('password', 'login_required',),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Discussion'), {'fields': ('comment_enabled',
                                               'pingback_enabled')}),
                 (_('Publication'), {'fields': ( 'tags',
                                                'sites', 'slug')}))
    list_filter = ('objecttypes', 'authors', 'status', 'featured',
                   'login_required', 'comment_enabled', 'pingback_enabled',
                   'creation_date', 'start_publication',
                   'end_publication', 'sites')
    list_display = ('get_title', 'get_authors', 'get_objecttypes',
                    'get_tags', 'get_sites',
                    'get_comments_are_open', 'pingback_enabled',
                    'get_is_actual', 'get_is_visible', 'get_link',
                    'get_short_url', 'creation_date')
    radio_fields = {'template': admin.VERTICAL}
    filter_horizontal = ('objecttypes', 'authors')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'excerpt', 'content', 'tags')
    actions = ['make_mine', 'make_published', 'make_hidden',
               'close_comments', 'close_pingbacks',
               'ping_directories', 'make_tweet', 'put_on_top']
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(GbobjectAdmin, self).__init__(model, admin_site)

    # Custom Display
    def get_title(self, gbobject):
        """Return the title with word count and number of comments"""
        title = _('%(title)s (%(word_count)i words)') % \
                {'title': gbobject.title, 'word_count': gbobject.word_count}
        comments = gbobject.comments.count()
        if comments:
            return _('%(title)s (%(comments)i comments)') % \
                   {'title': title, 'comments': comments}
        return title
    get_title.short_description = _('title')

    def get_authors(self, gbobject):
        """Return the authors in HTML"""
        try:
            authors = ['<a href="%s" target="blank">%s</a>' %
                       (reverse('objectapp_author_detail',
                                args=[author.username]),
                        author.username) for author in gbobject.authors.all()]
        except NoReverseMatch:
            authors = [author.username for author in gbobject.authors.all()]
        return ', '.join(authors)
    get_authors.allow_tags = True
    get_authors.short_description = _('author(s)')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = AdminMarkItUpWidget()
        return super(GbobjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def get_objecttypes(self, gbobject):
        """Return the objecttypes linked in HTML"""
        try:
            objecttypes = ['<a href="%s" target="blank">%s</a>' %
                          (Objecttype.get_absolute_url(), Objecttype.title)
                          for Objecttype in gbobject.objecttypes.all()]
        except NoReverseMatch:
            objecttypes = [Objecttype.title for Objecttype in
                          gbobject.objecttypes.all()]
        return ', '.join(objecttypes)
    get_objecttypes.allow_tags = True
    get_objecttypes.short_description = _('Objecttype(s)')

    def get_tags(self, gbobject):
        """Return the tags linked in HTML"""
        try:
            return ', '.join(['<a href="%s" target="blank">%s</a>' %
                              (reverse('objectapp_tag_detail',
                                       args=[tag.name]), tag.name)
                              for tag in Tag.objects.get_for_object(gbobject)])
        except NoReverseMatch:
            return gbobject.tags
    get_tags.allow_tags = True
    get_tags.short_description = _('tag(s)')

    def get_sites(self, gbobject):
        """Return the sites linked in HTML"""
        return ', '.join(
            ['<a href="http://%(domain)s" target="blank">%(name)s</a>' %
             site.__dict__ for site in gbobject.sites.all()])
    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')

    def get_comments_are_open(self, gbobject):
        """Admin wrapper for gbobject.comments_are_open"""
        return gbobject.comments_are_open
    get_comments_are_open.boolean = True
    get_comments_are_open.short_description = _('comment enabled')

    def get_is_actual(self, gbobject):
        """Admin wrapper for gbobject.is_actual"""
        return gbobject.is_actual
    get_is_actual.boolean = True
    get_is_actual.short_description = _('is actual')

    def get_is_visible(self, gbobject):
        """Admin wrapper for gbobject.is_visible"""
        return gbobject.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    def get_link(self, gbobject):
        """Return a formated link to the gbobject"""
        return u'<a href="%s" target="blank">%s</a>' % (
            gbobject.get_absolute_url(), _('View'))
    get_link.allow_tags = True
    get_link.short_description = _('View on site')

    def get_short_url(self, gbobject):
        """Return the short url in HTML"""
        short_url = gbobject.short_url
        if not short_url:
            return _('Unavailable')
        return '<a href="%(url)s" target="blank">%(url)s</a>' % \
               {'url': short_url}
    get_short_url.allow_tags = True
    get_short_url.short_description = _('short url')

    # Custom Methods
    def save_model(self, request, gbobject, form, change):
        """Save the authors, update time, make an excerpt"""
        if not form.cleaned_data.get('excerpt') and gbobject.status == PUBLISHED:
            gbobject.excerpt = truncate_words(strip_tags(gbobject.content), 50)

        if gbobject.pk and not request.user.has_perm('objectapp.can_change_author'):
            form.cleaned_data['authors'] = gbobject.authors.all()

        if not form.cleaned_data.get('authors'):
            form.cleaned_data['authors'].append(request.user)

        gbobject.last_update = datetime.now()
        gbobject.save()

    def queryset(self, request):
        """Make special filtering by user permissions"""
        queryset = super(GbobjectAdmin, self).queryset(request)
        if request.user.has_perm('objectapp.can_view_all'):
            return queryset
        return request.user.gbobjects.all()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filters the disposable authors"""
        if db_field.name == 'authors':
            if request.user.has_perm('objectapp.can_change_author'):
                kwargs['queryset'] = User.objects.filter(is_staff=True)
            else:
                kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

        return super(GbobjectAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_actions(self, request):
        """Define user actions by permissions"""
        actions = super(GbobjectAdmin, self).get_actions(request)
        if not request.user.has_perm('objectapp.can_change_author') \
           or not request.user.has_perm('objectapp.can_view_all'):
            del actions['make_mine']
        if not settings.PING_DIRECTORIES:
            del actions['ping_directories']
        if not settings.USE_TWITTER:
            del actions['make_tweet']

        return actions

    # Custom Actions
    def make_mine(self, request, queryset):
        """Set the gbobjects to the user"""
        for gbobject in queryset:
            if request.user not in gbobject.authors.all():
                gbobject.authors.add(request.user)
        self.message_user(
            request, _('The selected gbobjects now belong to you.'))
    make_mine.short_description = _('Set the gbobjects to the user')

    def make_published(self, request, queryset):
        """Set gbobjects selected as published"""
        queryset.update(status=PUBLISHED)
        self.ping_directories(request, queryset, messages=False)
        self.message_user(
            request, _('The selected gbobjects are now marked as published.'))
    make_published.short_description = _('Set gbobjects selected as published')

    def make_hidden(self, request, queryset):
        """Set gbobjects selected as hidden"""
        queryset.update(status=HIDDEN)
        self.message_user(
            request, _('The selected gbobjects are now marked as hidden.'))
    make_hidden.short_description = _('Set gbobjects selected as hidden')

    def make_tweet(self, request, queryset):
        """Post an update on Twitter"""
        import tweepy
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                   settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_KEY,
                              settings.TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        for gbobject in queryset:
            short_url = gbobject.short_url
            message = '%s %s' % (gbobject.title[:139 - len(short_url)], short_url)
            api.update_status(message)
        self.message_user(
            request, _('The selected gbobjects have been tweeted.'))
    make_tweet.short_description = _('Tweet gbobjects selected')

    def close_comments(self, request, queryset):
        """Close the comments for selected gbobjects"""
        queryset.update(comment_enabled=False)
        self.message_user(
            request, _('Comments are now closed for selected gbobjects.'))
    close_comments.short_description = _('Close the comments for '\
                                         'selected gbobjects')

    def close_pingbacks(self, request, queryset):
        """Close the pingbacks for selected gbobjects"""
        queryset.update(pingback_enabled=False)
        self.message_user(
            request, _('Linkbacks are now closed for selected gbobjects.'))
    close_pingbacks.short_description = _(
        'Close the linkbacks for selected gbobjects')

    def put_on_top(self, request, queryset):
        """Put the selected gbobjects on top at the current date"""
        queryset.update(creation_date=datetime.now())
        self.ping_directories(request, queryset, messages=False)
        self.message_user(request, _(
            'The selected gbobjects are now set at the current date.'))
    put_on_top.short_description = _(
        'Put the selected gbobjects on top at the current date')

    def ping_directories(self, request, queryset, messages=True):
        """Ping Directories for selected gbobjects"""
        for directory in settings.PING_DIRECTORIES:
            pinger = DirectoryPinger(directory, queryset)
            pinger.join()
            if messages:
                success = 0
                for result in pinger.results:
                    if not result.get('flerror', True):
                        success += 1
                    else:
                        self.message_user(request,
                                          '%s : %s' % (directory,
                                                       result['message']))
                if success:
                    self.message_user(
                        request,
                        _('%(directory)s directory succesfully ' \
                          'pinged %(success)d gbobjects.') %
                        {'directory': directory, 'success': success})
    ping_directories.short_description = _(
        'Ping Directories for selected gbobjects')

    def get_urls(self):
        gbobject_admin_urls = super(GbobjectAdmin, self).get_urls()
        urls = patterns(
            'django.views.generic.simple',
            url(r'^autocomplete_tags/$', 'direct_to_template',
                {'template': 'admin/objectapp/gbobject/autocomplete_tags.js',
                 'mimetype': 'application/javascript'},
                name='objectapp_gbobject_autocomplete_tags'),
            url(r'^wymeditor/$', 'direct_to_template',
                {'template': 'admin/objectapp/gbobject/wymeditor.js',
                 'mimetype': 'application/javascript'},
                name='objectapp_gbobject_wymeditor'),
            url(r'^markitup/$', 'direct_to_template',
                {'template': 'admin/objectapp/gbobject/markitup.js',
                 'mimetype': 'application/javascript'},
                name='objectapp_gbobject_markitup'),)
        return urls + gbobject_admin_urls

    def _media(self):
        STATIC_URL = '%sobjectapp/' % project_settings.STATIC_URL
        media = super(GbobjectAdmin, self).media + Media(
            css={'all': ('%scss/jquery.autocomplete.css' % STATIC_URL,)},
            js=('%sjs/jquery.js' % STATIC_URL,
                '%sjs/jquery.bgiframe.js' % STATIC_URL,
                '%sjs/jquery.autocomplete.js' % STATIC_URL,
                reverse('admin:objectapp_gbobject_autocomplete_tags'),))

        if settings.WYSIWYG == 'wymeditor':
            media += Media(
                js=('%sjs/wymeditor/jquery.wymeditor.pack.js' % STATIC_URL,
                    '%sjs/wymeditor/plugins/hovertools/'
                    'jquery.wymeditor.hovertools.js' % STATIC_URL,
                    reverse('admin:objectapp_gbobject_wymeditor')))
        elif settings.WYSIWYG == 'tinymce':
            from tinymce.widgets import TinyMCE
            media += TinyMCE().media + Media(
                js=(reverse('tinymce-js', args=('admin/objectapp/gbobject',)),))
        elif settings.WYSIWYG == 'markitup':
            media += Media(
                js=('%sjs/markitup/jquery.markitup.js' % STATIC_URL,
                    '%sjs/markitup/sets/%s/set.js' % (
                        STATIC_URL, settings.MARKUP_LANGUAGE),
                    reverse('admin:objectapp_gbobject_markitup')),
                css={'all': (
                    '%sjs/markitup/skins/django/style.css' % STATIC_URL,
                    '%sjs/markitup/sets/%s/style.css' % (
                        STATIC_URL, settings.MARKUP_LANGUAGE))})
        return media
    media = property(_media)
