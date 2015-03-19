import ast
import logging
import queries
from tornado import web, gen
from tornado.web import RequestHandler

from configuration import config


class IncidentCollection(RequestHandler):

    def initialize(self):
        self.session = queries.TornadoSession(config.get('uri'))

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
        try:
            results = yield self.session.query("SELECT * FROM incidents")

            if not results:
                self.set_status(204)
                self.finish()

            results.free()
            incidents = self._transform(results)

        except (queries.DataError, queries.IntegrityError) as error:
            logging.exception('Error making query: %s', error)
            self.set_status(409)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(incidents)

    def _transform(self, results):
        response = []

        for row in results:
            # TODO: add try/except for invalid data
            row_loc = ast.literal_eval(row['location'])
            location = {'x': row_loc[0], 'y': row_loc[1]}
            entry = [{"incident_id": row['id'],
                      "dispatched_at": row['dispatched_at'].strftime(
                          "%Y-%m-%d %H:%M:%S"),
                      "type": row['type'],
                      "alarms": row['alarms'],
                      "location": location}]
        response.append(entry)

        return response


class IncidentEntry(IncidentCollection):

    def initialize(self):
        self.session = queries.TornadoSession(config.get('uri'))

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
    def get(self, incident_id):
        """Return a single incident
        """
        try:
            results = yield self.session.query(
                "SELECT * FROM incidents WHERE id='%s'" % incident_id.upper())

            if not results:
                self.set_status(204)
                self.finish()

            results.free()

        except (queries.DataError, queries.IntegrityError) as error:
            self.set_status(409)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(results.as_dict())
