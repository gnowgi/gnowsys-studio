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
#!/usr/bin/env python
# This file reads the gstudio and objectapp models and generates the gstudio_schema.png file
# Please make sure graphviz(django-graphviz) app folder 'graphviz' is in the application.
# And the settings.py file has a GRAPHVIZ_DOT_CMD='<dot command path>'. The <dot command path>' should contain the right path to graphviz,
# Usually its GRAPHVIZ_DOT_CMD='/usr/bin/dot'. 
#                                                                                                                       
# Then run python manage.py syncdb. 

import os
import fileinput

dot_path = 'gstudio_schema.dot'
img_path = 'gstudio_schema.svg'

try:
    # generate dot file
    os.system('python manage.py modelviz objectapp gstudio auth reversion mptt >' + dot_path )
    
    # find and Replace "Node" in the file
    #dotfile = open(dot_path,'rw')

    # replacing Node to gbNode in the dotfile as it conflicts with graphvizdot notation

    os.system("sed -i 's/Node ->/gbNode ->/g' " + dot_path)
    os.system("sed -i 's/-> Node/-> gbNode/g' " + dot_path)
    os.system("sed -i 's/-> Edge/-> gbEdge/g' " + dot_path)
    os.system("sed -i 's/Edge ->/gbEdge ->/g' " + dot_path)

    '''
    for line in fileinput.input(dot_path, inplace = 1): 
        print line.replace("-> Node", "-> gbNode"),
    
    for line in fileinput.input(dot_path, inplace = 1): 
        print line.replace("Node ->", "gbNode ->"),
    '''

    #reduce graph

    os.system("tred " + dot_path + "> reduced_" + dot_path )

    # generate png
    os.system('dot reduced_'+dot_path+' -Tsvg -o '+img_path)


except(Error):
    print "Please make sure django-graphviz app folder 'graphviz' is installed, the GRAPHVIZ_DOT_CMD contains the right path to graphviz, then run syncdb."



    

