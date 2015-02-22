from flask.ext import restful
from flask_restful_swagger import swagger
import queries

from api.models import stations
from api.config import get_config


class Stations(restful.Resource):

    config = get_config()

    def get(self, id=None):
#	uri = queries.uri(user=config.get('database_user'))
#	with queries.Session(uri) as session:
#	    for row in session.query('select * from fire.stations'):
#		return row
#

	if id:
	    return {
    "station_id": "E02",
    "address": "2426 N 2ND ST",
    "city": "Philadelphia",
    "x": 2700894.6385047585,
    "y": 249141.22953005135,
    "radio_band": "S",
    "batallion_commander": None,
    "total_runs": 7607,
    "last_updated": "2015-01-01 00:00:00 -0500",
    "service_area": [
        {
            "x": 2686263.1155726761,
            "y": 280759.4062628746
        },
        {
            "x": 2686627.6466693729,
            "y": 280521.75548185408
        }
    ],
    "trucks": [
        {
            "id": "E02",
            "type": "Engine",
            "runs": 453
        },
        {
            "id": "L02",
            "type": "Ladder",
            "runs": 1234
        }
    ]
}


        return [
    {
        "station_id": "E02",
        "x": 2700894.6385047585,
        "y": 249141.22953005135
    },
    {
        "station_id": "E03",
        "x": 2700894.6385047585,
        "y": 249141.22953005135
    }
]

