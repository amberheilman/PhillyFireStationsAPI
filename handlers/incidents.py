import ast
import logging
import queries
from tornado import web, gen
from tornado.web import RequestHandler

# from api import config


class IncidentsCollection(RequestHandler):

    def initialize(self):
        self.session = queries.TornadoSession()

    @gen.coroutine
    def prepare(self):
        try:
            yield self.session.validate()
        except queries.OperationalError as error:
            logging.error('Error connecting to the database: %s', error)
            raise web.HTTPError(503)

    def options(self, *args, **kwargs):
        """Let the caller know what methods are supported

        :param list args: URI path arguments passed in by Tornado
        :param dict kwargs: URI path keyword arguments passed in by Tornado

        """
        self.set_header('Allow', ', '.join(['GET']))
        self.set_status(204)
        self.finish()

    @gen.coroutine
    def get(self):
        """Return all incidents
        """

        results = yield self.session.query("SELECT * FROM incidents")

        # No rows returned, send a 204 with a JSON
        if not results:
            self.set_status(204)
            self.finish()

        # Send back the row as a JSON object
        else:
            self.finish(results.as_dict())

        # Free the results and release the connection lock from session.query
        results.free()
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish()

    def _transform(self, results):
        response = []

        for row in results:
            # TODO: add try/except for invalid data
            row_loc = ast.literal_eval(row['location'])
            loc = {'x': row_loc[0], 'y': row_loc[1]}
            entry = [{
                "incident_id": row['id'],
                "dispatched_at": row['dispatched_at'].strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "type": row['type'],
                "alarms": row['alarms'],
                "location": loc}]
        response.append(entry)

        return response


class IncidentsEntry(IncidentsCollection):

    @gen.coroutine
    def get(self):
        """Return a single incident
        """

        results = yield self.session.query(
            "SELECT * FROM incidents WHERE id='%s'" % id.upper())

        # No rows returned, send a 204 with a JSON
        if not results:
            self.set_status(204)
            self.finish()

        # Send back the row as a JSON object
        else:
            self.finish(results.as_dict())

        # Free the results and release the connection lock from session.query
        results.free()
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish()
