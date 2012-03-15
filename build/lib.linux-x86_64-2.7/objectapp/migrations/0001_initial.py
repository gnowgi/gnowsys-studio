# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Gbobject'
        db.create_table('objectapp_gbobject', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gstudio.Node'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
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
            ('template', self.gf('django.db.models.fields.CharField')(default='objectapp/gbobject_detail.html', max_length=250)),
        ))
        db.send_create_signal('objectapp', ['Gbobject'])

        # Adding M2M table for field prior_nodes on 'Gbobject'
        db.create_table('objectapp_gbobject_prior_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False)),
            ('to_gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False))
        ))
        db.create_unique('objectapp_gbobject_prior_nodes', ['from_gbobject_id', 'to_gbobject_id'])

        # Adding M2M table for field posterior_nodes on 'Gbobject'
        db.create_table('objectapp_gbobject_posterior_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False)),
            ('to_gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False))
        ))
        db.create_unique('objectapp_gbobject_posterior_nodes', ['from_gbobject_id', 'to_gbobject_id'])

        # Adding M2M table for field objecttypes on 'Gbobject'
        db.create_table('objectapp_gbobject_objecttypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False)),
            ('nodetype', models.ForeignKey(orm['gstudio.nodetype'], null=False))
        ))
        db.create_unique('objectapp_gbobject_objecttypes', ['gbobject_id', 'nodetype_id'])

        # Adding M2M table for field authors on 'Gbobject'
        db.create_table('objectapp_gbobject_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('objectapp_gbobject_authors', ['gbobject_id', 'user_id'])

        # Adding M2M table for field sites on 'Gbobject'
        db.create_table('objectapp_gbobject_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('objectapp_gbobject_sites', ['gbobject_id', 'site_id'])

        # Adding model 'Process'
        db.create_table('objectapp_process', (
            ('gbobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['objectapp.Gbobject'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('objectapp', ['Process'])

        # Adding M2M table for field processtypes on 'Process'
        db.create_table('objectapp_process_processtypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False)),
            ('processtype', models.ForeignKey(orm['gstudio.processtype'], null=False))
        ))
        db.create_unique('objectapp_process_processtypes', ['process_id', 'processtype_id'])

        # Adding M2M table for field priorstate_attribute_set on 'Process'
        db.create_table('objectapp_process_priorstate_attribute_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False)),
            ('attribute', models.ForeignKey(orm['gstudio.attribute'], null=False))
        ))
        db.create_unique('objectapp_process_priorstate_attribute_set', ['process_id', 'attribute_id'])

        # Adding M2M table for field priorstate_relation_set on 'Process'
        db.create_table('objectapp_process_priorstate_relation_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False)),
            ('relation', models.ForeignKey(orm['gstudio.relation'], null=False))
        ))
        db.create_unique('objectapp_process_priorstate_relation_set', ['process_id', 'relation_id'])

        # Adding M2M table for field poststate_attribute_set on 'Process'
        db.create_table('objectapp_process_poststate_attribute_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False)),
            ('attribute', models.ForeignKey(orm['gstudio.attribute'], null=False))
        ))
        db.create_unique('objectapp_process_poststate_attribute_set', ['process_id', 'attribute_id'])

        # Adding M2M table for field poststate_relation_set on 'Process'
        db.create_table('objectapp_process_poststate_relation_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False)),
            ('relation', models.ForeignKey(orm['gstudio.relation'], null=False))
        ))
        db.create_unique('objectapp_process_poststate_relation_set', ['process_id', 'relation_id'])

        # Adding model 'System'
        db.create_table('objectapp_system', (
            ('gbobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['objectapp.Gbobject'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('objectapp', ['System'])

        # Adding M2M table for field systemtypes on 'System'
        db.create_table('objectapp_system_systemtypes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('systemtype', models.ForeignKey(orm['gstudio.systemtype'], null=False))
        ))
        db.create_unique('objectapp_system_systemtypes', ['system_id', 'systemtype_id'])

        # Adding M2M table for field gbobject_set on 'System'
        db.create_table('objectapp_system_gbobject_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('gbobject', models.ForeignKey(orm['objectapp.gbobject'], null=False))
        ))
        db.create_unique('objectapp_system_gbobject_set', ['system_id', 'gbobject_id'])

        # Adding M2M table for field relation_set on 'System'
        db.create_table('objectapp_system_relation_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('relation', models.ForeignKey(orm['gstudio.relation'], null=False))
        ))
        db.create_unique('objectapp_system_relation_set', ['system_id', 'relation_id'])

        # Adding M2M table for field attribute_set on 'System'
        db.create_table('objectapp_system_attribute_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('attribute', models.ForeignKey(orm['gstudio.attribute'], null=False))
        ))
        db.create_unique('objectapp_system_attribute_set', ['system_id', 'attribute_id'])

        # Adding M2M table for field process_set on 'System'
        db.create_table('objectapp_system_process_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('process', models.ForeignKey(orm['objectapp.process'], null=False))
        ))
        db.create_unique('objectapp_system_process_set', ['system_id', 'process_id'])

        # Adding M2M table for field system_set on 'System'
        db.create_table('objectapp_system_system_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_system', models.ForeignKey(orm['objectapp.system'], null=False)),
            ('to_system', models.ForeignKey(orm['objectapp.system'], null=False))
        ))
        db.create_unique('objectapp_system_system_set', ['from_system_id', 'to_system_id'])


    def backwards(self, orm):
        
        # Deleting model 'Gbobject'
        db.delete_table('objectapp_gbobject')

        # Removing M2M table for field prior_nodes on 'Gbobject'
        db.delete_table('objectapp_gbobject_prior_nodes')

        # Removing M2M table for field posterior_nodes on 'Gbobject'
        db.delete_table('objectapp_gbobject_posterior_nodes')

        # Removing M2M table for field objecttypes on 'Gbobject'
        db.delete_table('objectapp_gbobject_objecttypes')

        # Removing M2M table for field authors on 'Gbobject'
        db.delete_table('objectapp_gbobject_authors')

        # Removing M2M table for field sites on 'Gbobject'
        db.delete_table('objectapp_gbobject_sites')

        # Deleting model 'Process'
        db.delete_table('objectapp_process')

        # Removing M2M table for field processtypes on 'Process'
        db.delete_table('objectapp_process_processtypes')

        # Removing M2M table for field priorstate_attribute_set on 'Process'
        db.delete_table('objectapp_process_priorstate_attribute_set')

        # Removing M2M table for field priorstate_relation_set on 'Process'
        db.delete_table('objectapp_process_priorstate_relation_set')

        # Removing M2M table for field poststate_attribute_set on 'Process'
        db.delete_table('objectapp_process_poststate_attribute_set')

        # Removing M2M table for field poststate_relation_set on 'Process'
        db.delete_table('objectapp_process_poststate_relation_set')

        # Deleting model 'System'
        db.delete_table('objectapp_system')

        # Removing M2M table for field systemtypes on 'System'
        db.delete_table('objectapp_system_systemtypes')

        # Removing M2M table for field gbobject_set on 'System'
        db.delete_table('objectapp_system_gbobject_set')

        # Removing M2M table for field relation_set on 'System'
        db.delete_table('objectapp_system_relation_set')

        # Removing M2M table for field attribute_set on 'System'
        db.delete_table('objectapp_system_attribute_set')

        # Removing M2M table for field process_set on 'System'
        db.delete_table('objectapp_system_process_set')

        # Removing M2M table for field system_set on 'System'
        db.delete_table('objectapp_system_system_set')


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
        'gstudio.edge': {
            'Meta': {'object_name': 'Edge', '_ormbases': ['gstudio.NID']},
            'nid_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.NID']", 'unique': 'True', 'primary_key': 'True'})
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
        'objectapp.gbobject': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Gbobject', '_ormbases': ['gstudio.Node']},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'gbobjects'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'comment_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end_publication': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2042, 3, 15, 0, 0)'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gstudio.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'objecttypes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Nodetype']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pingback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'posterior_nodes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posterior_nodes_rel_+'", 'null': 'True', 'to': "orm['objectapp.Gbobject']"}),
            'prior_nodes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'prior_nodes_rel_+'", 'null': 'True', 'to': "orm['objectapp.Gbobject']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'gbobjects'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'start_publication': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'objectapp/gbobject_detail.html'", 'max_length': '250'})
        },
        'objectapp.process': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Process', '_ormbases': ['objectapp.Gbobject']},
            'gbobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['objectapp.Gbobject']", 'unique': 'True', 'primary_key': 'True'}),
            'poststate_attribute_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_post_state_attrset_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Attribute']"}),
            'poststate_relation_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_post_state_relset_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Relation']"}),
            'priorstate_attribute_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_prior_state_attrset_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Attribute']"}),
            'priorstate_relation_set': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_prior_state_relset_of'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Relation']"}),
            'processtypes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_processes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Processtype']"})
        },
        'objectapp.system': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'System', '_ormbases': ['objectapp.Gbobject']},
            'attribute_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_attribute_set_of'", 'blank': 'True', 'to': "orm['gstudio.Attribute']"}),
            'gbobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['objectapp.Gbobject']", 'unique': 'True', 'primary_key': 'True'}),
            'gbobject_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_gbobject_set_of'", 'blank': 'True', 'to': "orm['objectapp.Gbobject']"}),
            'process_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_process_set_of'", 'blank': 'True', 'to': "orm['objectapp.Process']"}),
            'relation_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_relation_set_of'", 'blank': 'True', 'to': "orm['gstudio.Relation']"}),
            'system_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'system_set_rel_+'", 'blank': 'True', 'to': "orm['objectapp.System']"}),
            'systemtypes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_systems'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['gstudio.Systemtype']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['objectapp']
