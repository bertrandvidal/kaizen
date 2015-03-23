from kaizen.cli import ZenApi, get_config, KaizenConfigError
import json
import os
import responses
import unittest


CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           "config_test.yaml")


class ZenApiTest(unittest.TestCase):

    @responses.activate
    def test_get_next_phase_id(self):
        api = ZenApi(CONFIG_PATH)
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertEqual(api._get_next_phase_id("phase_name", 12), 42)

    @responses.activate
    def test_get_next_phase_id_unknow_phase(self):
        api = ZenApi(CONFIG_PATH)
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertRaises(ValueError, api._get_next_phase_id, "unknown", 12)

    @responses.activate
    def test_get_next_phase_id_story_in_last_phase(self):
        api = ZenApi(CONFIG_PATH)
        phases = {"items": [{"id": 1, "name": "phase_name"},
                            {"id": 42, "name": "other_phase"}]}
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/?page=1&pageSize=100",
                      content_type="application/json", status=200,
                      body=json.dumps(phases), match_querystring=True)
        self.assertRaises(ValueError, api._get_next_phase_id, "other_phase", 12)


class ConfigTest(unittest.TestCase):

    def test_get_config_loads_yaml(self):
        self.assertEqual(get_config(CONFIG_PATH), {'api_key': 'api_key',
                                                   'done_phase': 'Archive',
                                                   'project_id': 12,
                                                   'todo_phase': 'Ready',
                                                   'user_name': 'username',
                                                   'working_phase': 'Working'})

    def test_get_config_raises_on_non_existent_file(self):
        self.assertRaises(KaizenConfigError, get_config, "unknown")

    def test_get_config_raises_on_non_yaml_file(self):
        malformed_file = os.path.abspath(__file__)
        self.assertRaises(KaizenConfigError, get_config, malformed_file)

