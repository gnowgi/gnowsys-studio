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
"""XML-RPC methods for Objectapp"""


OBJECTAPP_XMLRPC_PINGBACK = [
    ('objectapp.xmlrpc.pingback.pingback_ping',
     'pingback.ping'),
    ('objectapp.xmlrpc.pingback.pingback_extensions_get_pingbacks',
     'pingback.extensions.getPingbacks')]

OBJECTAPP_XMLRPC_METAWEBLOG = [
    ('objectapp.xmlrpc.metaweblog.get_users_blogs',
     'blogger.getUsersBlogs'),
    ('objectapp.xmlrpc.metaweblog.get_user_info',
     'blogger.getUserInfo'),
    ('objectapp.xmlrpc.metaweblog.delete_post',
     'blogger.deletePost'),
    ('objectapp.xmlrpc.metaweblog.get_authors',
     'wp.getAuthors'),
    ('objectapp.xmlrpc.metaweblog.get_objecttypes',
     'metaWeblog.getObjecttypes'),
    ('objectapp.xmlrpc.metaweblog.new_Objecttype',
     'wp.newObjecttype'),
    ('objectapp.xmlrpc.metaweblog.get_recent_posts',
     'metaWeblog.getRecentPosts'),
    ('objectapp.xmlrpc.metaweblog.get_post',
     'metaWeblog.getPost'),
    ('objectapp.xmlrpc.metaweblog.new_post',
     'metaWeblog.newPost'),
    ('objectapp.xmlrpc.metaweblog.edit_post',
     'metaWeblog.editPost'),
    ('objectapp.xmlrpc.metaweblog.new_media_object',
     'metaWeblog.newMediaObject')]

OBJECTAPP_XMLRPC_METHODS = OBJECTAPP_XMLRPC_PINGBACK + OBJECTAPP_XMLRPC_METAWEBLOG
