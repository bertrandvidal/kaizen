import unittest
import json
import responses

from kaizen.api import (ApiRequest, ProjectRequest, ZenRequest, PhaseRequest,
                        StoryRequest)
from kaizen.request import VERBS


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
        request = ZenRequest("fake_key").projects(12).phases(12)
        responses.add(responses.GET, phase_url, status=200,
                      content_type='application/json',
                      body=json.dumps(phase_data))
        request.send()

    @responses.activate
    def test_members_url(self):
        request = ZenRequest("fake_key").projects(12).members(12)
        members_url = "https://agilezen.com/api/v1/projects/12/members/12"
        responses.add(responses.GET, members_url, status=200,
                      content_type="application/json", body="{}")
        request.send()

    def test_from_zen_request(self):
        zen_request = ZenRequest("fake_key").update_url("/fake_url")\
                                            .update_params({"k": "v"})\
                                            .update_verb(VERBS.POST)\
                                            .update_data({"x": "y"})
        project_request = ProjectRequest.from_zen_request(zen_request)
        self.assertEqual(project_request.get_api_key(),
                         zen_request.get_api_key())
        self.assertEqual(project_request.url, "/fake_url/projects/")
        self.assertEqual(project_request.verb, VERBS.POST)
        self.assertEqual(project_request.params, {"k": "v"})
        self.assertEqual(project_request.data, {"x": "y"})

    @responses.activate
    def test_update_project(self):
        body = {"name": "name", "description": "description",
                "details": "details", "owner": 1}
        project = ZenRequest("fake_key").projects(12).update("name",
                                                             "description",
                                                             "details", 1)
        responses.add(responses.PUT,
                      "https://agilezen.com/api/v1/projects/12",
                      content_type="application/json", status=200,
                      body=json.dumps(body))
        project.send()


class PhaseRequestTest(unittest.TestCase):

    def test_from_project_request(self):
        zen_request = ZenRequest("fake_key").update_url("/fake_url")\
                                            .update_params({"k": "v"})\
                                            .update_verb(VERBS.POST)\
                                            .update_data({"x": "y"})
        project_request = ProjectRequest.from_zen_request(zen_request, 12)
        phase_request = PhaseRequest.from_project_request(project_request)
        self.assertEqual(phase_request.get_api_key(),
                         zen_request.get_api_key())
        self.assertEqual(phase_request.url, "/fake_url/projects/12/phases/")
        self.assertEqual(phase_request.verb, VERBS.POST)
        self.assertEqual(phase_request.params, {"k": "v"})
        self.assertEqual(phase_request.data, {"x": "y"})

    @responses.activate
    def test_list_phase(self):
        phase_request = ZenRequest("fake_key").projects(12).phases()
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/",
                      content_type="application/json", status=200, body="{}")
        phase_request.send()

    @responses.activate
    def test_add_phase(self):
        phase_request = ZenRequest("fake_key").projects(12).phases()
        add_request = phase_request.add("name", "description", 1, 12)
        responses.add(responses.POST,
                      "https://agilezen.com/api/v1/projects/12/phases/",
                      content_type="application/json", status=200, body="{}")
        add_request.send()

    @responses.activate
    def test_update_phase(self):
        phase_request = ZenRequest("fake_key").projects(12).phases()
        update_request = phase_request.update("name", "description", 1, 12)
        responses.add(responses.PUT,
                      "https://agilezen.com/api/v1/projects/12/phases/",
                      content_type="application/json", status=200, body="{}")
        update_request.send()

    @responses.activate
    def test_stories_list(self):
        phase_request = ZenRequest("fake_url").projects(12).phases(12)
        stories = phase_request.stories()
        responses.add(responses.GET,
                      "https://agilezen.com/api/v1/projects/12/phases/12/stories",
                      content_type="application/json", status=200, body="{}")
        stories.send()


class StoryRequestTest(unittest.TestCase):

    def test_from_project_request(self):
        zen_request = ZenRequest("fake_key").update_url("/fake_url")\
                                            .update_params({"k": "v"})\
                                            .update_verb(VERBS.POST)\
                                            .update_data({"x": "y"})
        project_request = ProjectRequest.from_zen_request(zen_request, 12)
        story_request = StoryRequest.from_project_request(project_request)
        self.assertEqual(story_request.get_api_key(),
                         zen_request.get_api_key())
        self.assertEqual(story_request.url, "/fake_url/projects/12/stories/")
        self.assertEqual(story_request.verb, VERBS.POST)
        self.assertEqual(story_request.params, {"k": "v"})
        self.assertEqual(story_request.data, {"x": "y"})

    def test_add_data(self):
        story_request = ZenRequest("fake_key").projects(12).stories()
        add_request = story_request.add("New story", owner=12)
        self.assertEqual({"text": "New story", "owner": 12}, add_request.data)

    @responses.activate
    def test_add_request(self):
        story_request = ZenRequest("fake_key").projects(12).stories()
        responses.add(responses.POST,
                      "https://agilezen.com/api/v1/projects/12/stories/",
                      content_type="application/json", status=200, body="{}")
        story_request.add("New story", details="More on that later")

    @responses.activate
    def test_update_request(self):
        story_request = ZenRequest("fake_key").projects(12).stories()
        responses.add(responses.PUT,
                      "https://agilezen.com/api/v1/projects/12/stories/",
                      content_type="application/json", status=200, body="{}")
        story_request.update(status="blocked", blocked_reason="Why not")


if __name__ == "__main__":
    unittest.main()
