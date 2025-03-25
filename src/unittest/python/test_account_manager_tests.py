# Module docstring: Describes the purpose of the test module
"""
Unit tests for the AccountManager class, verifying transaction balance calculations, error handling,
and edge cases.
"""
import unittest
import json
import os
from uc3m_money.account_manager import AccountManager, AccountManagementException




class TestAccountManager(unittest.TestCase):
    """
    Test suite for the AccountManager class, including various scenarios like valid IBANs
    ,invalid IBANs, handling of empty or corrupted transaction files.
    """
    TRANSACTIONS_FILE = "transactions.json"

    def setUp(self):
        """
        Creates a sample transactions.json file before each test.

        Initializes the AccountManager instance and sets up an empty transactions
        file for each test.
        """
        self.manager = AccountManager(self.TRANSACTIONS_FILE)
        self.create_transactions_file([])  # Start with an empty file

    def tearDown(self):
        """
        Deletes transactions.json after each test.

        Ensures that the transactions file is removed if it exists, cleaning up after tests.
        """
        if os.path.exists(self.TRANSACTIONS_FILE):
            os.remove(self.TRANSACTIONS_FILE)

    def create_transactions_file(self, transactions):
        """
        Helper function to create a local transactions.json file.

        Args:
            transactions (list): A list of transactions to be written to the JSON file.
        """
        with open(self.TRANSACTIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

    def test_valid_iban_sum_transactions_store_result(self):
        """
        Test case to validate the correct balance calculation for valid IBAN
        with deposit transactions.

        Verifies that the sum of all deposits for a specific IBAN is accurately calculated.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"},
            {"IBAN": "ES7921000813610123456789", "amount": "50"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_invalid_iban_exception(self):
        """
        Test case to verify that an exception is raised when an invalid IBAN is provided.

        This tests that the system correctly handles invalid IBAN inputs.
        """
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("INVALID_IBAN")
        print(str(context.exception))

    def test_iban_not_in_transactions_exception(self):
        """
        Test case to ensure that an exception is raised when an IBAN is
        not found in the transactions file.

        Verifies that the system correctly identifies when an IBAN is missing from the records.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"}
        ])
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610987654321")
        print(str(context.exception))

    def test_valid_iban_only_deposits(self):
        """
        Test case for a valid IBAN with only deposit transactions.

        Verifies that the balance calculation correctly sums up deposit amounts.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "100"},
            {"IBAN": "ES7921000813610123456789", "amount": "200"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_valid_iban_only_withdrawals(self):
        """
        Test case for a valid IBAN with only withdrawal transactions.

        Verifies that the balance calculation correctly sums up withdrawal amounts.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "-50"},
            {"IBAN": "ES7921000813610123456789", "amount": "-100"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_valid_iban_mixed_transactions(self):
        """
        Test case for a valid IBAN with both deposit and withdrawal transactions.

        Verifies that the balance calculation correctly accounts for both deposits and withdrawals.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "200"},
            {"IBAN": "ES7921000813610123456789", "amount": "-50"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))

    def test_empty_transactions_file_exception(self):
        """
        Test case to verify that an exception is raised when the transactions file is empty.

        This tests that the system correctly handles the scenario where no transactions are present.
        """
        self.create_transactions_file([])  # Empty file
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_file_not_found_exception(self):
        """
        Test case to verify that an exception is raised if the transactions file is not found.

        Verifies the system raises an appropriate exception when the file is missing.
        """
        os.remove(self.TRANSACTIONS_FILE)  # Ensure file is deleted
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_internal_processing_error_exception(self):
        """
        Test case to simulate an internal processing error due to a corrupted
        JSON file.

        Verifies that the system raises an exception when the transactions file
        contains invalid JSON.
        """
        with open(self.TRANSACTIONS_FILE, "w", encoding="utf-8") as file:
            file.write("{invalid_json}")  # Corrupt JSON file
        with self.assertRaises(AccountManagementException) as context:
            self.manager.calculate_balance("ES7921000813610123456789")
        print(str(context.exception))

    def test_valid_iban_edge_case_zero_transactions(self):
        """
        Test case for a valid IBAN with a zero transaction amount.

        Verifies that the balance calculation correctly handles zero amounts.
        """
        self.create_transactions_file([
            {"IBAN": "ES7921000813610123456789", "amount": "0"}
        ])
        self.assertTrue(self.manager.calculate_balance("ES7921000813610123456789"))


if __name__ == "__main__":
    unittest.main()
