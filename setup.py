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


import os
from setuptools import setup, find_packages

import gstudio

setup(name='django-gstudio',
      version=gstudio.__version__,

      description='A collaborative blogspace for constructing and publishing semantic knowledge networks and ontologies',
      long_description='\n'.join([open('README.rst').read(),
                                  open(os.path.join('docs', 'install.rst')).read(),
                                  open(os.path.join('docs', 'changelog.rst')).read(),]),
      keywords='django, blog, weblog, zinnia, post, news, gnowsys, gnowledge, semantic, networks, ontolgies',

      author=gstudio.__author__,
      author_email=gstudio.__email__,
      url=gstudio.__url__,

      packages=find_packages(exclude=['demo','demo.graphviz','demo.graphviz.management','demo.graphviz.management.commands']),
      
      classifiers=[
          'Framework :: Django',
          'Development Status :: 3 - Development/Alpha',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Libraries :: Python Modules',],

      license=gstudio.__license__,
      include_package_data=True,
      zip_safe=False,
      install_requires=['BeautifulSoup>=3.2.0',
                        'django>=1.4',
                        'django-mptt>=0.4.2',
                        'django-tagging>=0.3.1',
                        'django-xmlrpc>=0.1.3',
                        'pyparsing>=1.5.5',
                        'django-reversion>=1.5.1',
                        'django-grappelli>=2.3.4',
                        'django-ratings>=0.3.6',
                        'rdflib>=3.0.0',
                        'django-registration>=0.8',
                        'django-4store>=0.3',
                        'HTTP4Store>=0.2',
			'html5lib>=0.95',
                        'PIL>=1.1.7',
                        'diff-match-patch>=20120106',
                      
                        ])
