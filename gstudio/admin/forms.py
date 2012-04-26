"""Forms for Gstudio admin"""
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from gstudio.models import NID
from gstudio.models import Nodetype
from gstudio.models import Objecttype
from gstudio.models import Metatype
from gstudio.models import Relationtype
from gstudio.models import Relation
from gstudio.models import Attributetype
from gstudio.models import Attribute
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




from gstudio.models import Systemtype
from gstudio.models import Processtype


from gstudio.admin.widgets import TreeNodeChoiceField
from gstudio.admin.widgets import MPTTFilteredSelectMultiple
from gstudio.admin.widgets import MPTTModelMultipleChoiceField
from reversion.models import Version
        
class MetatypeAdminForm(forms.ModelForm):
    """Form for Metatype's Admin"""
    parent = TreeNodeChoiceField(
        label=_('parent metatype').capitalize(),
        required=False, empty_label=_('No parent metatype'),
        queryset=Metatype.tree.all())

    def __init__(self, *args, **kwargs):
        super(MetatypeAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(Metatype, 'id')
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget, rel, self.admin_site)

    def clean_parent(self):
        """Check if metatype parent is not selfish"""
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A metatype cannot be a parent of itself.'))
        return data

    class Meta:
        """MetatypeAdminForm's Meta"""
        model = Metatype


