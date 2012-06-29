"""RelationtypeAdmin for Gstudio"""
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
from markitup.widgets import AdminMarkItUpWidget

from tagging.models import Tag

import reversion
from gstudio import settings
from gstudio.managers import HIDDEN
from gstudio.managers import PUBLISHED
from gstudio.ping import DirectoryPinger
from gstudio.admin.forms import RelationtypeAdminForm
from gstudio.settings import GSTUDIO_VERSIONING


if GSTUDIO_VERSIONING == True:
    parent_class = reversion.VersionAdmin
else:
    parent_class = admin.ModelAdmin 

class RelationtypeAdmin(parent_class):
    """Admin for Relationtype model"""
    form = RelationtypeAdminForm
    date_hierarchy = 'creation_date'
    fieldsets = ((
            (_('Neighbourhood Definiton'), {'fields': (
                        'title',
                        'inverse', 
                        'altnames',
                        'parent',
                        'slug',
                        
                        'left_subjecttype',
                        'left_applicable_nodetypes',
                        'left_cardinality',
                        'right_subjecttype',
                        'right_applicable_nodetypes',
                        'right_cardinality',
                        'is_symmetrical',
                        'is_reflexive',
                        'is_transitive') 
                                            }),
            (_('Content'), {'fields': ('content', 'image',), 
                            'classes': ('collapse', 'collapse-closed')}),
            
            
            (_('Dependency'), {'fields': ('prior_nodes', 'posterior_nodes',), 
                               'classes': ('collapse', 'collapse-closed')}),
            (_('Options'), {'fields': ('featured', 'excerpt', 'template',
                                       'authors',
                                       'creation_date',
                                       'start_publication',
                                       'end_publication'),
                            'classes': ('collapse', 'collapse-closed')}),
            ))
            

    list_filter = ('parent','metatypes', 'authors', 'status', 'featured',
                   'login_required', 'comment_enabled', 'pingback_enabled',
                   'creation_date', 'start_publication',
                   'end_publication', 'sites')
    list_display = ('get_title', 'get_authors', 'get_metatypes',
                    'get_tags', 'get_sites',
                    'get_comments_are_open', 'pingback_enabled',
                    'get_is_actual', 'get_is_visible', 'get_link',
                    'get_short_url', 'creation_date')
    radio_fields = {'template': admin.VERTICAL}
    filter_horizontal = ('metatypes', 'authors')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'excerpt', 'content', 'tags')
    actions = ['make_mine', 'make_published', 'make_hidden',
               'close_comments', 'close_pingbacks',
               'ping_directories', 'make_tweet', 'put_on_top']
    actions_on_top = True
    actions_on_bottom = True
    
    def __init__(self, model, admin_site):
                     self.form.admin_site = admin_site
                     super(RelationtypeAdmin, self).__init__(model, admin_site)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = AdminMarkItUpWidget()
        return super(RelationtypeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
                 
                 # Custom Display
    def get_title(self, relationtype):
        """Return the title with word count and number of comments"""
        title = _('%(title)s (%(word_count)i words)') % \
            {'title': relationtype.title, 'word_count': relationtype.word_count}
        comments = relationtype.comments.count()
        if comments:
            return _('%(title)s (%(comments)i comments)') % \
                {'title': title, 'comments': comments}
        return title
    get_title.short_description = _('title')
    
    def get_authors(self, relationtype):
        """Return the authors in HTML"""
        try:
            authors = ['<a href="%s" target="blank">%s</a>' %
                       (reverse('gstudio_author_detail',
                                args=[author.username]),
                        author.username) for author in relationtype.authors.all()]
        except NoReverseMatch:
            authors = [author.username for author in relationtype.authors.all()]
        return ', '.join(authors)
    get_authors.allow_tags = True
    get_authors.short_description = _('author(s)')
        
    def get_metatypes(self, relationtype):
        """Return the metatypes linked in HTML"""
        try:
            metatypes = ['<a href="%s" target="blank">%s</a>' %
                          (metatype.get_absolute_url(), metatype.title)
                          for metatype in relationtype.metatypes.all()]
        except NoReverseMatch:
            metatypes = [metatype.title for metatype in
                          relationtype.metatypes.all()]
        return ', '.join(metatypes)
    get_metatypes.allow_tags = True
    get_metatypes.short_description = _('metatype(s)')

    def get_tags(self, relationtype):
        """Return the tags linked in HTML"""
        try:
            return ', '.join(['<a href="%s" target="blank">%s</a>' %
                              (reverse('gstudio_tag_detail',
                                       args=[tag.name]), tag.name)
                              for tag in Tag.relations.get_for_relation(relationtype)])
        except NoReverseMatch:
            return relationtype.tags
    get_tags.allow_tags = True
    get_tags.short_description = _('tag(s)')

    def get_sites(self, relationtype):
        """Return the sites linked in HTML"""
        return ', '.join(
            ['<a href="http://%(domain)s" target="blank">%(name)s</a>' %
             site.__dict__ for site in relationtype.sites.all()])
    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')

    def get_comments_are_open(self, relationtype):
        """Admin wrapper for relationtype.comments_are_open"""
        return relationtype.comments_are_open
    get_comments_are_open.boolean = True
    get_comments_are_open.short_description = _('comment enabled')

    def get_is_actual(self, relationtype):
        """Admin wrapper for relationtype.is_actual"""
        return relationtype.is_actual
    get_is_actual.boolean = True
    get_is_actual.short_description = _('is actual')

    def get_is_visible(self, relationtype):
        """Admin wrapper for relationtype.is_visible"""
        return relationtype.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    def get_link(self, relationtype):
        """Return a formated link to the relationtype"""
        return u'<a href="%s" target="blank">%s</a>' % (
            relationtype.get_absolute_url(), _('View'))
    get_link.allow_tags = True
    get_link.short_description = _('View on site')

    def get_short_url(self, relationtype):
        """Return the short url in HTML"""
        short_url = relationtype.short_url
        if not short_url:
            return _('Unavailable')
        return '<a href="%(url)s" target="blank">%(url)s</a>' % \
               {'url': short_url}
    get_short_url.allow_tags = True
    get_short_url.short_description = _('short url')

    # Custom Methods
    def save_model(self, request, relationtype, form, change):
        """Save the authors, update time, make an excerpt"""
        if not form.cleaned_data.get('excerpt') and relationtype.status == PUBLISHED:
            relationtype.excerpt = truncate_words(strip_tags(relationtype.content), 50)

        if relationtype.pk and not request.user.has_perm('gstudio.can_change_author'):
            form.cleaned_data['authors'] = relationtype.authors.all()

        if not form.cleaned_data.get('authors'):
            form.cleaned_data['authors'].append(request.user)

        relationtype.last_update = datetime.now()
        relationtype.save()

    def queryset(self, request):
        """Make special filtering by user permissions"""
        queryset = super(RelationtypeAdmin, self).queryset(request)
        if request.user.has_perm('gstudio.can_view_all'):
            return queryset
        return request.user.relationtypes.all()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filters the disposable authors"""
        if db_field.name == 'authors':
            if request.user.has_perm('gstudio.can_change_author'):
                kwargs['queryset'] = User.objects.filter(is_staff=True)
            else:
                kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

        return super(RelationtypeAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_actions(self, request):
        """Define user actions by permissions"""
        actions = super(RelationtypeAdmin, self).get_actions(request)
        if not request.user.has_perm('gstudio.can_change_author') \
           or not request.user.has_perm('gstudio.can_view_all'):
            del actions['make_mine']
        if not settings.PING_DIRECTORIES:
            del actions['ping_directories']
        if not settings.USE_TWITTER:
            del actions['make_tweet']

        return actions

    # Custom Actions
    def make_mine(self, request, queryset):
        """Set the relationtypes to the user"""
        for relationtype in queryset:
            if request.user not in relationtype.authors.all():
                relationtype.authors.add(request.user)
        self.message_user(
            request, _('The selected relationtypes now belong to you.'))
    make_mine.short_description = _('Set the relationtypes to the user')

    def make_published(self, request, queryset):
        """Set relationtypes selected as published"""
        queryset.update(status=PUBLISHED)
        self.ping_directories(request, queryset, messages=False)
        self.message_user(
            request, _('The selected relationtypes are now marked as published.'))
    make_published.short_description = _('Set relationtypes selected as published')

    def make_hidden(self, request, queryset):
        """Set relationtypes selected as hidden"""
        queryset.update(status=HIDDEN)
        self.message_user(
            request, _('The selected relationtypes are now marked as hidden.'))
    make_hidden.short_description = _('Set relationtypes selected as hidden')

    def make_tweet(self, request, queryset):
        """Post an update on Twitter"""
        import tweepy
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                   settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_KEY,
                              settings.TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        for relationtype in queryset:
            short_url = relationtype.short_url
            message = '%s %s' % (relationtype.title[:139 - len(short_url)], short_url)
            api.update_status(message)
        self.message_user(
            request, _('The selected relationtypes have been tweeted.'))
    make_tweet.short_description = _('Tweet relationtypes selected')

    def close_comments(self, request, queryset):
        """Close the comments for selected relationtypes"""
        queryset.update(comment_enabled=False)
        self.message_user(
            request, _('Comments are now closed for selected relationtypes.'))
    close_comments.short_description = _('Close the comments for '\
                                         'selected relationtypes')

    def close_pingbacks(self, request, queryset):
        """Close the pingbacks for selected relationtypes"""
        queryset.update(pingback_enabled=False)
        self.message_user(
            request, _('Linkbacks are now closed for selected relationtypes.'))
    close_pingbacks.short_description = _(
        'Close the linkbacks for selected relationtypes')

    def put_on_top(self, request, queryset):
        """Put the selected relationtypes on top at the current date"""
        queryset.update(creation_date=datetime.now())
        self.ping_directories(request, queryset, messages=False)
        self.message_user(request, _(
            'The selected relationtypes are now set at the current date.'))
    put_on_top.short_description = _(
        'Put the selected relationtypes on top at the current date')

    def ping_directories(self, request, queryset, messages=True):
        """Ping Directories for selected relationtypes"""
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
                          'pinged %(success)d relationtypes.') %
                        {'directory': directory, 'success': success})
    ping_directories.short_description = _(
        'Ping Directories for selected relationtypes')

    def get_urls(self):
        relationtype_admin_urls = super(RelationtypeAdmin, self).get_urls()
        urls = patterns(
            'django.views.generic.simple',
            url(r'^autocomplete_tags/$', 'direct_to_template',
                {'template': 'admin/gstudio/relationtype/autocomplete_tags.js',
                 'mimetype': 'application/javascript'},
                name='gstudio_relationtype_autocomplete_tags'),
            url(r'^wymeditor/$', 'direct_to_template',
                {'template': 'admin/gstudio/relationtype/wymeditor.js',
                 'mimetype': 'application/javascript'},
                name='gstudio_relationtype_wymeditor'),
            url(r'^markitup/$', 'direct_to_template',
                {'template': 'admin/gstudio/relationtype/markitup.js',
                 'mimetype': 'application/javascript'},
                name='gstudio_relationtype_markitup'),)
        return urls + relationtype_admin_urls

    def _media(self):
        STATIC_URL = '%sgstudio/' % project_settings.STATIC_URL
        media = super(RelationtypeAdmin, self).media + Media(
            css={'all': ('%scss/jquery.autocomplete.css' % STATIC_URL,)},
            js=('%sjs/jquery.js' % STATIC_URL,
                '%sjs/jquery.bgiframe.js' % STATIC_URL,
                '%sjs/jquery.autocomplete.js' % STATIC_URL,
                reverse('admin:gstudio_relationtype_autocomplete_tags'),))

        if settings.WYSIWYG == 'wymeditor':
            media += Media(
                js=('%sjs/wymeditor/jquery.wymeditor.pack.js' % STATIC_URL,
                    '%sjs/wymeditor/plugins/hovertools/'
                    'jquery.wymeditor.hovertools.js' % STATIC_URL,
                    reverse('admin:gstudio_relationtype_wymeditor')))
        elif settings.WYSIWYG == 'tinymce':
            from tinymce.widgets import TinyMCE
            media += TinyMCE().media + Media(
                js=(reverse('tinymce-js', args=('admin/gstudio/relationtype',)),))
        elif settings.WYSIWYG == 'markitup':
            media += Media(
                js=('%sjs/markitup/jquery.markitup.js' % STATIC_URL,
                    '%sjs/markitup/sets/%s/set.js' % (
                        STATIC_URL, settings.MARKUP_LANGUAGE),
                    reverse('admin:gstudio_relationtype_markitup')),
                css={'all': (
                    '%sjs/markitup/skins/django/style.css' % STATIC_URL,
                    '%sjs/markitup/sets/%s/style.css' % (
                        STATIC_URL, settings.MARKUP_LANGUAGE))})
        return media
    media = property(_media)
