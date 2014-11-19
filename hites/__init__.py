import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


active_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(active_dir, 'templates')
static_dir = os.path.join(active_dir, 'static')
app = Flask(
    'hites.org',
    template_folder=templates_dir,
    static_folder=static_dir
)
if 'WSGI_ENV' in os.environ and os.environ['WSGI_ENV'] == 'production':
    db_config = {
        'user': 'hites_prod:Pr0dHit3s',
        'host': 'mysql.hites.org',
        'db': 'woodworking_calendar'
    }
else:
    db_config = {
        'user': 'root:password',
        'host': 'db',
        'db': 'woodworking_calendar'
    }
db_uri = 'mysql://%(user)s@%(host)s/%(db)s' % db_config
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


import hites.views
