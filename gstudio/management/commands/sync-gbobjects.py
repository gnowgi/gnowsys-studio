#    Copyright (c) 2012 Free Software Foundation

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand
from optparse import make_option

import re
from datetime import datetime
from objectapp.models import Gbobject
from xmlrpclib import DateTime
from xmlrpclib import ServerProxy

class Command(BaseCommand):
    """Gets all Gbobjects for a specified server"""
    option_list = BaseCommand.option_list + (
        make_option("--server", action="store", type="string",
                    dest="server", help="Specify an ip"),)

    def handle(self, *args, **options):
        def parse_id(id=None):
            def inner_parse(id):
                """Gets a dict, parses and saves it"""
                dict = srv.metaWeblog.dict_id(id)
                pattern = "^(\d{4})(\d{2})(\d{2}).(\d{2}).(\d{2}).(\d{2})$"

                cd = DateTime().make_comparable(dict['creation_date'])[1]
                lu = DateTime().make_comparable(dict['last_update'])[1]
                ep = DateTime().make_comparable(dict['end_publication'])[1]
                sp = DateTime().make_comparable(dict['start_publication'])[1]

                def group(value):
                    return value.group(1, 2, 3, 4, 5, 6)

                cd = group(re.search(pattern, cd))
                lu = group(re.search(pattern, lu))
                ep = group(re.search(pattern, ep))
                sp = group(re.search(pattern, sp))

                def str_to_int(string):
                    return [int(x) for x in string]

                cd = str_to_int(cd)
                lu = str_to_int(lu)
                ep = str_to_int(ep)
                sp = str_to_int(sp)

                dict['creation_date'] = datetime(*cd)
                dict['last_update'] = datetime(*lu)
                dict['end_publication'] = datetime(*ep)
                dict['start_publication'] = datetime(*sp)

                Gbobject(**dict).save()

            for d in srv.metaWeblog.dict_id():
                inner_parse(d['node_ptr_id'])

        server = options["server"]
        srv = ServerProxy(server, allow_none=True)
        parse_id()
