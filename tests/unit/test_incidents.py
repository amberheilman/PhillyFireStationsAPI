import json
import mock
from mock import patch

from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test
from tornado.web import Application

from handlers import incidents


class TestIncidentCollection(AsyncHTTPTestCase):
    url = '/incidents/'
    expected_status_code = 200
    method = 'GET'

    def setUp(self):
        super(TestIncidentCollection, self).setUp()
        self.configure()
        self.execute()

    def configure(self):
        pass

    def get_app(self):
        return Application([('/incidents', incidents.IncidentCollection),
                            ('/incidents/<id>', incidents.IncidentEntry)])

    @patch('queries.TornadoSession', return_value='{}')
    def execute(self, session):
        self.session = session = mock.Mock()
        self.response = self.fetch(self.url, method=self.method)

    def tearDown(self):
        pass

#    def test_response_is_json(self):
#        self.assertIsInstance(self.response.body.json(), dict)
#
    def test_returns_expected_status_code(self):
        self.assertEqual(self.response.code, self.expected_status_code)

#    def test_returns_expected_response(self):
#        self.assertEqual(self.response.json, self.expected_response)
#
#
#class TestIncidentNoResults(TestIncidentCollection):
#    expected_status_code = 201
#
#
#class TestIncidentMethodNotFound(TestIncidentCollection):
#    expected_status_code = 405
#
#
#class TestIncidentHasOptions(TestIncidentCollection):
#    method = 'OPTIONS'
#    expected_response_header = 'Allow: GET'
#
#    def test_returns_get_method_as_option(self):
#        self.assertEqual(self.response.header.get('Allow'),
#                         self.expected_response_header)
#
#
#class TestReturnsExpectedIncident(TestIncidentCollection):
#    expected_response_body = {}
#
