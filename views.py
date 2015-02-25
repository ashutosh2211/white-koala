__author__ = 'ashutosh.banerjee'
from flask import Blueprint, request, redirect, render_template, url_for, jsonify, Response
from flask.views import MethodView
from delmart.models import Shipment, Comment
from data_transfer.shipment_dto import ShipmentDto
from mongoengine.fields import *
from flask.ext.restful import reqparse

from flask import make_response

import json
from bson.json_util import dumps
from bson import json_util
from flask.json import JSONEncoder
import calendar
from datetime import datetime

shipments = Blueprint('shipments', __name__)

class ListView(MethodView):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('shipment_id', type = str, required=True,
                                   help = 'No shipment_id provided', location = 'json')
        self.reqparse.add_argument('creator_organisation', type = str, required=True,
                                   help = 'No creator_organisation provided', location = 'json')
        self.reqparse.add_argument('body', type = str, required=True,
                                   help = 'No body provided', location = 'json')
        super(ListView, self).__init__()

    def get(self):
        shipments = Shipment.objects.all()
        format1 = ShipmentDto(shipments)
        return json.dumps(format1.format())
        # return shipments.to_json()
        # return dumps(list(shipments))
        # return jsonify({"shipments":shipments})

    def post(self):
        # shipment =Shipment()
        # result = shipment.parse_input()
        result = {}
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                result[k] = v

        shipment = update_document(Shipment(),result)
        shipment.save()
        format = ShipmentDto([shipment])
        return Response(json.dumps(format.format()), status=200, mimetype='application/json')
        # return jsonify( { 'task': shipment } )
        # a= {}
        # a['shipment_id'] = "1234"
        # a['body'] = '16254'
        # a['creator_organisation'] = request.json.get('creator_organisation')
        # shipment = update_document(Shipment(),a)
        # # shipment.creator_organisation = request.json.get('creator_organisation')
        # # shipment.body = request.json.get('body')
        # shipment.save()
        # return Response(shipment, status=200, mimetype='application/json')

class DetailView(MethodView):

    def get(self, shipment_id):
        shipments = Shipment.objects.get_or_404(shipment_id=shipment_id)
        return shipments


def field_value(field, value):
  '''
  Converts a supplied value to the type required by the field.
  If the field requires a EmbeddedDocument the EmbeddedDocument
  is created and updated using the supplied data.
  '''
  if field.__class__ in (ListField, SortedListField):
    # return a list of the field values
    return [
      field_value(field.field, item)
      for item in value]

  elif field.__class__ in (
    EmbeddedDocumentField,
    GenericEmbeddedDocumentField,
    ReferenceField,
    GenericReferenceField):

    embedded_doc = field.document_type()
    update_document(embedded_doc, value)
    return embedded_doc
  else:
    return value


def update_document(doc, data):
  ''' Update an document to match the supplied dictionary.
  '''
  for key, value in data.iteritems():

    if hasattr(doc, key):
        value = field_value(doc._fields[key], value)
        setattr(doc, key, value)
    else:
        # handle invalid key
        pass

  return doc

shipments.add_url_rule('/', view_func=ListView.as_view('list'))
shipments.add_url_rule('/<shipment_id>/', view_func=DetailView.as_view('detail'))