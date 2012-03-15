from gstudio.models import *
from objectapp.models import *
from reversion.models import *

mts = Metatype.objects.all()
ots = Objecttype.objects.all()
ot = Objecttype.objects.get(title='person')
ot2 = Objecttype.objects.get(title='city')
ot3 = Objecttype.objects.get(title='country')
ot4 = Objecttype.objects.get(title='place')
rts = Relationtype.objects.all()
rt1 = Relationtype.objects.get(title='capital of')
rs= Relation.objects.all()
#r1 = Relation.objects.get(relationtype=rt1.id)
at1 = Attributetype.objects.get(title='population')
o =Gbobject.objects.get(title='Mumbai')
a = Attribute.objects.all()
