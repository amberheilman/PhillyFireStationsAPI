from api import api
from api.resources import stations
from api.resources import incidents

api.add_resource(stations.Stations, '/stations/', '/stations/<id>')
api.add_resource(incidents.Incidents, '/incidents/', '/incidents/<id>')
