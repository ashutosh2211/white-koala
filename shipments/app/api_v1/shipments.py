__author__ = 'ashutosh.banerjee'
from flask import request, Response, jsonify
from . import api
from .. import db
from flask.views import MethodView
from data_transfer.shipment_dto import ShipmentDto
from ..models import Shipment
from ..decorators import json, paginate
from flask.ext.restful import reqparse
from mongoengine.fields import *

#import json


class ListView(MethodView):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('shipment_id', type = str, required=True,
                                   help = 'No shipment_id provided', location = 'json')
        self.reqparse.add_argument('creator_organisation', type = str, required=True,
                                   help = 'No creator_organisation provided', location = 'json')
        self.reqparse.add_argument('body', type = str, required=True,
                                   help = 'No body provided', location = 'json')
        self.reqparse.add_argument('metadata', type = dict, required=False,
                                   help = 'No metadata provided', location = 'json')
        super(ListView, self).__init__()

    @json
    def get(self):
        shipments = Shipment.objects.all()
        return shipments

    def post(self):
        # shipment =Shipment()
        # result = shipment.parse_input()
        result = {}
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                result[k] = v
        shipment = Shipment()
        shipment.import_data(result)
        shipment.save()
        return jsonify(shipment.export_data())
        # shipment = update_document(Shipment(),result)
        # shipment.save()
        # format = ShipmentDto([shipment])
        # return Response(x.__str__(), status=200, mimetype='application/json')

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
api.add_url_rule('/', view_func=ListView.as_view('list'))
api.add_url_rule('/abc', view_func=ListView.as_view('list1'))
# @api.route('/customers/', methods=['GET'])
# @json
# @paginate('customers')
# def get_customers():
#     return Customer.query
#
# @api.route('/customers/<int:id>', methods=['GET'])
# @json
# def get_customer(id):
#     return Customer.query.get_or_404(id)
#
# @api.route('/customers/', methods=['POST'])
# @json
# def new_customer():
#     customer = Customer()
#     customer.import_data(request.json)
#     db.session.add(customer)
#     db.session.commit()
#     return {}, 201, {'Location': customer.get_url()}
#
# @api.route('/customers/<int:id>', methods=['PUT'])
# @json
# def edit_customer(id):
#     customer = Customer.query.get_or_404(id)
#     customer.import_data(request.json)
#     db.session.add(customer)
#     db.session.commit()
#     return {}
