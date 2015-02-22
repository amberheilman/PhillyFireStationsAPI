from flask.ext import restful
from flask_restful_swagger import swagger

import queries
from api.config import get_config

class Incidents(restful.Resource):
    def get(self):
        with queries.Session('postgresql://halimaolapade@localhost/philly_fire') as session:
            results = session.query("SELECT * FROM incidents")
            return results.items();

class Incident(restful.Resource):
    def get(self, id):
        with queries.Session('postgresql://halimaolapade@localhost/philly_fire') as session:
            results = session.query("SELECT * FROM incidents WHERE id='%s'" % id.upper())
            return results.items();

