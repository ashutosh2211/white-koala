import datetime
from flask import url_for
from flask.ext.restful import reqparse
import validictory

from mongoengine import *


class Shipment(Document):
    created_at = DateTimeField(default=datetime.datetime.now)
    shipment_id = StringField(max_length=255, required=True, unique=True)
    creator_organisation = StringField(max_length=255, required=True)
    promised_delivery_date = DateTimeField(default=datetime.datetime.now, required=True)
    metadata = DictField(default={})
    body = StringField(required=True)
    comments = ListField(EmbeddedDocumentField('Comment'))

# "promised_delivery_date" : {"type": "string", "format" : "date-time"},
    def validate_fields(self, data):
        schema = {  "type" : "object",
                    "properties" : {
                        "shipment_id": {"type":"string", "maxlength" : "16"},
                        "creator_organisation" : {"type" : "string"},
                        "metadata" : { "type" : "object",
                                       "properties" : {"weight" : {"type" : "string"}}},
                        "body" : {"type" : "string"}
                    }
        }
        validictory.validate(data, schema)

    def get_absolute_url(self):
        return url_for('post', kwargs={"shipment_id": self.shipment_id})

    def __unicode__(self):
        return self.shipment_id

    def __repr__(self):
        return self.shipment_id

    def export_data(self):
        return {
            'shipment_id': self.shipment_id,
            'creator_organisation': self.creator_organisation,
            #'body': url_for('api.get_customer_orders', id=self.id,
            #                      _external=True)
        }

    def import_data(self, data):
        try:
            self.shipment_id = data['shipment_id']
            self.creator_organisation = data['creator_organisation']
            self.body = data['body']
            self.metadata = data['metadata']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }


class Comment(EmbeddedDocument):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    body = StringField(verbose_name="Comment", required=True)
    author = StringField(verbose_name="Name", max_length=255, required=True)