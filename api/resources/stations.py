from collections import defaultdict
from flask.ext import restful
from flask_restful.utils import cors
import json
from flask import make_response
from flask import jsonify
import queries
import ast
from api.models import stations
from api.config import get_config


class Stations(restful.Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        with queries.Session('postgresql://fire_read:rad2sz4e@localhost/philly_fire') as session:
            results = session.query("SELECT  s.id,  s.address, s.city,  s.latitude, s.longitude, dt.runs FROM stations as s JOIN ( SELECT   station_id, SUM (runs) AS runs FROM truck_runs  GROUP BY station_id ) as dt ON s.id = dt.station_id")
            return self._transform(results)

    def _transform(self, result):
        response = []

        for row in result:
            entry = {
            "address": row['address'],
            "city": row['city'],
            "id": row['id'],
            "x": row['latitude'],
            "y": row['longitude'],
            "total_runs": row['runs']
            }
            response.append(entry)
	resp = make_response(json.dumps(response), 200)
	resp.headers.extend({'Content-Type': 'application/json'})
	return resp

class Station(restful.Resource):
    @cors.crossdomain(origin='*')
    def get(self, id):
        with queries.Session('postgresql://fire_read:rad2sz4e@localhost/philly_fire') as session:
            results = session.query("SELECT s.address, s.city, s.id, s.latitude, s.longitude, s.chief, s.service_area, dt.runs AS totalRuns, t.truck_id, t.type, t.runs FROM stations AS s JOIN trucks_with_types_and_runs AS t ON t.station_id = s.id JOIN ( SELECT station_id, SUM(runs) AS runs FROM truck_runs GROUP BY station_id) AS dt ON s.id = dt.station_id WHERE s.id='%s'" % id.upper()) 
            
	    resp = make_response(json.dumps(self._transform(results)), 200)
  	    resp.headers.extend({'Content-Type': 'application/json'})
	    return resp


    def _transform(self, result):
        response = []

        for row in result:
            areas = ast.literal_eval(row['service_area'])
            service_area = [] 
                 
            for x,y in areas:
                d = {
                    "x": x,
                    "y": y
                }
                print x, y;
                service_area.append(d) 

            entry = {
            "station_id": row['id'],
            "address": row['address'],
            "city": row['city'],
            "x": row['latitude'],
            "y": row['longitude'],
            "batallion_commander": row['chief'],
            "total_runs": row['totalruns'],
            "service_area": service_area,
            "trucks": {
                'id': row['truck_id'],
                'type': row['type'],
                'runs': row['runs']
            }
            };

            response.append(entry)
        return response
