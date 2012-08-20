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
import sys
from datetime import datetime

from objectapp.models import ObjectDoesNotExist

# from gstudio.xmlrpc.metaweblog import class_checker
from gstudio import models as gstmodels
from objectapp import models as objmodels
import inspect

from xmlrpclib import DateTime
from xmlrpclib import ServerProxy

from django.db.utils import IntegrityError

class Command(BaseCommand):
    """Gets all Gbobjects from a specified server"""
    option_list = BaseCommand.option_list + (
        make_option("--server", action="store", type="string",
                    dest="server", help="Specify IP address or URI"),
        make_option("--instance", action="store", type="string",
                    dest="instance", help="Specify an instance"),)

    def handle(self, *args, **options):
        def class_checker(m):
            """Returns a dict which contains all classes of the m module"""
            res = {}
            for name, obj in inspect.getmembers(m):
                if inspect.isclass(obj) and obj.__module__ == m.__name__:
                    res[name] = obj
            return res

        def parse(module=None, instance=None, id=None):
            """Parses and saves instances"""
            try:
                instances = srv.metaWeblog.show_instance(module, instance, id)

                if module == "objectapp.models":
                    module = objmodels

                if module == "gstudio.models":
                    module = gstmodels

                for i in instances:
                    pattern = "^(\d{4})(\d{2})(\d{2}).(\d{2}).(\d{2}).(\d{2})$"

                    if "_tags_cache" in i:
                        del i["_tags_cache"]

                    if "_state" in i:
                        del i["_state"]

                    if "_altnames_cache" in i:
                        del i["_altnames_cache"]

                    if "_mptt_cached_fields" in i:
                        del i["_mptt_cached_fields"]

                    def group(value):
                        return value.group(1, 2, 3, 4, 5, 6)

                    def str_to_int(string):
                        return [int(x) for x in string]

                    # Weird check for DateTime objects

                    for key in i.keys():
                        if "make_comparable" in dir(i[key]):
                            dt = DateTime().make_comparable(i[key])[1]
                            dt = str_to_int(group(re.search(pattern, dt)))

                            i[key] = datetime(*dt)

                    class_checker(module)[instance](**i).save()

            except (ObjectDoesNotExist, IntegrityError):
                sys.stderr.write("sync-instances.py:55: "
                                 "Object matching query does not exist\n")

            except ValueError:
                sys.stderr.write("sync-instances.py:93: "
                                 "Object already exists\n")

        server = options["server"]
        srv = ServerProxy(server, allow_none=True)

        instance = options["instance"]

        objcc = class_checker(objmodels)
        gstcc = class_checker(gstmodels)

        if instance:
            if instance in objkeys:
                parse("objectapp.models", instance)

            if instance in gstkeys:
                parse("gstudio.models", instance)

        else:
            for i in objkeys:
                parse("objectapp.models", i)

            for i in gstkeys:
                parse("gstudio.models", i)