class ObjecttypeAdminForm(forms.ModelForm):
    """Form for Objecttype's Admin"""

    parent = TreeNodeChoiceField(
        label=_('parent nodetype').capitalize(),
        required=False, empty_label=_('No parent nodetype'),
        queryset=Nodetype.tree.all())

    metatypes = MPTTModelMultipleChoiceField(
        label=_('Metatypes'), required=False,
        queryset=Metatype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('metatypes'), False,
                                          attrs={'rows': '10'}))
    priornodes = MPTTModelMultipleChoiceField(
        label=_('priornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('nodetypes'), False,
                                          attrs={'rows': '10'}))

    posteriornodes = MPTTModelMultipleChoiceField(
        label=_('posteriornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('nodetypes'), False,
                                          attrs={'rows': '10'}))




    def __init__(self, *args, **kwargs):
        super(ObjecttypeAdminForm, self).__init__(*args, **kwargs)
        meta = ManyToManyRel(Metatype, 'id')
        prior = ManyToManyRel(Nodetype,'id')
        post = ManyToManyRel(Nodetype,'id')
        self.fields['metatypes'].widget = RelatedFieldWidgetWrapper(
            self.fields['metatypes'].widget, meta, self.admin_site)
        self.fields['priornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['priornodes'].widget, prior, self.admin_site)
        self.fields['posteriornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['posteriornodes'].widget, post, self.admin_site)



        self.fields['sites'].initial = [Site.objects.get_current()]

    def clean_parent(self):
        """Check if an object does not become a parent of itself"""
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('An objectype cannot be parent of itself.'))
        return data

    class Meta:
        """NodetypeAdminForm's Meta"""
        model = Objecttype


class RelationtypeAdminForm(forms.ModelForm):
    
    priornodes = MPTTModelMultipleChoiceField(
        label=_('Priornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('priornodes'), False,
                                          attrs={'rows': '10'}))
    posteriornodes = MPTTModelMultipleChoiceField(
        label=_('Prosterior Nodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('prosteriornode'), False,
                                          attrs={'rows': '10'}))

    def __init__(self, *args, **kwargs):
        super(RelationtypeAdminForm, self).__init__(*args, **kwargs)
        prior = ManyToManyRel(Nodetype, 'id')
        post = ManyToManyRel(Nodetype, 'id')
        
       

        self.fields['priornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['priornodes'].widget, prior, self.admin_site)
        self.fields['posteriornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['posteriornodes'].widget, post, self.admin_site)




    class Meta:
        """MetatypeAdminForm's Meta"""
        model = Relationtype


class RelationAdminForm(forms.ModelForm):


    def ApplicableNodeTypes_filter(self):
        choice = 'NT'
        if choice == 'ED':
            nid = 'Edge'
        if choice == 'ND':
            nid = 'Node' 
        if choice == 'NT':
            nid = 'Nodetype'
        if choice == 'ET':
            nid = 'Edgetype'
        if choice == 'OT':
            nid = 'Objecttype'
        if choice == 'RT':
            nid = 'Relationtype'
        if choice == 'MT':
            nid = 'Metatype'
        if choice == 'AT':
            nid = 'Attributetype'
        if choice == 'RN':
            nid = 'Relation'
        if choice == 'AS':
            nid = 'Attributes'
        if choice == 'ST':
            nid = 'Systemtype'
        if choice == 'SY':
            nid = 'System'

        node = NID.objects.get(Objecttype)
        vrs = Version.objects.filter(type=0 , object_id=node.id) 
        vrs =  vrs[0]
        AppNode = vrs.object._meta.module_name
        AppNodeList = AppNode.objects.all()
        return AppNodeList

        

    class Meta:
        """MetatypeAdminForm's Meta"""
        model = Relation


class ProcesstypeAdminForm(forms.ModelForm):

    priornodes = MPTTModelMultipleChoiceField(
        label=_('Priornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('priornodes'), False,
                                          attrs={'rows': '10'}))
    posteriornodes = MPTTModelMultipleChoiceField(
        label=_('Prosterior Nodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('prosteriornode'), False,
                                          attrs={'rows': '10'}))
    attributetype_set = MPTTModelMultipleChoiceField(
        label=_('Attributetype Sets'), required=False,
        queryset=Attributetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Attributetype Set'), False,
                                          attrs={'rows': '10'}))
    relationtype_set = MPTTModelMultipleChoiceField(
        label=_('Relationtype Set'), required=False,
        queryset=Relationtype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Relationtype Set'), False,
                                          attrs={'rows': '10'}))


    def __init__(self, *args, **kwargs):
        super(ProcesstypeAdminForm, self).__init__(*args, **kwargs)
        prior = ManyToManyRel(Nodetype, 'id')
        post = ManyToManyRel(Nodetype, 'id')
        atype = ManyToManyRel(Attributetype, 'id')
        rtype = ManyToManyRel(Relationtype, 'id')
       

        self.fields['priornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['priornodes'].widget, prior, self.admin_site)
        self.fields['posteriornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['posteriornodes'].widget, post, self.admin_site)
        self.fields['attributetype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['attributetype_set'].widget, atype, self.admin_site)
        self.fields['relationtype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['relationtype_set'].widget, rtype, self.admin_site)




    class Meta:
        """SystemAdminForm's Meta"""
        model = Processtype

class AttributetypeAdminForm(forms.ModelForm):
    priornodes = MPTTModelMultipleChoiceField(
        label=_('Priornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('priornodes'), False,
                                          attrs={'rows': '10'}))
    posteriornodes = MPTTModelMultipleChoiceField(
        label=_('Posterior Nodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('posteriornodes'), False,
                                          attrs={'rows': '10'}))
    def __init__(self, *args, **kwargs):
        super(AttributetypeAdminForm, self).__init__(*args, **kwargs)
        prior = ManyToManyRel(Nodetype, 'id')
        post = ManyToManyRel(Nodetype, 'id')
        self.fields['sites'].initial = [Site.objects.get_current()]

        self.fields['priornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['priornodes'].widget, prior, self.admin_site)
        self.fields['posteriornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['posteriornodes'].widget, post, self.admin_site)



    class Meta:
        """MetatypeAdminForm's Meta"""
        model = Attributetype


class AttributeAdminForm(forms.ModelForm):

    def subject_filter(attr):
        """
        returns applicable selection of nodes for selecting objects
        """
        for each in Objecttype.objects.all():
            if attr.subjecttype.id == each.id:
                return each.get_members

    def __init__(self, *args, **kwargs):
        super(AttributeAdminForm, self).__init__(*args, **kwargs)
        self.fields["subject"].queryset = subject_filter(attr)
        

    class Meta:
        """MetatypeAdminForm's Meta"""
        model = Attribute



class SystemtypeAdminForm(forms.ModelForm):
    nodetype_set = MPTTModelMultipleChoiceField(
        label=_('Nodetypeset'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Nodetypesets'), False,
                                          attrs={'rows': '10'}))
    relationtype_set = MPTTModelMultipleChoiceField(
        label=_('Relationtypeset'), required=False,
        queryset=Relationtype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Relationtypesets'), False,
                                          attrs={'rows': '10'}))
    attributetype_set = MPTTModelMultipleChoiceField(
        label=_('Attributetypeset'), required=False,
        queryset=Attributetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Attributetypesets'), False,
                                          attrs={'rows': '10'}))
    metatype_set = MPTTModelMultipleChoiceField(
        label=_('Metatypeset'), required=False,
        queryset=Metatype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('metatypesets'), False,
                                          attrs={'rows': '10'}))
    processtype_set = MPTTModelMultipleChoiceField(
        label=_('Processtypeset'), required=False,
        queryset=Processtype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('Processtypesets'), False,
                                          attrs={'rows': '10'}))

    priornodes = MPTTModelMultipleChoiceField(
        label=_('priornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('nodetypes'), False,
                                          attrs={'rows': '10'}))

    posteriornodes = MPTTModelMultipleChoiceField(
        label=_('posteriornodes'), required=False,
        queryset=Nodetype.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('nodetypes'), False,
                                          attrs={'rows': '10'}))
    def __init__(self, *args, **kwargs):
        super(SystemtypeAdminForm, self).__init__(*args, **kwargs)
        ot = ManyToManyRel(Nodetype,'id')
        rt = ManyToManyRel(Relationtype,'id')
        at = ManyToManyRel(Attributetype,'id')
        mt = ManyToManyRel(Metatype,'id')
        pt = ManyToManyRel(Processtype,'id')
        prior = ManyToManyRel(Nodetype,'id')
        post = ManyToManyRel(Nodetype,'id')

        self.fields['nodetype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['nodetype_set'].widget, ot, self.admin_site)
        self.fields['relationtype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['relationtype_set'].widget, rt, self.admin_site)
        self.fields['attributetype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['attributetype_set'].widget, at, self.admin_site)
        self.fields['metatype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['metatype_set'].widget, mt, self.admin_site)
        self.fields['processtype_set'].widget = RelatedFieldWidgetWrapper(
            self.fields['processtype_set'].widget, pt, self.admin_site)
        self.fields['priornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['priornodes'].widget, prior, self.admin_site)
        self.fields['posteriornodes'].widget = RelatedFieldWidgetWrapper(
            self.fields['posteriornodes'].widget, post, self.admin_site)




    class Meta:
        """SystemAdminForm's Meta"""
        model = Systemtype


class AttributeSpecificationAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeSpecification

class RelationSpecificationAdminForm(forms.ModelForm):
    class Meta:
        model = RelationSpecification

class NodeSpecificationAdminForm(forms.ModelForm):
    class Meta:
        model = NodeSpecification

class UnionAdminForm(forms.ModelForm):
    class Meta:
        model = Union

class ComplementAdminForm(forms.ModelForm):
    class Meta:
        model = Complement



class IntersectionAdminForm(forms.ModelForm):
    class Meta:
        model = Intersection


class ExpressionAdminForm(forms.ModelForm):
    class Meta:
        model = Expression

### Datatypes here ###

class AttributeCharFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeCharField

class AttributeTextFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeTextField

class AttributeIntegerFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeIntegerField

class AttributeCommaSeparatedIntegerFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeCommaSeparatedIntegerField
class AttributeBigIntegerFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeBigIntegerField
class AttributePositiveIntegerFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributePositiveIntegerField

class AttributeDecimalFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeDecimalField
class AttributeFloatFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeFloatField
class AttributeBooleanFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeBooleanField

class AttributeNullBooleanFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeNullBooleanField
class AttributeDateFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeDateField
class AttributeDateTimeFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeDateField

class AttributeTimeFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeTimeField

class AttributeEmailFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeEmailField
class AttributeFileFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeFileField
class AttributeFilePathFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeFilePathField
class AttributeImageFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeImageField

class AttributeURLFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeURLField
class AttributeIPAddressFieldAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeIPAddressField










