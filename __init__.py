__author__ = 'ashutosh.banerjee'
# from flask import Flask
# from mongoengine import connect
# from flask.ext.restful import Api, Resource
#
#
# db = connect('entities', host='localhost', port=27017)
#
# app = Flask(__name__)
# api = Api(app)
#
# def register_blueprints(app):
#     # Prevents circular imports
#     from delmart.views import shipments
#     app.register_blueprint(shipments)
#
# register_blueprints(app)
# # app.json_encoder = CustomJSONEncoder
# if __name__ == '__main__':
#     app.run()