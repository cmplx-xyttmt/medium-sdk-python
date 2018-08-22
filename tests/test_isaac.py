import responses
import unittest
from urllib.parse import parse_qs
import json

from medium import Client, MediumError


class TestIsaac(unittest.TestCase):

    def setUp(self):
        self.client = Client(access_token="isaac-token")

    @responses.activate
    def test_create_post_fails(self):
        """Tests whether MediumError exception occurs if publish_status is not in the payload"""
        def response_callback(payload):
            data = {
                "license": "all-rights-reserved",
                "title": "Starships",
                "url": "https://medium.com/@nicki/55050649c95",
                "tags": ["stars", "ships", "pop"],
                "authorId": "5303d74c64f66366f00cb9b2a94f3251bf5",
                "publishStatus": "draft",
                "id": "55050649c95",
            }

            if "publish_status" in payload:
                return 200, data

            return 400, {"error": ["Bad Request"]}

        self._mock_endpoint(
            "POST",
            "/v1/users/5303d74c64f66366f00cb9b2a94f3251bf5/posts",
            response_callback
        )

        with self.assertRaises(MediumError) as context:
            self.client.create_post(
                "5303d74c64f66366f00cb9b2a94f3251bf5",
                "Starships",
                "<p>Are meant to flyyyy</p>",
                "html",
                tags=["stars", "ships", "pop"]
            )

        self.assertEqual('API request failed', str(context.exception))

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
