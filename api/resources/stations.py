from flask.ext import restful
from flask_restful_swagger import swagger

from api.models import stations


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
        return {'hello': 'world'}
