from flask_cors import CORS
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "http://10.233.10.136"}})

import api.views
