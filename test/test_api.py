import unittest
import json
import responses

from kaizen.api import ApiRequest, ProjectRequest, ZenRequest


class ApiRequestTest(unittest.TestCase):

    @responses.activate
    def test_paginate(self):
        request = ApiRequest("fake_key").paginate(2, 12)
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?page=2&pageSize=12",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()

    @responses.activate
    def test_where(self):
        request = ApiRequest("fake_key").where("color:green")
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?where=color:green",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()

    @responses.activate
    def test_with_enrichments(self):
        request = ApiRequest("fake_key").with_enrichments("metrics", "members")
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/?with=metrics,members",
                      content_type="application/json", body="{}", status=200,
                      match_querystring=True)
        request.send()


class ZenRequestTest(unittest.TestCase):

    def test_projects_return_project_request(self):
        self.assertEqual(type(ZenRequest("fake_key").projects()),
                         ProjectRequest)

    def test_projects_sets_url(self):
        request = ZenRequest("fake_key").projects(12)
        self.assertIn("projects", request.url)
        self.assertIn("12", request.url)


class ProjectRequestTest(unittest.TestCase):

    @responses.activate
    def test_phase_list_url(self):
        phase_data = {
            "id": 12,
            "name": "Phase",
            "description": "Contains stories",
            "index": 2
        }
        phase_url = "https://agilezen.com/api/v1/projects/12/phases/12"
        request = ProjectRequest("fake_key", 12).phases(12)
        responses.add(responses.GET, phase_url, status=200,
                      content_type='application/json',
                      body=json.dumps(phase_data))
        request.send()

    @responses.activate
    def test_members_url(self):
        request = ProjectRequest("fake_key", 12).members(12)
        members_url = "https://agilezen.com/api/v1/projects/12/members/12"
        responses.add(responses.GET, members_url, status=200,
                      content_type="application/json", body="{}")
        request.send()

    def test_from_zen_request(self):
        zen_request = ZenRequest("fake_key")
        project_request = ProjectRequest.from_zen_request(zen_request)
        self.assertEqual(project_request.get_api_key(),
                         zen_request.get_api_key())


if __name__ == "__main__":
    unittest.main()
