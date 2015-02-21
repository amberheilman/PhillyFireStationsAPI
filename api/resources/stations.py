from flask.ext import restful
from flask_restful_swagger import swagger

from api.models import stations
#import configpaser


class Stations(restful.Resource):

    @swagger.operation(
        notes='some really good notes',
        responseClass=stations.__name__,
        nickname='upload',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object.",
              "required": True,
              "allowMultiple": False,
              "dataType": stations.__name__,
              "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created."
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def get(self):
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
