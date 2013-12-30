# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Item._meta'
        db.delete_column(u'cart_item', '_meta')

        # Adding field 'Item.metafld'
        db.add_column(u'cart_item', 'metafld',
                      self.gf('django.db.models.fields.TextField')(default=u'{}'),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Item._meta'
        db.add_column(u'cart_item', '_meta',
                      self.gf('django.db.models.fields.TextField')(default=u'{}'),
                      keep_default=False)

        # Deleting field 'Item.metafld'
        db.delete_column(u'cart_item', 'metafld')


    models = {
        u'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cart.item': {
            'Meta': {'unique_together': "((u'cart', u'content_type', u'object_id'),)", 'object_name': 'Item'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Cart']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metafld': ('django.db.models.fields.TextField', [], {'default': "u'{}'"}),
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