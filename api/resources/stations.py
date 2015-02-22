from flask.ext import restful
from flask_restful_swagger import swagger
import queries

from api.models import stations
from api.config import get_config


class Stations(restful.Resource):
    config = get_config()

    def get(self):
        with queries.Session('postgresql://halimaolapade@localhost/philly_fire') as session:
            results = session.query("SELECT id, latitude, longitude FROM stations")
            return results.items()

class Station(restful.Resource):
    def get(self, id):
        with queries.Session('postgresql://halimaolapade@localhost/philly_fire') as session:
            results = session.query("SELECT * FROM stations WHERE id='%s'" % id.upper())
            return results.items();
