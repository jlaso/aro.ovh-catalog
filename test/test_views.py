import unittest

from service.web_service import app


class TestViews(unittest.TestCase):

    def test_analytics_pbjs(self):
        client = app.test_client()
        partner_id = 1234
        url = f"/{partner_id}/pbjs"
        resp = client.get(url)
        self.assertTrue("partner_id" in resp.json)
