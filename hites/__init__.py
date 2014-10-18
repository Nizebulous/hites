import os
from flask import Flask


active_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(active_dir, 'templates')
static_dir = os.path.join(active_dir, 'static')
app = Flask(
    'hites.org',
    template_folder=templates_dir,
    static_folder=static_dir
)


import hites.views
