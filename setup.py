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

setup(name='gnowsys-studio',
      version=gstudio.__version__,

      description='A collaborative blogspace for constructing and publishing semantic knowledge networks and ontologies',
      long_description='\n'.join([open('README.rst').read(),
                                  open(os.path.join('docs', 'install.rst')).read(),
                                  open(os.path.join('docs', 'changelog.rst')).read(),]),
      keywords='django, blog, weblog, zinnia, post, news, gnowsys, gnowledge, semantic, networks, ontolgies, knowledge, representation, concepts, graphs, gnu',

      author=gstudio.__author__,
      author_email=gstudio.__email__,
      url=gstudio.__url__,

      packages=find_packages(exclude=['demo','demo.graphviz','demo.graphviz.management','demo.graphviz.management.commands']),
      
      classifiers=[
          'Framework :: Django',
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Visualization',],
      

      license=gstudio.__license__,
      include_package_data=True,
      zip_safe=False,
      install_requires=['BeautifulSoup>=3.2.0',
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
                        'django-markitup>=1.0.0',
                        'inflection>=0.1.2',
                        'PIL>=1.1.7',
                        'diff-match-patch>=20120106',
                        'ox>=2.0.356',
                        'pandora_client>=0.2.94',
			'django-pagination>=1.0.7',
                        'inflect>=0.2.3',
                        ])
