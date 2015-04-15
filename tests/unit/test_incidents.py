from concurrent.futures import Future
from datetime import datetime
import json
from mock import Mock, MagicMock, patch

from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test
from tornado.web import Application

from handlers import incidents

class _BaseIncidentCollection(AsyncHTTPTestCase):
    url = '/incidents'
    method = 'GET'
    expected_status_code = 200
    expected_response = {}
    results = [{'id': 1,
                'dispatched_at': datetime.now(),
                'type': 'House Fire',
                'alarms': 2,
                'location': (2.4, 3.4)}]
    def setUp(cls):
        super(_BaseIncidentCollection, cls).setUp()
        cls.configure()
        cls.execute()

    def configure(cls):
        pass

    def get_app(cls):
        return Application([('/incidents', incidents.IncidentCollection),
                            ('/incidents/<id>', incidents.IncidentEntry)])

    @patch('queries.TornadoSession')
    def execute(cls, session):
        cls.session = session.return_value

        future_is_valid = Future()
        future_is_valid.set_result(True)
        future_query = Future()
        future_query.set_result(cls.results)
        cls.session.validate.return_value = future_is_valid
        cls.session.query.return_value = future_query
        cls.session.query.free = Mock()


        cls.response = cls.fetch(cls.url, method=cls.method)
        if cls.response.body:
            cls.json = json.loads(cls.response.body.decode('utf-8'))

    def test_returns_expected_status_code(self):
        self.assertEqual(self.response.code, self.expected_status_code)

class TestIncidentCollectionOneResult(_BaseIncidentCollection):

    def test_response_is_bytes(self):
        self.assertIsInstance(self.response.body, bytes)

    def test_returns_incident_id(self):
        self.assertIn('incident_id', self.json)

    def test_returns_incident_dispatched_at_time(self):
        self.assertIn('dispatched_at', self.json)

    def test_returns_incident_type(self):
        self.assertIn('type', self.json)

    def test_returns_incident_alarms(self):
        self.assertIn('alarms', self.json)

    def test_returns_incident_location(self):
        self.assertIn('location', self.json)


class TestIncidentNoResults(_BaseIncidentCollection):
    results = None
    expected_status_code = 204


class TestIncidentCollectionMethodNotAllowed(_BaseIncidentCollection):
    method = 'POST'
    expected_status_code = 405


class TestIncidentHasOptions(_BaseIncidentCollection):
    method = 'OPTIONS'

    def test_returns_expected_header(self):
        self.assertIn('GET', self.response.headers.pop('Allow'))

