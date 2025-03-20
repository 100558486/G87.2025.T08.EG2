import unittest
import sys
import os
from unittest.mock import patch, mock_open

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main/python')))
from src.main.python.uc3m_money.deposit_request import deposit_into_account, AccountManagementException

class DepositRequestTests(unittest.TestCase):
    """Test cases for the deposit_into_account function"""

    def run_test_case(self, file_path, expected_message):
        print(f"Testing: {expected_message}")
        with self.assertRaises(AccountManagementException) as context:
            deposit_into_account(file_path)
        print(f"Exception raised: {context.exception}")
        self.assertEqual(str(context.exception), expected_message)

    def test_missing_file(self):
        self.run_test_case("./data/missing.json", "The data file is not found")

    def test_invalid_format(self):
        self.run_test_case("./data/deposit_invalid.txt", "The file is not in JSON format")

    def test_missing_iban(self):
        self.run_test_case("./data/deposit_missing_iban.json", "The JSON does not have the expected structure")

    def test_missing_amount(self):
        self.run_test_case("./data/deposit_missing_amount.json", "The JSON does not have the expected structure")

    def test_invalid_iban_format(self):
        self.run_test_case("./data/deposit_invalid_iban.json", "Invalid IBAN format")

    def test_foreign_iban(self):
        self.run_test_case("./data/deposit_foreign_iban.json", "Invalid IBAN format")

    def test_wrong_currency(self):
        self.run_test_case("./data/deposit_wrong_currency.json", "Invalid amount format")

    def test_non_numeric_amount(self):
        self.run_test_case("./data/deposit_non_numeric_amount.json", "Invalid amount format")

    def test_negative_amount(self):
        self.run_test_case("./data/deposit_negative.json", "Invalid amount format")

    def test_duplicate_entry(self):
        self.run_test_case("./data/deposit_duplicate.json", "Duplicate entry")

    def test_missing_colon(self):
        self.run_test_case("./data/deposit_missing_colon.json", "The file is not in JSON format")

    def test_missing_comma(self):
        self.run_test_case("./data/deposit_missing_comma.json", "The file is not in JSON format")

    def test_missing_quotes(self):
        self.run_test_case("./data/deposit_missing_quotes.json", "The file is not in JSON format")

    def test_internal_error_signature(self):
        self.run_test_case("./data/deposit1.json", "Signature error")

    def test_valid_deposit(self):
        print("Testing valid deposit request...")
        result = deposit_into_account("./data/deposit1.json")
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)  # SHA-256 produces a 64-character hex string

if __name__ == "__main__":
    unittest.main()
