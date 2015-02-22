from flask.ext import restful
import json
from flask import make_response
from flask_restful_swagger import swagger
from datetime import datetime
import queries
from api.config import get_config
from flask_restful.utils import cors
from flask.json import jsonify
from collections import defaultdict
import ast

class Incidents(restful.Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        with queries.Session('postgresql://fire_read:rad2sz4e@localhost/philly_fire') as session:
            results = session.query("SELECT * FROM incidents")
	    resp = make_response(json.dumps(self._transform(results)), 200)
	    resp.headers.extend({'Content-Type': 'application/json'})
	    return resp

    def _transform(self, results):
        response = []

	for row in results:
            row_loc = ast.literal_eval(row['location'])
            loc = {'x': row_loc[0], 'y': row_loc[1]}            
	    entry = [
    	{
        "incident_id": row['id'],
        "dispatched_at": row['dispatched_at'].strftime("%Y-%m-%d %H:%M:%S"),
        "type": row['type'],
        "alarms": row['alarms'],
        "location": loc,
    	}
	]
            response.append(entry)
                
        return response       


class Incident(restful.Resource):
    @cors.crossdomain(origin='*')
    def get(self, id):
        with queries.Session('postgresql://fire_read:rad2sz4e@localhost/philly_fire') as session:
            results = session.query("SELECT * FROM incidents WHERE id='%s'" % id.upper())
	    resp = make_response(json.dumps(self._transform(results)), 200)
	    resp.headers.extend({'Content-Type': 'application/json'})
	    return resp

    def _transform(self, results):
        response = []

	for row in results:
            row_loc = ast.literal_eval(row['location'])
            loc = {'x': row_loc[0], 'y': row_loc[1]}            
	    entry = [
    	{
        "incident_id": row['id'],
        "dispatched_at": row['dispatched_at'].strftime("%Y-%m-%d %H:%M:%S"),
        "type": row['type'],
        "alarms": row['alarms'],
        "location": loc,
    	}
	]
            response.append(entry)
        return response
    
