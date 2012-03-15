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



from gstudio.models import *
from objectapp.models import *
from reversion.models import Version

MAP = (
    ('objecttype','Objecttype'),
    ('gbobject', 'Gbobject')
       )


def get_slug(name):
    """
    returns the uri of the node. 
    """    
    try:
        """ 
        note: its very good to use only the meta information given for Version data, 
        individual object information is best retrieved from the main table. 
        # Also Version.object.meta contains a lot of valuable information about the model.
        """
        node = NID.objects.get(title=str(name))
        # Retrieving only the relevant tupleset for the versioned objects
        vrs = Version.objects.filter(type=0 , object_id=node.id) 
        vrs =  vrs[0]

    except:
        return "The item was not found."

    return vrs.object.get_absolute_url()

def get_nodetype(name):
    """
    returns the model the id belongs to.  
    """    
    try:
        """ 
        ALGO:     get object id, go to version model, return for the given id.
        """
        node = NID.objects.get(title=str(name))
        # Retrieving only the relevant tupleset for the versioned objects
        vrs = Version.objects.filter(type=0 , object_id=node.id) 
        # Returned value is a list, so splice it .
        vrs =  vrs[0]

    except:
        return "The item was not found."
        
    return vrs.object._meta.module_name   
    


def get_node(name):
    """
    returns a reference to the model object 
    """
    nt = get_nodetype(name)
    node = NID.objects.get(title=str(name))
    this_id = node.id
    if (nt == 'gbobject'):
        return Gbobject.objects.get(id=this_id)
    
    if (nt == 'objecttype'):
        return Objecttype.objects.get(id=this_id)

    if (nt == 'metatype'):
        return Metatype.objects.get(id=this_id)

    
