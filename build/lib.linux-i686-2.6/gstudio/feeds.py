
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


"""Feeds for Gstudio"""
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist

from tagging.models import Tag
from tagging.models import TaggedItem

from gstudio.models import Nodetype
from gstudio.settings import COPYRIGHT
from gstudio.settings import PROTOCOL
from gstudio.settings import FEEDS_FORMAT
from gstudio.settings import FEEDS_MAX_ITEMS
from gstudio.managers import nodetypes_published
from gstudio.views.metatypes import get_metatype_or_404
from gstudio.templatetags.gstudio_tags import get_gravatar


class GstudioFeed(Feed):
    """Base Feed for Gstudio"""
    feed_copyright = COPYRIGHT

    def __init__(self):
        self.site = Site.objects.get_current()
        self.site_url = '%s://%s' % (PROTOCOL, self.site.domain)
        if FEEDS_FORMAT == 'atom':
            self.feed_type = Atom1Feed
            self.subtitle = self.description


class NodetypeFeed(GstudioFeed):
    """Base Nodetype Feed"""
    title_template = 'feeds/nodetype_title.html'
    description_template = 'feeds/nodetype_description.html'

    def item_pubdate(self, item):
        """Publication date of a nodetype"""
        return item.creation_date

    def item_metatypes(self, item):
        """Nodetype's metatypes"""
        return [metatype.title for metatype in item.metatypes.all()]

    def item_author_name(self, item):
        """Returns the first author of a nodetype"""
        if item.authors.count():
            self.item_author = item.authors.all()[0]
            return self.item_author.username

    def item_author_email(self, item):
        """Returns the first author's email"""
        return self.item_author.email

    def item_author_link(self, item):
        """Returns the author's URL"""
        try:
            author_url = reverse('gstudio_author_detail',
                                 args=[self.item_author.username])
            return self.site_url + author_url
        except NoReverseMatch:
            return self.site_url

    def item_enclosure_url(self, item):
        """Returns an image for enclosure"""
        if item.image:
            return item.image.url

        img = BeautifulSoup(item.html_content).find('img')
        if img:
            return urljoin(self.site_url, img['src'])

    def item_enclosure_length(self, item):
        """Hardcoded enclosure length"""
        return '100000'

    def item_enclosure_mime_type(self, item):
        """Hardcoded enclosure mimetype"""
        return 'image/jpeg'


class LatestNodetypes(NodetypeFeed):
    """Feed for the latest nodetypes"""

    def link(self):
        """URL of latest nodetypes"""
        return reverse('gstudio_nodetype_archive_index')

    def items(self):
        """Items are published nodetypes"""
        return Nodetype.published.all()[:FEEDS_MAX_ITEMS]

    def title(self):
        """Title of the feed"""
        return '%s - %s' % (self.site.name, _('Latest nodetypes'))

    def description(self):
        """Description of the feed"""
        return _('The latest nodetypes for the site %s') % self.site.name


class MetatypeNodetypes(NodetypeFeed):
    """Feed filtered by a metatype"""

    def get_object(self, request, path):
        """Retrieve the metatype by his path"""
        return get_metatype_or_404(path)

    def items(self, obj):
        """Items are the published nodetypes of the metatype"""
        return obj.nodetypes_published()[:FEEDS_MAX_ITEMS]

    def link(self, obj):
        """URL of the metatype"""
        return obj.get_absolute_url()

    def title(self, obj):
        """Title of the feed"""
        return _('Nodetypes for the metatype %s') % obj.title

    def description(self, obj):
        """Description of the feed"""
        return _('The latest nodetypes for the metatype %s') % obj.title


class AuthorNodetypes(NodetypeFeed):
    """Feed filtered by an author"""

    def get_object(self, request, username):
        """Retrieve the author by his username"""
        return get_object_or_404(User, username=username)

    def items(self, obj):
        """Items are the published nodetypes of the author"""
        return nodetypes_published(obj.nodetypes)[:FEEDS_MAX_ITEMS]

    def link(self, obj):
        """URL of the author"""
        return reverse('gstudio_author_detail', args=[obj.username])

    def title(self, obj):
        """Title of the feed"""
        return _('Nodetypes for author %s') % obj.username

    def description(self, obj):
        """Description of the feed"""
        return _('The latest nodetypes by %s') % obj.username


class TagNodetypes(NodetypeFeed):
    """Feed filtered by a tag"""

    def get_object(self, request, slug):
        """Retrieve the tag by his name"""
        return get_object_or_404(Tag, name=slug)

    def items(self, obj):
        """Items are the published nodetypes of the tag"""
        return TaggedItem.objects.get_by_model(
            Nodetype.published.all(), obj)[:FEEDS_MAX_ITEMS]

    def link(self, obj):
        """URL of the tag"""
        return reverse('gstudio_tag_detail', args=[obj.name])

    def title(self, obj):
        """Title of the feed"""
        return _('Nodetypes for the tag %s') % obj.name

    def description(self, obj):
        """Description of the feed"""
        return _('The latest nodetypes for the tag %s') % obj.name


