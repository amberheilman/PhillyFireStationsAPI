from flask.ext import restful
from flask_restful_swagger import swagger

import queries
from api.config import get_config

class Incidents(restful.Resource):

    config = get_config()

    def get(self, id=None):
        return [
        {
        "incident_id": 1234,
        "responders": [
        {
            "id": "L02",
            "station_id": "E02",
            "arrived_at": "2014-01-01 00:00:00 -0500",
            "departed_at": "2014-01-01 02:00:00 -0500"
        },
        {
            "id": "E02",
            "station_id": "E02",
            "arrived_at": "2014-01-01 00:00:00 -0500",
            "departed_at": "2014-01-01 02:00:00 -0500"
        }
        ],
            "dispatched_at": "2014-01-01 00:00:00 -0500",
            "type": "House fire",
            "alarms": 4,
            "location": {
                "x": 2686263.115572676,
                "y": 280759.4062628746
            },
            "description": "House fire at the residence of... blah"
        }
        ]
