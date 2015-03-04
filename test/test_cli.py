from kaizen.cli import ZenApi
import json
import responses
import unittest


class ZenApiTest(unittest.TestCase):

    @responses.activate
    def test_get_next_phase_id(self):
        api = ZenApi("fake_key")
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertEqual(api._get_next_phase_id("phase_name", 12), 42)

    @responses.activate
    def test_get_next_phase_id_unknow_phase(self):
        api = ZenApi("fake_key")
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertRaises(ValueError, api._get_next_phase_id, "unknown", 12)

    @responses.activate
    def test_get_next_phase_id_story_in_last_phase(self):
        api = ZenApi("fake_key")
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertRaises(ValueError, api._get_next_phase_id, "other_phase", 12)

