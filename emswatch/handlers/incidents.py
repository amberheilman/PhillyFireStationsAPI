from datetime import datetime, timedelta
import json
import logging
import os

import psycopg2.extras
import queries
from tornado import web, gen

from . import _BaseHandler


logger = logging.getLogger(__name__)


class IncidentCollection(_BaseHandler):

    @gen.coroutine
    def get(self):
        """Return all incidents from yesterday.

        """
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        arg = psycopg2.extras.DateTimeTZRange(upper=now, lower=yesterday)
        try:
            results = yield self.call_proc('get_incidents_by_timerange', arg)
        except:
            self.set_status(500)
            self.finish()
            return

        if not results:
            return
        response = self._transform(results)
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish(response)

    def _transform(self, results):
        return results.to_dict()


class IncidentEntry(_BaseHandler):

    @gen.coroutine
    def get(self, incident_id):
        """Return a single incident
        """
        try:
            results = yield self.session.query(
                "SELECT * FROM incidents WHERE id='%s'" % incident_id.upper())
        except queries.DataError as error:
            logger.exception('Error making query: %s', error)
            self.set_status(400)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})
        except queries.IntegrityError as error:
            logger.exception('Error making query: %s', error)
            self.set_status(409)
            self.finish({'error':
                        {'description': error.pgerror.split('\n')[0][8:]}})

        if not results:
            results.free()
            self.set_status(204)
            self.finish()
            return

        results.free()
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish(results.as_dict())
