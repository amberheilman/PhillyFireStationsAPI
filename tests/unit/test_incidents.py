from concurrent.futures import Future
from datetime import datetime
import json
from mock import Mock, patch

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from handlers import incidents


class _BaseIncidentCollection(AsyncHTTPTestCase):
    expected_status_code = 200
    req_kwargs = {'path': '/incidents', 'method': 'GET'}
    results = [{'id': 1,
                'dispatched_at': datetime.now(),
                'type': 'House Fire',
                'alarms': 2,
                'location': (2.4, 3.4)}]

    def setUp(cls):
        super(_BaseIncidentCollection, cls).setUp()
        cls.configure()
        cls.execute()

    def get_app(cls):
        return Application([('/incidents', incidents.IncidentCollection)])

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
        cls.response = cls.fetch(**cls.req_kwargs)
        try:
            cls.json = json.loads(cls.response.body.decode('utf-8'))
        except (ValueError, AttributeError):
            pass

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


class TestIncidentCollectionMutipleResults(TestIncidentCollectionOneResult):
    results = [{'id': 1,
                'dispatched_at': datetime.now(),
                'type': 'House Fire',
                'alarms': 2,
                'location': (2.4, 3.4)},
                {'id': 2,
                'dispatched_at': datetime.now(),
                'type': 'Apartment Fire',
                'alarms': 2,
                'location': (2.2, 4.4)}]


class TestIncidentNoResults(_BaseIncidentCollection):
    expected_status_code = 204
    results = None


class TestIncidentCollectionMethodNotAllowed(_BaseIncidentCollection):
    expected_status_code = 405
    req_kwargs = {'path': '/incidents',
                  'method': 'POST',
                  'body': json.dumps({'incident_id': 1})}


class TestIncidentOptionsMethodHasAllowHeader(_BaseIncidentCollection):
    expected_status_code = 204
    req_kwargs = {'path': '/incidents',
                  'method': 'OPTIONS'}

    def test_returns_expected_header(self):
        self.assertEqual('GET', self.response.headers.pop('Allow'))

