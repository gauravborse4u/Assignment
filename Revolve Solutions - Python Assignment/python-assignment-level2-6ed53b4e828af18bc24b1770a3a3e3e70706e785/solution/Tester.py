import unittest

from solution.solution_start import read_json_lines, read_csv


class TestDataProcessing(unittest.TestCase):

    def test_read_csv(self):
        # Define test data
        file_path = './test_data/customer.csv'
        expected_data = [
            {'customer_id': 'C1', 'loyalty_score': '7'},
            {'customer_id': 'C2', 'loyalty_score': '4'},
            {'customer_id': 'C3', 'loyalty_score': '8'}
        ]

        # Call the function
        result = read_csv(file_path)

        # Compare the result with the expected data
        self.assertEqual(result, expected_data)


if __name__ == '__main__':
    unittest.main()