class SearchNodetypes(NodetypeFeed):
    """Feed filtered by a search pattern"""

    def get_object(self, request):
        """The GET parameter 'pattern' is the object"""
        pattern = request.GET.get('pattern', '')
        if len(pattern) < 3:
            raise ObjectDoesNotExist
        return pattern

    def items(self, obj):
        """Items are the published nodetypes founds"""
        return Nodetype.published.search(obj)[:FEEDS_MAX_ITEMS]

    def link(self, obj):
        """URL of the search request"""
        return '%s?pattern=%s' % (reverse('gstudio_nodetype_search'), obj)

    def title(self, obj):
        """Title of the feed"""
        return _("Results of the search for '%s'") % obj

    def description(self, obj):
        """Description of the feed"""
        return _("The nodetypes containing the pattern '%s'") % obj


class NodetypeDiscussions(GstudioFeed):
    """Feed for discussions in a nodetype"""
    title_template = 'feeds/discussion_title.html'
    description_template = 'feeds/discussion_description.html'

    def get_object(self, request, year, month, day, slug):
        """Retrieve the discussions by nodetype's slug"""
        return get_object_or_404(Nodetype.published, slug=slug,
                                 creation_date__year=year,
                                 creation_date__month=month,
                                 creation_date__day=day)

    def items(self, obj):
        """Items are the discussions on the nodetype"""
        return obj.discussions[:FEEDS_MAX_ITEMS]

    def item_pubdate(self, item):
        """Publication date of a discussion"""
        return item.submit_date

    def item_link(self, item):
        """URL of the discussion"""
        return item.get_absolute_url()

    def link(self, obj):
        """URL of the nodetype"""
        return obj.get_absolute_url()

    def item_author_name(self, item):
        """Author of the discussion"""
        return item.userinfo['name']

    def item_author_email(self, item):
        """Author's email of the discussion"""
        return item.userinfo['email']

    def item_author_link(self, item):
        """Author's URL of the discussion"""
        return item.userinfo['url']

    def title(self, obj):
        """Title of the feed"""
        return _('Discussions on %s') % obj.title

    def description(self, obj):
        """Description of the feed"""
        return _('The latest discussions for the nodetype %s') % obj.title


class NodetypeComments(NodetypeDiscussions):
    """Feed for comments in a nodetype"""
    title_template = 'feeds/comment_title.html'
    description_template = 'feeds/comment_description.html'

    def items(self, obj):
        """Items are the comments on the nodetype"""
        return obj.comments[:FEEDS_MAX_ITEMS]

    def item_link(self, item):
        """URL of the comment"""
        return item.get_absolute_url('#comment_%(id)s')

    def title(self, obj):
        """Title of the feed"""
        return _('Comments on %s') % obj.title

    def description(self, obj):
        """Description of the feed"""
        return _('The latest comments for the nodetype %s') % obj.title

    def item_enclosure_url(self, item):
        """Returns a gravatar image for enclosure"""
        return get_gravatar(item.userinfo['email'])

    def item_enclosure_length(self, item):
        """Hardcoded enclosure length"""
        return '100000'

    def item_enclosure_mime_type(self, item):
        """Hardcoded enclosure mimetype"""
        return 'image/jpeg'


class NodetypePingbacks(NodetypeDiscussions):
    """Feed for pingbacks in a nodetype"""
    title_template = 'feeds/pingback_title.html'
    description_template = 'feeds/pingback_description.html'

    def items(self, obj):
        """Items are the pingbacks on the nodetype"""
        return obj.pingbacks[:FEEDS_MAX_ITEMS]

    def item_link(self, item):
        """URL of the pingback"""
        return item.get_absolute_url('#pingback_%(id)s')

    def title(self, obj):
        """Title of the feed"""
        return _('Pingbacks on %s') % obj.title

    def description(self, obj):
        """Description of the feed"""
        return _('The latest pingbacks for the nodetype %s') % obj.title


class NodetypeTrackbacks(NodetypeDiscussions):
    """Feed for trackbacks in a nodetype"""
    title_template = 'feeds/trackback_title.html'
    description_template = 'feeds/trackback_description.html'

    def items(self, obj):
        """Items are the trackbacks on the nodetype"""
        return obj.trackbacks[:FEEDS_MAX_ITEMS]

    def item_link(self, item):
        """URL of the trackback"""
        return item.get_absolute_url('#trackback_%(id)s')

    def title(self, obj):
        """Title of the feed"""
        return _('Trackbacks on %s') % obj.title

    def description(self, obj):
        """Description of the feed"""
        return _('The latest trackbacks for the nodetype %s') % obj.title
