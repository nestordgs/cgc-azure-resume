import json
from utils import send_response
from unittest import mock, TestCase

class TestUtils(TestCase):

    def test_send_response_json(self):
        
        response = send_response({
            "message": 'Something went wront',
            "status_code": 400
        })

        self.assertEqual({
            "message": 'Something went wront',
            "status_code": 400
        }, json.loads(response.get_body()))

    def test_send_response_string(self):
        
        response = send_response('Message send successfully', is_json=False)

        self.assertEqual(
            'Message send successfully'
            , response.get_body().decode("utf-8")
        )