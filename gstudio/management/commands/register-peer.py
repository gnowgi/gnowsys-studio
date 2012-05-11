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

# from django.core.management.base import BaseCommand
# from optparse import make_option
# import sys
# from gstudio.models import Peer

# class Command(BaseCommand):
#     """Custom manage.py command to register a peer"""
#     option_list = BaseCommand.option_list + (
#         make_option("--ip", action="store", type="string",
#                     dest="ip", help="Specify an IP"),
#         make_option("--pkey", action="store", type="string",
#                     dest="pkey", help="Specify a public-key"))

#     def handle(self, *args, **options):
#         try:
#             ip = options["ip"]
#             pkey = options["pkey"]

#             if not ip:
#                 sys.stderr.write("Please specify an IP\n")
#                 sys.exit(2)

#             if not pkey:
#                 sys.stderr.write("Please specify a public-key\n")
#                 sys.exit(2)

#             pkey = open(options["pkey"]).readline().rstrip()

#         except (IOError, TypeError):
#             sys.stderr.write("Please specify a correct public-key\n")
#             sys.exit(2)

#         ip = Peer(ip="{0}".format(ip))
#         ip.save()

#         pkey = Peer(pkey="{0}".format(pkey))
#         pkey.save()
