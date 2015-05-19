from datetime import datetime
import json

from . import _BaseAPITest


class TestIncidentCollectionOneResult(_BaseAPITest):

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




