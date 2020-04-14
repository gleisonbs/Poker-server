from unittest import TestCase

from network.request_specification import RequestSpecification

class RequestSpecificationTest(TestCase):
    def test_request_without_colon(self):
        result = RequestSpecification().is_satisfied_by('request')
        self.assertEqual(result, False)

    def test_empty_request(self):
        result = RequestSpecification().is_satisfied_by('')
        self.assertEqual(result, False)

    def test_create_table(self):
        result = RequestSpecification().is_satisfied_by('create_table:me:my table:2')
        self.assertEqual(result, True)

    def test_create_table_lest_than_2_max_players(self):
        result = RequestSpecification().is_satisfied_by('create_table:me:my table:1')
        self.assertEqual(result, False)

        result = RequestSpecification().is_satisfied_by('create_table:me:my table:0')
        self.assertEqual(result, False)

        result = RequestSpecification().is_satisfied_by('create_table:me:my table:-1')
        self.assertEqual(result, False)

    def test_create_table_more_than_10_max_players(self):
        result = RequestSpecification().is_satisfied_by('create_table:me:my table:11')
        self.assertEqual(result, False)

        result = RequestSpecification().is_satisfied_by('create_table:me:my table:100000')
        self.assertEqual(result, False)

    def test_list_tables(self):
        result = RequestSpecification().is_satisfied_by('list_tables:me')
        self.assertEqual(result, True)

