import unittest

from kaizen.request import Verbs, Request


class VerbsTest(unittest.TestCase):

    def setUp(self):
        self._verbs = Verbs()

    def testIn(self):
        self.assertIn("GET", self._verbs)
        self.assertIn("POST", self._verbs)
        self.assertIn("PUT", self._verbs)
        self.assertIn("DELETE", self._verbs)

    def testNotIn(self):
        self.assertNotIn("NoWay", self._verbs)
        self.assertNotIn("OPTIONS", self._verbs)
        self.assertNotIn("HEAD", self._verbs)


class RequestTest(unittest.TestCase):

    def setUp(self):
        self._request = Request()

    def testSetVerb(self):
        def assign_verb(new_verb):
            """To make it possible to use assertRaises."""
            self._request.verb = new_verb
        self.assertRaises(ValueError, assign_verb, "Nop!")

    def testCallChaining(self):
        post_request = self._request.update_verb("POST").update_url("/call_me")\
            .update_params({"name": "popo"}).update_data({"text": "cool beans"})
        self.assertEquals(post_request, self._request)
        self.assertEquals(post_request.verb, "POST")
        self.assertEquals(post_request.url, "/call_me")
        self.assertDictEqual(post_request.params, {"name": "popo"})
        self.assertDictEqual(post_request.data, {"text": "cool beans"})

