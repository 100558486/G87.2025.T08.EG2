import unittest
import json
import os
from uc3m_money.account_manager import AccountManager, AccountManagementException


class TestAccountManager(unittest.TestCase):
    TRANSACTIONS_FILE = "transactions.json"

    def setUp(self):
        """Creates a sample transactions.json file before each test."""
        self.manager = AccountManager(self.TRANSACTIONS_FILE)
        self.create_transactions_file([])  # Start with an empty file

    def tearDown(self):
        """Deletes transactions.json after each test."""
        if os.path.exists(self.TRANSACTIONS_FILE):
            os.remove(self.TRANSACTIONS_FILE)

    def create_transactions_file(self, transactions):
        """Helper function to create a local transactions.json file."""
        with open(self.TRANSACTIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

    def test_valid_iban_sum_transactions_store_result(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"},
            {"IBAN": "ES7921000813610123456789", "amount": "50"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_invalid_iban_exception(self):
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("INVALID_IBAN")
        print(str(context.exception))

    def test_iban_not_in_transactions_exception(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"}
        ])
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610987654321")
        print(str(context.exception))

    def test_valid_iban_only_deposits(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"},
            {"IBAN": "ES7921000813610123456789", "amount": "200"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_valid_iban_only_withdrawals(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "-50"},
            {"IBAN": "ES7921000813610123456789", "amount": "-100"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_valid_iban_mixed_transactions(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "200"},
            {"IBAN": "ES7921000813610123456789", "amount": "-50"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_empty_transactions_file_exception(self):
        self.create_transactions_file([])  # Empty file
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_file_not_found_exception(self):
        os.remove(self.TRANSACTIONS_FILE)  # Ensure file is deleted
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_internal_processing_error_exception(self):
        with open(self.TRANSACTIONS_FILE, "w", encoding="utf-8") as file:
            file.write("{invalid_json}")  # Corrupt JSON file
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_valid_iban_edge_case_zero_transactions(self):
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "0"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))


if __name__ == "__main__":
    unittest.main()
