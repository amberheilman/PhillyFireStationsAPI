from api import api
from api.resources import stations

api.add_resource(stations.Stations, '/stations/', '/stations/<id>')
#api.add_resource(incidents.Incidents, '/incidents', '/incidents/<id>')
