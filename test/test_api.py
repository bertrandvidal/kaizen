import unittest

from kaizen.api import ZenRequest, ChainingError

class ZenRequestTest(unittest.TestCase):

    def test_chaining_project_phase(self):
        request = ZenRequest("fake_key")
        self.assertRaises(ChainingError, request.phases)


if __name__ == "__main__":
    unittest.main()
