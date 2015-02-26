__author__ = 'ashutosh.banerjee'
#!/usr/bin/env python
import os, sys
from app import create_app, db
from flask.ext.script import Manager, Server
#from app.models import User

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    # with app.app_context():
    #     db.create_all()
    #     # create a development user
    #     if User.query.get(1) is None:
    #         u = User(username='john')
    #         u.set_password('cat')
    #         db.session.add(u)
    #         db.session.commit()
    manager = Manager(app)

# Turn on debugger by default and reloader
    manager.add_command("runserver", Server(
        use_debugger = True,
        use_reloader = True,
        host = '127.0.0.1')
    )
    manager.run()
