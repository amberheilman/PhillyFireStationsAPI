from concurrent.futures import Future
from datetime import datetime
import json
from mock import Mock, patch

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from handlers import incidents, stations


class _BaseAPITest(AsyncHTTPTestCase):
    expected_status_code = 200
    req_kwargs = [{'path': '/incidents', 'method': 'GET'}]
    results = [{'id': 1,
                'dispatched_at': datetime.now(),
                'type': 'House Fire',
                'alarms': 2,
                'location': (2.4, 3.4)}]
    responses = frozenset()

    def setUp(cls):
        super(_BaseAPITest, cls).setUp()
        cls.configure()
        cls.execute()

    def get_app(cls):
        return Application([('/incidents', incidents.IncidentCollection),
                           ('/incidents/<id>', incidents.IncidentEntry),
                           ('/stations', stations.StationCollection),
                           ('/stations/<id>', stations.StationEntry)])

    @classmethod
    def configure(cls):
        cls.future_is_valid = cls.future_query = Future()
        cls.future_is_valid.set_result(True)
        cls.future_query.set_result(cls.results)

    @patch('queries.TornadoSession')
    def execute(cls, session):
        cls.session = session.return_value
        cls.session.validate.return_value = cls.future_is_valid
        cls.session.query.return_value = cls.future_query
        for request in req_kwargs:
            responses.add(cls.fetch(**cls.req_kwargs))

        try:
            cls.json = json.loads(cls.response.body.decode('utf-8'))
        except (ValueError, AttributeError):
            pass

    def test_returns_expected_status_code(self):
        self.assertEqual(self.response.code, self.expected_status_code)


    def test_returns_204_when_no_results(_BaseAPITest):
        expected_status_code = 204
        results = None

    def test_returns_405_when_http_method_not_allowed(_BaseAPITest):
        expected_status_code = 405
        req_kwargs = {'path': '/incidents',
                      'method': 'POST',
                      'body': json.dumps({'incident_id': 1})}


#class TestIncidentCollectionOptionsMethodHasAllowHeader(_BaseAPITest):
#    expected_status_code = 204
#    req_kwargs = {'path': '/incidents',
#                  'method': 'OPTIONS'}
#
#    def test_returns_expected_header(self):
#        self.assertEqual('GET', self.response.headers.pop('Allow'))
