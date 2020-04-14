from unittest import TestCase
from network.request import Request, RequestType

class RequestTest(TestCase):
    def test_create_table(self):
        request = Request('create_table:me:my table:2')
    
        self.assertEqual(request.type, RequestType.CREATE_TABLE)
        self.assertEqual(request.player, 'me')
        self.assertListEqual(request.values, ['my table', '2'])
        