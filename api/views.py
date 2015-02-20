from api import api
from api.resources import stations

api.add_resource(stations.Stations, '/')
