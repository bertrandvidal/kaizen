import unittest
import json
import responses

from kaizen.api import ZenRequest, ChainingError


class ZenRequestTest(unittest.TestCase):

    def test_chaining_project_phase(self):
        request = ZenRequest("fake_key")
        self.assertRaises(ChainingError, request.phases)

    def test_paginate(self):
        params = ZenRequest("fake_key").paginate(2, 12).params
        self.assertListEqual(params.values(), [2,12])

    def test_where(self):
        params = ZenRequest("fake_key").where("color:green").params
        self.assertEqual(params, {"where": "color:green"})

    def test_with_enrichments(self):
        request = ZenRequest("fake_key").with_enrichments("metrics", "members")
        self.assertEqual(request.params, {"with": "metrics,members"})

    @responses.activate
    def test_phase_list_url(self):
        phase_data = {
            "id": 12,
            "name": "Phase",
            "description": "Contains stories",
            "index": 2
        }
        phase_url = "https://agilezen.com/api/v1/projects/12/phases/12"
        request = ZenRequest("fake_key").projects(12).phases(12)
        responses.add(responses.GET, phase_url, status=200,
                      content_type='application/json',
                      body=json.dumps(phase_data))
        request.send()


if __name__ == "__main__":
    unittest.main()
