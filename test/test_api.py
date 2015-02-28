import unittest

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
        self.assertEquals(params, {"where": "color:green"})

    def test_with_enrichments(self):
        request = ZenRequest("fake_key").with_enrichments("metrics", "members")
        self.assertEquals(request.params, {"with": "metrics,members"})


if __name__ == "__main__":
    unittest.main()
