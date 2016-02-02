import logging
import queries
from tornado import gen

from . import _BaseHandler


logger = logging.getLogger(__name__)


class StationCollection(_BaseHandler):

    @gen.coroutine
    def get(self):
        try:
            results = yield self.call_proc('get_stations')
            return self._transform(results)

            if not results:
                self.set_status(204)
                self.finish()

            stations = self._transform(results)
            results.free()

        except (queries.DataError, queries.IntegrityError) as error:
            logger.exception('Error making query: %s', error)
            self.set_status(500)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})
        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(stations)

    def _transform(self, results):
        return results.as_dict()


class StationEntry(_BaseHandler):

    @gen.coroutine
    def get(self, station_id):
        try:
            results = self.session.query(
                'SELECT * from stations WHERE id=%s' % int(station_id))

            if not results:
                self.set_status(204)
                self.finish()

            stations = self._transform(results)
            results.free()

        except (queries.DataError, queries.IntegrityError) as error:
            logger.exception('Error making query: %s', error)
            self.set_status(500)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        else:
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish(stations)

    def _transform(self, result):
        return result.as_dict()
