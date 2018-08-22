import responses
import unittest
from urllib.parse import parse_qs
import json

from medium import Client


class TestIsaac(unittest.TestCase):

    def setUp(self):
        self.client = Client(access_token="isaac-token")

    def _mock_endpoint(self, method, path, callback, is_json=True):
        def wrapped_callback(req):
            if is_json:
                self.assertEqual(req.headers["Authorization"],
                                 "Bearer isaac-token")
            if req.body is not None:
                body = json.loads(req.body) if is_json else parse_qs(req.body)
            else:
                body = None
            status, data = callback(body)
            return status, {}, json.dumps(data)

        response_method = responses.GET if method == "GET" else responses.POST
        url = "https://api.medium.com" + path
        content_type = ("application/json" if is_json else
                        "application/x-www-form-urlencoded")
        responses.add_callback(response_method, url, content_type=content_type,
                               callback=wrapped_callback)


if __name__ == '__main__':
    unittest.main()
