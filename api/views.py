from api import api
from api.resources import stations

api.add_resource(stations.Stations, '/stations')
api.add_resource(stations.Stations, '/stations/<id>') 
api.add_resource(incidents.Incidents, '/incidents')
api.add_resource(incidents.Incidents, '/incidents/<id>')
