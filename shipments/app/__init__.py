__author__ = 'ashutosh.banerjee'

from flask import Flask, g
import os
from mongoengine import connect

db = connect('entities', host='localhost', port=27017)

# db = connect(
#                 name='',
#                 username='',
#                 password='',
#                 host='mongodb://localhost/entities'
#            )

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    db = connect('entities', host='localhost', port=27017)
    # initialize extensions
    # db.init_app(app)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    # # authentication token route
    # from .auth import auth
    # @app.route('/get-auth-token')
    # @auth.login_required
    # @rate_limit(1, 600)  # one call per 10 minute period
    # @no_cache
    # @json
    # def get_auth_token():
    #     return {'token': g.user.generate_auth_token()}

    return app
