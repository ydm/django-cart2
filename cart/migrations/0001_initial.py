# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cart'
        db.create_table(u'cart_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cart', ['Cart'])

        # Adding model 'Item'
        db.create_table(u'cart_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('_meta', self.gf('django.db.models.fields.TextField')(default=u'{}')),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'cart', ['Item'])

        # Adding unique constraint on 'Item', fields ['cart', 'content_type', 'object_id']
        db.create_unique(u'cart_item', ['cart_id', 'content_type_id', 'object_id'])

        # Adding model 'TestProduct'
        db.create_table(u'cart_testproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal(u'cart', ['TestProduct'])


    def backwards(self, orm):
        # Removing unique constraint on 'Item', fields ['cart', 'content_type', 'object_id']
        db.delete_unique(u'cart_item', ['cart_id', 'content_type_id', 'object_id'])

        # Deleting model 'Cart'
        db.delete_table(u'cart_cart')

        # Deleting model 'Item'
        db.delete_table(u'cart_item')

        # Deleting model 'TestProduct'
        db.delete_table(u'cart_testproduct')


    models = {
        u'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cart.item': {
            'Meta': {'unique_together': "((u'cart', u'content_type', u'object_id'),)", 'object_name': 'Item'},
            '_meta': ('django.db.models.fields.TextField', [], {'default': "u'{}'"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Cart']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'cart.testproduct': {
            'Meta': {'object_name': 'TestProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cart']