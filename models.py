import datetime
from flask import url_for
from mongoengine import *


class Shipment(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    shipment_id = StringField(max_length=255, required=True, unique=True)
    creator_organisation = StringField(max_length=255, required=True)
    body = StringField(required=True)
    comments = ListField(EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"shipment_id": self.shipment_id})

    def __unicode__(self):
        return self.shipment_id

    def __repr__(self):
        return self.shipment_id

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }


class Comment(EmbeddedDocument):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    body = StringField(verbose_name="Comment", required=True)
    author = StringField(verbose_name="Name", max_length=255, required=True)