"""Admin of Gstudio"""
from django.contrib import admin

#Models import
from gstudio.models import Objecttype
from gstudio.models import Metatype
from gstudio.models import Relation
from gstudio.models import Relationtype
from gstudio.models import Attribute
from gstudio.models import Attributetype
from gstudio.models import Systemtype
from gstudio.models import Processtype
from gstudio.models import AttributeSpecification
from gstudio.models import RelationSpecification
from gstudio.models import NodeSpecification
from gstudio.models import Union
from gstudio.models import Complement
from gstudio.models import Intersection
from gstudio.models import Expression
from gstudio.models import AttributeCharField
from gstudio.models import AttributeTextField
from gstudio.models import AttributeIntegerField
from gstudio.models import AttributeCommaSeparatedIntegerField
from gstudio.models import AttributeBigIntegerField
from gstudio.models import AttributePositiveIntegerField
from gstudio.models import AttributeDecimalField
from gstudio.models import AttributeFloatField 
from gstudio.models import AttributeBooleanField
from gstudio.models import AttributeNullBooleanField
from gstudio.models import AttributeDateField
from gstudio.models import AttributeDateTimeField
from gstudio.models import AttributeTimeField
from gstudio.models import AttributeEmailField
from gstudio.models import AttributeFileField
from gstudio.models import AttributeFilePathField
from gstudio.models import AttributeImageField
from gstudio.models import AttributeURLField
from gstudio.models import AttributeIPAddressField
from gstudio.models import Peer


#Admin imports

from gstudio.admin.objecttype import ObjecttypeAdmin
from gstudio.admin.metatype import MetatypeAdmin
from gstudio.admin.relationtype import RelationtypeAdmin
from gstudio.admin.relation import RelationAdmin
from gstudio.admin.attribute import AttributeAdmin
from gstudio.admin.attributetype import AttributetypeAdmin
from gstudio.admin.attributespecification import AttributeSpecificationAdmin
from gstudio.admin.relationspecification import RelationSpecificationAdmin
from gstudio.admin.nodespecification import NodeSpecificationAdmin
from gstudio.admin.union import UnionAdmin
from gstudio.admin.complement import ComplementAdmin
from gstudio.admin.intersection import IntersectionAdmin 
from gstudio.admin.expression import ExpressionAdmin 
from gstudio.admin.systemtype import SystemtypeAdmin
from gstudio.admin.processtype import ProcesstypeAdmin

from gstudio.admin.attribute_charfield import AttributeCharFieldAdmin 
from gstudio.admin.attribute_textfield import AttributeTextFieldAdmin
from gstudio.admin.attribute_integerfield import AttributeIntegerFieldAdmin
from gstudio.admin.attribute_commaseparatedintegerfield import AttributeCommaSeparatedIntegerFieldAdmin
from gstudio.admin.attribute_bigintegerfield import AttributeBigIntegerFieldAdmin
from gstudio.admin.attribute_positiveintegerfield import AttributePositiveIntegerFieldAdmin
from gstudio.admin.attribute_decimalfield import AttributeDecimalFieldAdmin
from gstudio.admin.attribute_floatfield import AttributeFloatFieldAdmin
from gstudio.admin.attribute_booleanfield import AttributeBooleanFieldAdmin
from gstudio.admin.attribute_nullbooleanfield import AttributeNullBooleanFieldAdmin
from gstudio.admin.attribute_datefield import AttributeDateFieldAdmin
from gstudio.admin.attribute_datetimefield import AttributeDateTimeFieldAdmin
from gstudio.admin.attribute_timefield import AttributeTimeFieldAdmin
from gstudio.admin.attribute_emailfield import AttributeEmailFieldAdmin
from gstudio.admin.attribute_filefield import AttributeFileFieldAdmin
from gstudio.admin.attribute_filepathfield import AttributeFilePathFieldAdmin
from gstudio.admin.attribute_imagefield import AttributeImageFieldAdmin
from gstudio.admin.attribute_urlfield import AttributeURLFieldAdmin
from gstudio.admin.attribute_ipaddressfield import AttributeIPAddressFieldAdmin






admin.site.register(Objecttype, ObjecttypeAdmin)
admin.site.register(Metatype, MetatypeAdmin)
admin.site.register(Relationtype, RelationtypeAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Attributetype, AttributetypeAdmin)

admin.site.register(Systemtype, SystemtypeAdmin)
admin.site.register(Processtype, ProcesstypeAdmin)
admin.site.register(AttributeSpecification, AttributeSpecificationAdmin)
admin.site.register(RelationSpecification, RelationSpecificationAdmin)
admin.site.register(NodeSpecification, NodeSpecificationAdmin)
admin.site.register(Union, UnionAdmin)
admin.site.register(Complement, ComplementAdmin)
admin.site.register(Intersection, IntersectionAdmin)
admin.site.register(Expression, ExpressionAdmin)
admin.site.register(Peer)


admin.site.register(AttributeCharField, AttributeCharFieldAdmin)
admin.site.register(AttributeTextField, AttributeTextFieldAdmin)
admin.site.register(AttributeIntegerField, AttributeIntegerFieldAdmin)
admin.site.register(AttributeCommaSeparatedIntegerField, AttributeCommaSeparatedIntegerFieldAdmin)
admin.site.register(AttributeBigIntegerField,AttributeBigIntegerFieldAdmin)
admin.site.register(AttributePositiveIntegerField, AttributePositiveIntegerFieldAdmin)
admin.site.register(AttributeDecimalField, AttributeDecimalFieldAdmin)
admin.site.register(AttributeFloatField, AttributeFloatFieldAdmin)  
admin.site.register(AttributeBooleanField, AttributeBooleanFieldAdmin)
admin.site.register(AttributeNullBooleanField, AttributeNullBooleanFieldAdmin)
admin.site.register(AttributeDateField, AttributeDateFieldAdmin)
admin.site.register(AttributeDateTimeField, AttributeDateTimeFieldAdmin)
admin.site.register(AttributeTimeField,AttributeTimeFieldAdmin)
admin.site.register(AttributeEmailField, AttributeEmailFieldAdmin)
admin.site.register(AttributeFileField, AttributeFileFieldAdmin)
admin.site.register(AttributeFilePathField, AttributeFilePathFieldAdmin)
admin.site.register(AttributeImageField, AttributeImageFieldAdmin)
admin.site.register(AttributeURLField, AttributeURLFieldAdmin)
admin.site.register(AttributeIPAddressField, AttributeIPAddressFieldAdmin)

