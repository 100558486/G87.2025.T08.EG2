import unittest
import json
import os
import tempfile
from src.main.python.uc3m_money.account_deposit import deposit_into_account, AccountManagementException

class TestComprehensiveAccountDeposit(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

        # Comprehensive test data covering all scenarios
        self.test_data = {
            "valid_json": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_start_brace": '"alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_start_brace": '{{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_end_brace": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z"',
            "duplicate_end_brace": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }}',
            "empty_data": '{ }',
            "duplicate_data": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z", "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_alg_key": '{ "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_alg_key": '{ "alg": "SHA-256", "alg": "SHA-512", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "modified_alg_key": '{ "algorithm": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "modified_alg_value": '{ "alg": "MD5", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_alg_value": '{ "alg": , "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_alg_value": '{ "alg": "SHA-256 SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_typ_key": '{ "alg": "SHA-256", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_typ_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "typ": "WITHDRAWAL", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "modified_typ_key": '{ "alg": "SHA-256", "transaction_type": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "modified_typ_value": '{ "alg": "SHA-256", "typ": "TRANSFER", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_typ_value": '{ "alg": "SHA-256", "typ": , "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_typ_value": '{ "alg": "SHA-256", "typ": "DEPOSIT DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_iban_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_iban_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "iban": "ES9121000418450200051333", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "invalid_iban_value": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "INVALID_IBAN", "amount": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_amount_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "deposit_date": "2025-03-20T12:34:56Z" }',
            "duplicate_amount_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "amount": "EUR 2000.00", "deposit_date": "2025-03-20T12:34:56Z" }',
            "modified_amount_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "money": "EUR 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "invalid_amount_value": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "USD 1000.50", "deposit_date": "2025-03-20T12:34:56Z" }',
            "missing_deposit_date_key": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50" }',
            "invalid_deposit_date_value": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": "INVALID_DATE" }',
            "missing_deposit_date_value": '{ "alg": "SHA-256", "typ": "DEPOSIT", "iban": "ES9121000418450200051332", "amount": "EUR 1000.50", "deposit_date": }'
        }

        # Creating test files in the temporary directory
        self.test_files = {}
        for key, data in self.test_data.items():
            file_path = os.path.join(self.test_dir, f"deposit_{key}.json")

            try:
                # Handle different types of input
                with open(file_path, "w") as f:
                    f.write(data if isinstance(data, str) else json.dumps(data))

                self.test_files[key] = file_path
            except Exception as e:
                print(f"Error creating file {key}: {e}")

    def get_file_path(self, key):
        """Helper method to get file path, with fallback."""
        return self.test_files.get(key, os.path.join(self.test_dir, f"deposit_{key}.json"))

    def run_error_test(self, key):
        """Helper function to print out the actual error message"""
        file_path = self.get_file_path(key)
        print(f"\nRunning test for: {file_path}")
        try:
            deposit_into_account(file_path)
            self.fail(f"Expected AccountManagementException for {key}")
        except AccountManagementException as e:
            print(f"AccountManagementException: {str(e)}")
            raise  # Re-raise to ensure test failure

    def test_valid_deposit(self):
        print("\nRunning test_valid_deposit")
        signature = deposit_into_account(self.get_file_path("valid_json"))
        print(f"Generated Signature: {signature}")
        self.assertIsInstance(signature, str)

    # JSON Structure Tests
    def test_missing_start_brace(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_start_brace")

    def test_duplicate_start_brace(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_start_brace")

    def test_missing_end_brace(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_end_brace")

    def test_duplicate_end_brace(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_end_brace")

    def test_empty_data(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("empty_data")

    def test_duplicate_data(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_data")

    # Separator Tests
    def test_missing_separator(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_separator")

    def test_duplicate_separator(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_separator")

    # 'alg' Key Tests
    def test_missing_alg_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_alg_key")

    def test_duplicate_alg_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_alg_key")

    def test_modified_alg_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_alg_key")

    def test_modified_alg_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_alg_value")

    def test_missing_alg_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_alg_value")

    def test_duplicate_alg_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_alg_value")

    # 'typ' Key Tests
    def test_missing_typ_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_typ_key")

    def test_duplicate_typ_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_typ_key")

    def test_modified_typ_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_typ_key")

    def test_modified_typ_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_typ_value")

    def test_missing_typ_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_typ_value")

    def test_duplicate_typ_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_typ_value")

    # 'iban' Key Tests
    def test_missing_iban_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_iban_key")

    def test_duplicate_iban_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_iban_key")

    def test_modified_iban_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_iban_key")

    def test_invalid_iban_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("invalid_iban_value")

    def test_missing_iban_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_iban_value")

    def test_duplicate_iban_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_iban_value")

    # 'amount' Key Tests
    def test_missing_amount_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_amount_key")

    def test_duplicate_amount_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_amount_key")

    def test_modified_amount_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_amount_key")

    def test_missing_amount_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_amount_value")

    def test_duplicate_amount_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_amount_value")

    def test_invalid_amount_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("invalid_amount_value")

    # 'deposit_date' Key Tests
    def test_missing_deposit_date_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_deposit_date_key")

    def test_duplicate_deposit_date_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_deposit_date_key")

    def test_modified_deposit_date_key(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("modified_deposit_date_key")

    def test_invalid_deposit_date_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("invalid_deposit_date_value")

    def test_missing_deposit_date_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("missing_deposit_date_value")

    def test_duplicate_deposit_date_value(self):
        with self.assertRaises(AccountManagementException):
            self.run_error_test("duplicate_deposit_date_value")

    def tearDown(self):
        """Remove temporary directory and test files."""
        try:
            import shutil
            shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"Error removing temporary directory: {e}")


if __name__ == "__main__":
    unittest.main()