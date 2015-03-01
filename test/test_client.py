import json
import requests
import responses
import unittest

from kaizen.client import ApiClient
from kaizen.request import Request, VERBS


class ApiClientTest(unittest.TestCase):

    def setUp(self):
        self._client = ApiClient("fake_api_key")

    def test_get_url(self):
        full_url = "https://agilezen.com/api/v1/fake_url"
        self.assertEqual(full_url, self._client._get_url("/fake_url"))
        self.assertEqual(full_url, self._client._get_url("fake_url"))

    @responses.activate
    def test_issue_request(self):
        items = {"items": [1, 2]}
        params = {"k": "v"}
        request = Request().update_url("fake_url").update_params({"k":"v"})\
                           .update_verb(VERBS.GET)
        responses.add(responses.GET, "https://agilezen.com/api/v1/fake_url?k=v",
                      match_querystring=True, body=json.dumps(items),
                      status=200, content_type="application/json")
        self.assertEquals(self._client.send_request(request),
                          items)

    @responses.activate
    def test_request_raises(self):
        request = Request().update_url("fake_url").update_verb(VERBS.GET)
        responses.add(responses.GET, "https://agilezen.com/api/v1/fake_url",
                      status=404, content_type='application/json')
        self.assertRaises(requests.HTTPError, self._client.send_request,
                          request)

if __name__ == "__main__":
    unittest.main()
