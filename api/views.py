from api import api
from api.resources import stations
from api.resources import incidents

api.add_resource(stations.Stations, '/stations/')
api.add_resource(stations.Station, '/stations/<id>')
api.add_resource(incidents.Incidents, '/incidents/')
api.add_resource(incidents.Incident, '/incidents/<id>')
