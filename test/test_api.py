import unittest
import json
import responses

from kaizen.api import ZenRequest, ChainingError


class ZenRequestTest(unittest.TestCase):

    def test_chaining_project_phase(self):
        request = ZenRequest("fake_key")
        self.assertRaises(ChainingError, request.phases)

    @responses.activate
    def test_paginate(self):
        request = ZenRequest("fake_key").paginate(2, 12)
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?page=2&pageSize=12",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()

    @responses.activate
    def test_where(self):
        request = ZenRequest("fake_key").where("color:green")
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?where=color:green",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()

    @responses.activate
    def test_with_enrichments(self):
        request = ZenRequest("fake_key").with_enrichments("metrics", "members")
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?with=metrics,members",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()

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

    def test_members_raises_chaining_error(self):
        request = ZenRequest("fake_key")
        self.assertRaises(ChainingError, request.members)

    @responses.activate
    def test_members_url(self):
        request = ZenRequest("fake_key").projects(12).members(12)
        members_url = "https://agilezen.com/api/v1/projects/12/members/12"
        responses.add(responses.GET, members_url, status=200,
                      content_type="application/json", body="{}")
        request.send()



if __name__ == "__main__":
    unittest.main()
