import json
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from handlers import stations, incidents


class _BaseAppTest(AsyncHTTPTestCase):

    @classmethod
    def setUpClass(cls):
        cls.configure()
        cls.get_app()
        cls.execute()

    @classmethod
    def configure(cls):
        pass

    def get_app(self):
        return Application([
            ('/stations/', stations.StationCollection),
            ('/stations/<id>', stations.StationEntry),
            ('/incidents/', incidents.IncidentCollection),
            ('/incidents/<id>', incidents.IncidentEntry)])

    @classmethod
    def execute(cls):
        cls.response = cls.fetch(cls.get_url(cls.url), method=cls.method)


class TestStationCollection(_BaseAppTest):
    url = '/stations/'
    status_code = 200
    method = 'GET'

    def response_is_json(self):
        self.assertIsInstance(self.response, json)

    def returns_expected_status_code(self):
        self.assertEqual(self.response.status_code, self.status_code)


class TestStationNoResults(TestStationCollection):
    status_code = 201


