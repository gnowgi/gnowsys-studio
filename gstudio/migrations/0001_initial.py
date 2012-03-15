# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NID'
        db.create_table('gstudio_nid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('gstudio', ['NID'])

        # Adding model 'Node'
        db.create_table('gstudio_node', (
            ('nid_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.NID'], unique=True, primary_key=True)),
            ('altnames', self.gf('tagging.fields.TagField')(null=True)),
            ('plural', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('gstudio', ['Node'])

        # Adding model 'Edge'
        db.create_table('gstudio_edge', (
            ('nid_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.NID'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gstudio', ['Edge'])

        # Adding model 'Metatype'
        db.create_table('gstudio_metatype', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['gstudio.Metatype'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Metatype'])

        # Adding model 'Nodetype'
        db.create_table('gstudio_nodetype', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['gstudio.Nodetype'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pingback_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('start_publication', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end_publication', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2042, 3, 15, 0, 0))),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='gstudio/nodetype_detail.html', max_length=250)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Nodetype'])

        # Adding M2M table for field prior_nodes on 'Nodetype'
        db.create_table('gstudio_nodetype_prior_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False)),
            ('to_nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_nodetype_prior_nodes', ['from_nodetype_id', 'to_nodetype_id'])

        # Adding M2M table for field posterior_nodes on 'Nodetype'
        db.create_table('gstudio_nodetype_posterior_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False)),
            ('to_nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_nodetype_posterior_nodes', ['from_nodetype_id', 'to_nodetype_id'])

        # Adding M2M table for field metatypes on 'Nodetype'
        db.create_table('gstudio_nodetype_metatypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False)),
            ('metatype', models.ForeignKey(orm['gstudio.metatype'], null=False))
        ))
        db.create_unique('gstudio_nodetype_metatypes', ['nodetype_id', 'metatype_id'])

        # Adding M2M table for field authors on 'Nodetype'
        db.create_table('gstudio_nodetype_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('gstudio_nodetype_authors', ['nodetype_id', 'user_id'])

        # Adding M2M table for field sites on 'Nodetype'
        db.create_table('gstudio_nodetype_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('gstudio_nodetype_sites', ['nodetype_id', 'site_id'])

        # Adding model 'Objecttype'
        db.create_table('gstudio_objecttype', (
            ('nodetype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Nodetype'], unique=True, primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Objecttype'])

        # Adding model 'Relationtype'
        db.create_table('gstudio_relationtype', (
            ('nodetype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Nodetype'], unique=True, primary_key=True)),
            ('inverse', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('left_subjecttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='left_subjecttype_of', to=orm['gstudio.NID'])),
            ('left_applicable_nodetypes', self.gf('django.db.models.fields.CharField')(default='OT', max_length=2)),
            ('left_cardinality', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('right_subjecttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='right_subjecttype_of', to=orm['gstudio.NID'])),
            ('right_applicable_nodetypes', self.gf('django.db.models.fields.CharField')(default='OT', max_length=2)),
            ('right_cardinality', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_symmetrical', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_reflexive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_transitive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Relationtype'])

        # Adding model 'Attributetype'
        db.create_table('gstudio_attributetype', (
            ('nodetype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Nodetype'], unique=True, primary_key=True)),
            ('subjecttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjecttype_of', to=orm['gstudio.NID'])),
            ('applicable_nodetypes', self.gf('django.db.models.fields.CharField')(default='OT', max_length=2)),
            ('dataType', self.gf('django.db.models.fields.CharField')(default='01', max_length=2)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('null', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('blank', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('max_digits', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('decimal_places', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('auto_now', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('auto_now_add', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('upload_to', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('verify_exists', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('min_length', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('unique', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('editable', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Attributetype'])

        # Adding M2M table for field validators on 'Attributetype'
        db.create_table('gstudio_attributetype_validators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_attributetype', models.ForeignKey(orm['gstudio.attributetype'], null=False)),
            ('to_attributetype', models.ForeignKey(orm['gstudio.attributetype'], null=False))
        ))
        db.create_unique('gstudio_attributetype_validators', ['from_attributetype_id', 'to_attributetype_id'])

        # Adding model 'Relation'
        db.create_table('gstudio_relation', (
            ('edge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Edge'], unique=True, primary_key=True)),
            ('left_subject_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('left_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='left_subject_of', to=orm['gstudio.NID'])),
            ('relationtype_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('relationtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gstudio.Relationtype'])),
            ('right_subject_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('right_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='right_subject_of', to=orm['gstudio.NID'])),
        ))
        db.send_create_signal('gstudio', ['Relation'])

        # Adding unique constraint on 'Relation', fields ['left_subject_scope', 'left_subject', 'relationtype_scope', 'relationtype', 'right_subject_scope', 'right_subject']
        db.create_unique('gstudio_relation', ['left_subject_scope', 'left_subject_id', 'relationtype_scope', 'relationtype_id', 'right_subject_scope', 'right_subject_id'])

        # Adding model 'Attribute'
        db.create_table('gstudio_attribute', (
            ('edge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Edge'], unique=True, primary_key=True)),
            ('subject_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject_of', to=orm['gstudio.NID'])),
            ('attributetype_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('attributetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gstudio.Attributetype'])),
            ('value_scope', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('svalue', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['Attribute'])

        # Adding unique constraint on 'Attribute', fields ['subject_scope', 'subject', 'attributetype_scope', 'attributetype', 'value_scope', 'svalue']
        db.create_unique('gstudio_attribute', ['subject_scope', 'subject_id', 'attributetype_scope', 'attributetype_id', 'value_scope', 'svalue'])

        # Adding model 'AttributeCharField'
        db.create_table('gstudio_attributecharfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeCharField'])

        # Adding model 'AttributeTextField'
        db.create_table('gstudio_attributetextfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gstudio', ['AttributeTextField'])

        # Adding model 'AttributeIntegerField'
        db.create_table('gstudio_attributeintegerfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeIntegerField'])

        # Adding model 'AttributeCommaSeparatedIntegerField'
        db.create_table('gstudio_attributecommaseparatedintegerfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeCommaSeparatedIntegerField'])

        # Adding model 'AttributeBigIntegerField'
        db.create_table('gstudio_attributebigintegerfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.BigIntegerField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeBigIntegerField'])

        # Adding model 'AttributePositiveIntegerField'
        db.create_table('gstudio_attributepositiveintegerfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributePositiveIntegerField'])

        # Adding model 'AttributeDecimalField'
        db.create_table('gstudio_attributedecimalfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal('gstudio', ['AttributeDecimalField'])

        # Adding model 'AttributeFloatField'
        db.create_table('gstudio_attributefloatfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeFloatField'])

        # Adding model 'AttributeBooleanField'
        db.create_table('gstudio_attributebooleanfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gstudio', ['AttributeBooleanField'])

        # Adding model 'AttributeNullBooleanField'
        db.create_table('gstudio_attributenullbooleanfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('gstudio', ['AttributeNullBooleanField'])

        # Adding model 'AttributeDateField'
        db.create_table('gstudio_attributedatefield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.DateField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeDateField'])

        # Adding model 'AttributeDateTimeField'
        db.create_table('gstudio_attributedatetimefield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.DateTimeField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeDateTimeField'])

        # Adding model 'AttributeTimeField'
        db.create_table('gstudio_attributetimefield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TimeField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeTimeField'])

        # Adding model 'AttributeEmailField'
        db.create_table('gstudio_attributeemailfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeEmailField'])

        # Adding model 'AttributeFileField'
        db.create_table('gstudio_attributefilefield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeFileField'])

        # Adding model 'AttributeFilePathField'
        db.create_table('gstudio_attributefilepathfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.FilePathField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeFilePathField'])

        # Adding model 'AttributeImageField'
        db.create_table('gstudio_attributeimagefield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeImageField'])

        # Adding model 'AttributeURLField'
        db.create_table('gstudio_attributeurlfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.URLField')(max_length=100)),
        ))
        db.send_create_signal('gstudio', ['AttributeURLField'])

        # Adding model 'AttributeIPAddressField'
        db.create_table('gstudio_attributeipaddressfield', (
            ('attribute_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Attribute'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('gstudio', ['AttributeIPAddressField'])

        # Adding model 'Processtype'
        db.create_table('gstudio_processtype', (
            ('nodetype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Nodetype'], unique=True, primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Processtype'])

        # Adding M2M table for field changing_attributetype_set on 'Processtype'
        db.create_table('gstudio_processtype_changing_attributetype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('processtype', models.ForeignKey(orm['gstudio.processtype'], null=False)),
            ('attributetype', models.ForeignKey(orm['gstudio.attributetype'], null=False))
        ))
        db.create_unique('gstudio_processtype_changing_attributetype_set', ['processtype_id', 'attributetype_id'])

        # Adding M2M table for field changing_relationtype_set on 'Processtype'
        db.create_table('gstudio_processtype_changing_relationtype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('processtype', models.ForeignKey(orm['gstudio.processtype'], null=False)),
            ('relationtype', models.ForeignKey(orm['gstudio.relationtype'], null=False))
        ))
        db.create_unique('gstudio_processtype_changing_relationtype_set', ['processtype_id', 'relationtype_id'])

        # Adding model 'Systemtype'
        db.create_table('gstudio_systemtype', (
            ('nodetype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Nodetype'], unique=True, primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gstudio', ['Systemtype'])

        # Adding M2M table for field nodetype_set on 'Systemtype'
        db.create_table('gstudio_systemtype_nodetype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_systemtype_nodetype_set', ['systemtype_id', 'nodetype_id'])

        # Adding M2M table for field relationtype_set on 'Systemtype'
        db.create_table('gstudio_systemtype_relationtype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False)),
            ('relationtype', models.ForeignKey(orm['gstudio.relationtype'], null=False))
        ))
        db.create_unique('gstudio_systemtype_relationtype_set', ['systemtype_id', 'relationtype_id'])

        # Adding M2M table for field attributetype_set on 'Systemtype'
        db.create_table('gstudio_systemtype_attributetype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False)),
            ('attributetype', models.ForeignKey(orm['gstudio.attributetype'], null=False))
        ))
        db.create_unique('gstudio_systemtype_attributetype_set', ['systemtype_id', 'attributetype_id'])

        # Adding M2M table for field metatype_set on 'Systemtype'
        db.create_table('gstudio_systemtype_metatype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False)),
            ('metatype', models.ForeignKey(orm['gstudio.metatype'], null=False))
        ))
        db.create_unique('gstudio_systemtype_metatype_set', ['systemtype_id', 'metatype_id'])

        # Adding M2M table for field processtype_set on 'Systemtype'
        db.create_table('gstudio_systemtype_processtype_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False)),
            ('processtype', models.ForeignKey(orm['gstudio.processtype'], null=False))
        ))
        db.create_unique('gstudio_systemtype_processtype_set', ['systemtype_id', 'processtype_id'])

        # Adding model 'AttributeSpecification'
        db.create_table('gstudio_attributespecification', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('attributetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gstudio.Attributetype'])),
        ))
        db.send_create_signal('gstudio', ['AttributeSpecification'])

        # Adding M2M table for field subjects on 'AttributeSpecification'
        db.create_table('gstudio_attributespecification_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attributespecification', models.ForeignKey(orm['gstudio.attributespecification'], null=False)),
            ('nid', models.ForeignKey(orm['gstudio.nid'], null=False))
        ))
        db.create_unique('gstudio_attributespecification_subjects', ['attributespecification_id', 'nid_id'])

        # Adding model 'RelationSpecification'
        db.create_table('gstudio_relationspecification', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('relationtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gstudio.Relationtype'])),
        ))
        db.send_create_signal('gstudio', ['RelationSpecification'])

        # Adding M2M table for field subjects on 'RelationSpecification'
        db.create_table('gstudio_relationspecification_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relationspecification', models.ForeignKey(orm['gstudio.relationspecification'], null=False)),
            ('nid', models.ForeignKey(orm['gstudio.nid'], null=False))
        ))
        db.create_unique('gstudio_relationspecification_subjects', ['relationspecification_id', 'nid_id'])

        # Adding model 'NodeSpecification'
        db.create_table('gstudio_nodespecification', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject_nodespec', to=orm['gstudio.Node'])),
        ))
        db.send_create_signal('gstudio', ['NodeSpecification'])

        # Adding M2M table for field relations on 'NodeSpecification'
        db.create_table('gstudio_nodespecification_relations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodespecification', models.ForeignKey(orm['gstudio.nodespecification'], null=False)),
            ('relation', models.ForeignKey(orm['gstudio.relation'], null=False))
        ))
        db.create_unique('gstudio_nodespecification_relations', ['nodespecification_id', 'relation_id'])

        # Adding M2M table for field attributes on 'NodeSpecification'
        db.create_table('gstudio_nodespecification_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodespecification', models.ForeignKey(orm['gstudio.nodespecification'], null=False)),
            ('attribute', models.ForeignKey(orm['gstudio.attribute'], null=False))
        ))
        db.create_unique('gstudio_nodespecification_attributes', ['nodespecification_id', 'attribute_id'])

        # Adding model 'Union'
        db.create_table('gstudio_union', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gstudio', ['Union'])

        # Adding M2M table for field nodetypes on 'Union'
        db.create_table('gstudio_union_nodetypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('union', models.ForeignKey(orm['gstudio.union'], null=False)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_union_nodetypes', ['union_id', 'nodetype_id'])

        # Adding model 'Complement'
        db.create_table('gstudio_complement', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gstudio', ['Complement'])

        # Adding M2M table for field nodetypes on 'Complement'
        db.create_table('gstudio_complement_nodetypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('complement', models.ForeignKey(orm['gstudio.complement'], null=False)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_complement_nodetypes', ['complement_id', 'nodetype_id'])

        # Adding model 'Intersection'
        db.create_table('gstudio_intersection', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gstudio', ['Intersection'])

        # Adding M2M table for field nodetypes on 'Intersection'
        db.create_table('gstudio_intersection_nodetypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('intersection', models.ForeignKey(orm['gstudio.intersection'], null=False)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('gstudio_intersection_nodetypes', ['intersection_id', 'nodetype_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Attribute', fields ['subject_scope', 'subject', 'attributetype_scope', 'attributetype', 'value_scope', 'svalue']
        db.delete_unique('gstudio_attribute', ['subject_scope', 'subject_id', 'attributetype_scope', 'attributetype_id', 'value_scope', 'svalue'])

        # Removing unique constraint on 'Relation', fields ['left_subject_scope', 'left_subject', 'relationtype_scope', 'relationtype', 'right_subject_scope', 'right_subject']
        db.delete_unique('gstudio_relation', ['left_subject_scope', 'left_subject_id', 'relationtype_scope', 'relationtype_id', 'right_subject_scope', 'right_subject_id'])

        # Deleting model 'NID'
        db.delete_table('gstudio_nid')

        # Deleting model 'Node'
        db.delete_table('gstudio_node')

        # Deleting model 'Edge'
        db.delete_table('gstudio_edge')

        # Deleting model 'Metatype'
        db.delete_table('gstudio_metatype')

        # Deleting model 'Nodetype'
        db.delete_table('gstudio_nodetype')

        # Removing M2M table for field prior_nodes on 'Nodetype'
        db.delete_table('gstudio_nodetype_prior_nodes')

        # Removing M2M table for field posterior_nodes on 'Nodetype'
        db.delete_table('gstudio_nodetype_posterior_nodes')

        # Removing M2M table for field metatypes on 'Nodetype'
        db.delete_table('gstudio_nodetype_metatypes')

        # Removing M2M table for field authors on 'Nodetype'
        db.delete_table('gstudio_nodetype_authors')

        # Removing M2M table for field sites on 'Nodetype'
        db.delete_table('gstudio_nodetype_sites')

        # Deleting model 'Objecttype'
        db.delete_table('gstudio_objecttype')

        # Deleting model 'Relationtype'
        db.delete_table('gstudio_relationtype')

        # Deleting model 'Attributetype'
        db.delete_table('gstudio_attributetype')

        # Removing M2M table for field validators on 'Attributetype'
        db.delete_table('gstudio_attributetype_validators')

        # Deleting model 'Relation'
        db.delete_table('gstudio_relation')

        # Deleting model 'Attribute'
        db.delete_table('gstudio_attribute')

        # Deleting model 'AttributeCharField'
        db.delete_table('gstudio_attributecharfield')

        # Deleting model 'AttributeTextField'
        db.delete_table('gstudio_attributetextfield')

        # Deleting model 'AttributeIntegerField'
        db.delete_table('gstudio_attributeintegerfield')

        # Deleting model 'AttributeCommaSeparatedIntegerField'
        db.delete_table('gstudio_attributecommaseparatedintegerfield')

        # Deleting model 'AttributeBigIntegerField'
        db.delete_table('gstudio_attributebigintegerfield')

        # Deleting model 'AttributePositiveIntegerField'
        db.delete_table('gstudio_attributepositiveintegerfield')

        # Deleting model 'AttributeDecimalField'
        db.delete_table('gstudio_attributedecimalfield')

        # Deleting model 'AttributeFloatField'
        db.delete_table('gstudio_attributefloatfield')

        # Deleting model 'AttributeBooleanField'
        db.delete_table('gstudio_attributebooleanfield')

        # Deleting model 'AttributeNullBooleanField'
        db.delete_table('gstudio_attributenullbooleanfield')

        # Deleting model 'AttributeDateField'
        db.delete_table('gstudio_attributedatefield')

        # Deleting model 'AttributeDateTimeField'
        db.delete_table('gstudio_attributedatetimefield')

        # Deleting model 'AttributeTimeField'
        db.delete_table('gstudio_attributetimefield')

        # Deleting model 'AttributeEmailField'
        db.delete_table('gstudio_attributeemailfield')

        # Deleting model 'AttributeFileField'
        db.delete_table('gstudio_attributefilefield')

        # Deleting model 'AttributeFilePathField'
        db.delete_table('gstudio_attributefilepathfield')

        # Deleting model 'AttributeImageField'
        db.delete_table('gstudio_attributeimagefield')

        # Deleting model 'AttributeURLField'
        db.delete_table('gstudio_attributeurlfield')

        # Deleting model 'AttributeIPAddressField'
        db.delete_table('gstudio_attributeipaddressfield')

        # Deleting model 'Processtype'
        db.delete_table('gstudio_processtype')

        # Removing M2M table for field changing_attributetype_set on 'Processtype'
        db.delete_table('gstudio_processtype_changing_attributetype_set')

        # Removing M2M table for field changing_relationtype_set on 'Processtype'
        db.delete_table('gstudio_processtype_changing_relationtype_set')

        # Deleting model 'Systemtype'
        db.delete_table('gstudio_systemtype')

        # Removing M2M table for field nodetype_set on 'Systemtype'
        db.delete_table('gstudio_systemtype_nodetype_set')

        # Removing M2M table for field relationtype_set on 'Systemtype'
        db.delete_table('gstudio_systemtype_relationtype_set')

        # Removing M2M table for field attributetype_set on 'Systemtype'
        db.delete_table('gstudio_systemtype_attributetype_set')

        # Removing M2M table for field metatype_set on 'Systemtype'
        db.delete_table('gstudio_systemtype_metatype_set')

        # Removing M2M table for field processtype_set on 'Systemtype'
        db.delete_table('gstudio_systemtype_processtype_set')

        # Deleting model 'AttributeSpecification'
        db.delete_table('gstudio_attributespecification')

        # Removing M2M table for field subjects on 'AttributeSpecification'
        db.delete_table('gstudio_attributespecification_subjects')

        # Deleting model 'RelationSpecification'
        db.delete_table('gstudio_relationspecification')

        # Removing M2M table for field subjects on 'RelationSpecification'
        db.delete_table('gstudio_relationspecification_subjects')

        # Deleting model 'NodeSpecification'
        db.delete_table('gstudio_nodespecification')

        # Removing M2M table for field relations on 'NodeSpecification'
        db.delete_table('gstudio_nodespecification_relations')

        # Removing M2M table for field attributes on 'NodeSpecification'
        db.delete_table('gstudio_nodespecification_attributes')

        # Deleting model 'Union'
        db.delete_table('gstudio_union')

        # Removing M2M table for field nodetypes on 'Union'
        db.delete_table('gstudio_union_nodetypes')

        # Deleting model 'Complement'
        db.delete_table('gstudio_complement')

        # Removing M2M table for field nodetypes on 'Complement'
        db.delete_table('gstudio_complement_nodetypes')

        # Deleting model 'Intersection'
        db.delete_table('gstudio_intersection')

        # Removing M2M table for field nodetypes on 'Intersection'
        db.delete_table('gstudio_intersection_nodetypes')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gstudio.attribute': {
            'Meta': {'unique_together': "(('subject_scope', 'subject', 'attributetype_scope', 'attributetype', 'value_scope', 'svalue'),)", 'object_name': 'Attribute', '_ormbases': ['gstudio.Edge']},
            'attributetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gstudio.Attributetype']"}),
            'attributetype_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'edge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Edge']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_of'", 'to': "orm['gstudio.NID']"}),
            'subject_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'svalue': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'gstudio.attributebigintegerfield': {
            'Meta': {'object_name': 'AttributeBigIntegerField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.BigIntegerField', [], {'max_length': '100'})
        },
        'gstudio.attributebooleanfield': {
            'Meta': {'object_name': 'AttributeBooleanField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gstudio.attributecharfield': {
            'Meta': {'object_name': 'AttributeCharField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gstudio.attributecommaseparatedintegerfield': {
            'Meta': {'object_name': 'AttributeCommaSeparatedIntegerField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'})
        },
        'gstudio.attributedatefield': {
            'Meta': {'object_name': 'AttributeDateField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.DateField', [], {'max_length': '100'})
        },
        'gstudio.attributedatetimefield': {
            'Meta': {'object_name': 'AttributeDateTimeField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.DateTimeField', [], {'max_length': '100'})
        },
        'gstudio.attributedecimalfield': {
            'Meta': {'object_name': 'AttributeDecimalField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        'gstudio.attributeemailfield': {
            'Meta': {'object_name': 'AttributeEmailField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gstudio.attributefilefield': {
            'Meta': {'object_name': 'AttributeFileField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'gstudio.attributefilepathfield': {
            'Meta': {'object_name': 'AttributeFilePathField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.FilePathField', [], {'max_length': '100'})
        },
        'gstudio.attributefloatfield': {
            'Meta': {'object_name': 'AttributeFloatField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'max_length': '100'})
        },
        'gstudio.attributeimagefield': {
            'Meta': {'object_name': 'AttributeImageField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'gstudio.attributeintegerfield': {
            'Meta': {'object_name': 'AttributeIntegerField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '100'})
        },
        'gstudio.attributeipaddressfield': {
            'Meta': {'object_name': 'AttributeIPAddressField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        'gstudio.attributenullbooleanfield': {
            'Meta': {'object_name': 'AttributeNullBooleanField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'gstudio.attributepositiveintegerfield': {
            'Meta': {'object_name': 'AttributePositiveIntegerField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '100'})
        },
        'gstudio.attributespecification': {
            'Meta': {'object_name': 'AttributeSpecification', '_ormbases': ['gstudio.Node']},
            'attributetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gstudio.Attributetype']"}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subjects_attrspec_of'", 'symmetrical': 'False', 'to': "orm['gstudio.NID']"})
        },
        'gstudio.attributetextfield': {
            'Meta': {'object_name': 'AttributeTextField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'gstudio.attributetimefield': {
            'Meta': {'object_name': 'AttributeTimeField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TimeField', [], {'max_length': '100'})
        },
        'gstudio.attributetype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Attributetype', '_ormbases': ['gstudio.Nodetype']},
            'applicable_nodetypes': ('django.db.models.fields.CharField', [], {'default': "'OT'", 'max_length': '2'}),
            'auto_now': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'auto_now_add': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'blank': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.CharField', [], {'default': "'01'", 'max_length': '2'}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'editable': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'max_digits': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'nodetype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Nodetype']", 'unique': 'True', 'primary_key': 'True'}),
            'null': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'subjecttype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjecttype_of'", 'to': "orm['gstudio.NID']"}),
            'unique': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'upload_to': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'validators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'validators_rel_+'", 'null': 'True', 'to': "orm['gstudio.Attributetype']"}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'verify_exists': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'gstudio.attributeurlfield': {
            'Meta': {'object_name': 'AttributeURLField', '_ormbases': ['gstudio.Attribute']},
            'attribute_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Attribute']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        },
        'gstudio.complement': {
            'Meta': {'object_name': 'Complement', '_ormbases': ['gstudio.Node']},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'nodetypes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'complement_of'", 'symmetrical': 'False', 'to': "orm['gstudio.Nodetype']"})
        },
        'gstudio.edge': {
            'Meta': {'object_name': 'Edge', '_ormbases': ['gstudio.NID']},
            'nid_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.NID']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gstudio.intersection': {
            'Meta': {'object_name': 'Intersection', '_ormbases': ['gstudio.Node']},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'nodetypes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'intersection_of'", 'symmetrical': 'False', 'to': "orm['gstudio.Nodetype']"})
        },
        'gstudio.metatype': {
            'Meta': {'ordering': "['title']", 'object_name': 'Metatype', '_ormbases': ['gstudio.Node']},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['gstudio.Metatype']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'gstudio.nid': {
            'Meta': {'object_name': 'NID'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'gstudio.node': {
            'Meta': {'object_name': 'Node', '_ormbases': ['gstudio.NID']},
            'altnames': ('tagging.fields.TagField', [], {'null': 'True'}),
            'nid_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.NID']", 'unique': 'True', 'primary_key': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'gstudio.nodespecification': {
            'Meta': {'object_name': 'NodeSpecification', '_ormbases': ['gstudio.Node']},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attributes_in_nodespec'", 'symmetrical': 'False', 'to': "orm['gstudio.Attribute']"}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'relations_in_nodespec'", 'symmetrical': 'False', 'to': "orm['gstudio.Relation']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_nodespec'", 'to': "orm['gstudio.Node']"})
        },
        'gstudio.nodetype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Nodetype', '_ormbases': ['gstudio.Node']},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'nodetypes'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'comment_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end_publication': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2042, 3, 15, 0, 0)'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metatypes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_types'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Metatype']"}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['gstudio.Nodetype']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pingback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'posterior_nodes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posterior_nodes_rel_+'", 'null': 'True', 'to': "orm['gstudio.Nodetype']"}),
            'prior_nodes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'prior_nodes_rel_+'", 'null': 'True', 'to': "orm['gstudio.Nodetype']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nodetypes'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'start_publication': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'gstudio/nodetype_detail.html'", 'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'gstudio.objecttype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Objecttype', '_ormbases': ['gstudio.Nodetype']},
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nodetype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Nodetype']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gstudio.processtype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Processtype', '_ormbases': ['gstudio.Nodetype']},
            'changing_attributetype_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "' changing_attributetype_set_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Attributetype']"}),
            'changing_relationtype_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'changing_relationtype_set_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Relationtype']"}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nodetype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Nodetype']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gstudio.relation': {
            'Meta': {'unique_together': "(('left_subject_scope', 'left_subject', 'relationtype_scope', 'relationtype', 'right_subject_scope', 'right_subject'),)", 'object_name': 'Relation', '_ormbases': ['gstudio.Edge']},
            'edge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Edge']", 'unique': 'True', 'primary_key': 'True'}),
            'left_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left_subject_of'", 'to': "orm['gstudio.NID']"}),
            'left_subject_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'relationtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gstudio.Relationtype']"}),
            'relationtype_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'right_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right_subject_of'", 'to': "orm['gstudio.NID']"}),
            'right_subject_scope': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'gstudio.relationspecification': {
            'Meta': {'object_name': 'RelationSpecification', '_ormbases': ['gstudio.Node']},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'relationtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gstudio.Relationtype']"}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subjects_in_relspec'", 'symmetrical': 'False', 'to': "orm['gstudio.NID']"})
        },
        'gstudio.relationtype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Relationtype', '_ormbases': ['gstudio.Nodetype']},
            'inverse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'is_reflexive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_symmetrical': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_transitive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'left_applicable_nodetypes': ('django.db.models.fields.CharField', [], {'default': "'OT'", 'max_length': '2'}),
            'left_cardinality': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'left_subjecttype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left_subjecttype_of'", 'to': "orm['gstudio.NID']"}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nodetype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Nodetype']", 'unique': 'True', 'primary_key': 'True'}),
            'right_applicable_nodetypes': ('django.db.models.fields.CharField', [], {'default': "'OT'", 'max_length': '2'}),
            'right_cardinality': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'right_subjecttype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right_subjecttype_of'", 'to': "orm['gstudio.NID']"})
        },
        'gstudio.systemtype': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Systemtype', '_ormbases': ['gstudio.Nodetype']},
            'attributetype_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'attributetype_set_of'", 'blank': 'True', 'to': "orm['gstudio.Attributetype']"}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'metatype_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'metatype_set_of'", 'blank': 'True', 'to': "orm['gstudio.Metatype']"}),
            'nodetype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Nodetype']", 'unique': 'True', 'primary_key': 'True'}),
            'nodetype_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'nodetype_set_of'", 'blank': 'True', 'to': "orm['gstudio.Nodetype']"}),
            'processtype_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'processtype_set_of'", 'blank': 'True', 'to': "orm['gstudio.Processtype']"}),
            'relationtype_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'relationtype_set_of'", 'blank': 'True', 'to': "orm['gstudio.Relationtype']"})
        },
        'gstudio.union': {
            'Meta': {'object_name': 'Union', '_ormbases': ['gstudio.Node']},
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'nodetypes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'union_of'", 'symmetrical': 'False', 'to': "orm['gstudio.Nodetype']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['gstudio']
