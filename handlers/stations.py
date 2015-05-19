import ast
import logging
import os
import queries
from tornado import web, gen
from tornado.web import RequestHandler

PG_URI = os.environ.get('PG_URI')


class StationCollection(RequestHandler):

    def initialize(self):
        self.session = queries.TornadoSession(PG_URI)

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

        try:
            results = self.session.query(
                "SELECT  s.id,  s.address, s.city,  s.latitude, "
                "s.longitude, dt.runs FROM stations as s JOIN ("
                "SELECT station_id, SUM (runs) AS runs FROM truck_runs "
                "GROUP BY station_id ) as dt ON s.id = dt.station_id")
            return self._transform(results)

            if not results:
                self.set_status(204)
                self.finish()

            stations = self._transform(results)
            results.free()

        except (queries.DataError, queries.IntegrityError) as error:
            logging.exception('Error making query: %s', error)
            self.set_status(409)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(stations)

    def _transform(self, result):
        response = []

        for row in result:
            entry = {"address": row['address'],
                     "city": row['city'],
                     "id": row['id'],
                     "x": row['latitude'],
                     "y": row['longitude'],
                     "total_runs": row['runs']}
            response.append(entry)


class StationEntry(RequestHandler):

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
    def get(self, station_id):

        try:
            results = self.session.query(
                "SELECT s.address, s.city, s.id, s.latitude, s.longitude, "
                "s.chief, s.service_area, dt.runs AS totalRuns, t.truck_id, "
                "t.type, t.runs FROM stations AS s JOIN "
                "trucks_with_types_and_runs AS t ON t.station_id = s.id JOIN"
                "( SELECT station_id, SUM(runs) AS runs FROM truck_runs "
                "GROUP BY station_id) AS dt ON s.id = dt.station_id "
                "WHERE s.id='%s'" % station_id.upper())

            if not results:
                self.set_status(204)
                self.finish()

            stations = self._transform(results)
            results.free()

        except (queries.DataError, queries.IntegrityError) as error:
            logging.exception('Error making query: %s', error)
            self.set_status(409)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(stations)

    def _transform(self, result):
        response = []
        station_info = result[0]

        areas = ast.literal_eval(station_info['service_area'])
        service_area = []

        for x, y in areas:
            area = {'x': x, 'y': y}
            service_area.append(area)

        trucks = []
        for row in result:
            entry = {'id': row['truck_id'],
                     'type': row['type'],
                     'runs': row['runs']}

            trucks.append(entry)

        station_entry = {'station_id': station_info['id'],
                         'address': station_info['address'],
                         'city': station_info['city'],
                         'x': station_info['latitude'],
                         'y': station_info['longitude'],
                         'batallion_commander': station_info['chief'],
                         'total_runs': station_info['totalruns'],
                         'service_area': service_area,
                         'trucks': trucks}

        response.append(station_entry)
        return response
