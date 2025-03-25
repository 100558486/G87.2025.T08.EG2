import unittest

from uc3m_money import account_management_exception
from uc3m_money.transfer_request import transfer_request, AccountManagementException



class TransferRequestTests(unittest.TestCase):
    """Test cases for the TransferRequest class"""

    def test_valid_transfer(self):
        print("Testing valid transfer request...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                                  "7/7/2025", 500.75)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_min_valid_amount(self):
        print("Testing minimum valid transfer amount...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Car Repair", "IMMEDIATE",
                                  "7/7/2025", 10.00)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_max_valid_amount(self):
        print("Testing maximum valid transfer amount...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789",
                                  "House renovation payment", "URGENT", "31/12/2050", 10000.00)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_invalid_iban_country_code(self):
        print("Testing invalid IBAN (wrong country code)...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("FR9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/7/2025", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_invalid_iban_format(self):
        print("Testing invalid IBAN format...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES91A100041845020005133B", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/7/2025", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_invalid_iban_length(self):
        print("Testing invalid IBAN (length 23 characters)...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES912100041845020005133", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/7/2025", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_short_concept(self):
        print("Testing short transfer concept...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Rent", "ORDINARY", "7/7/2025",
                             500.75)
        print(f"Exception raised: {context.exception}")

    def test_concept_too_short(self):
        print("Testing concept with 9 characters (invalid)...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Rent pay", "ORDINARY",
                             "7/7/2025", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_invalid_transfer_type(self):
        print("Testing invalid transfer type...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "FAST",
                             "7/7/2025", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_invalid_past_date(self):
        print("Testing invalid past transfer date...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "31/12/2024", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_invalid_future_date(self):
        print("Testing invalid future transfer date...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "1/1/2051", 500.75)
        print(f"Exception raised: {context.exception}")

    def test_amount_below_minimum(self):
        print("Testing transfer amount below minimum...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/7/2025", 9.99)
        print(f"Exception raised: {context.exception}")

    def test_amount_above_maximum(self):
        print("Testing transfer amount above maximum...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/7/2025", 10000.01)
        print(f"Exception raised: {context.exception}")

    def test_transfer_amount_above_maximum(self):
        print("Testing transfer amount above maximum...")
        with self.assertRaises(AccountManagementException) as context:
            transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "House Rent", "ORDINARY",
                             "7/1/2025", 10000.01)
        print(f"Exception raised: {context.exception}")

    def test_valid_iban_different_banks(self):
        print("Testing valid IBANs with different banks...")
        result = transfer_request("ES4420385778983000760236", "ES3320385778983000760238", "Tuition Fees",
                                  "ORDINARY", "15/06/2025", 1500.00)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_valid_iban_same_bank(self):
        print("Testing valid IBANs with the same bank...")
        result = transfer_request("ES9121000418450200051332", "ES9121000418450200051340", "Car Loan Payment",
                                  "IMMEDIATE", "22/07/2025", 750.5)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_concept_max_length(self):
        print("Testing concept with max valid length (30 chars)..")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789",
                                  "Mortgage Payment March 25 Home", "URGENT", "2/2/2026", 2750.00)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_concept_min_length(self):
        print("Testing concept with min valid length (10 chars)...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Loan repay", "ORDINARY",
                                  "14/09/2025", 350.25)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_transfer_different_valid_types(self):
        print("Testing transfer with different valid types...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Subscription Fee",
                                  "URGENT", "7/8/2025", 999.99)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_transfer_last_valid_date(self):
        print("Testing transfer on last valid date (31/12/2050)...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Travel Booking", "IMMEDIATE",
                                  "31/12/2050", 4300.00)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_transfer_first_valid_date(self):
        print("Testing transfer on first valid date (25/03/2025)...")
        result = transfer_request("ES9121000418450200051332", "ES7921000813450200056789", "Insurance Premium",
                                  "ORDINARY", "25/03/2025", 1250.55)
        print(f"Received result: {result}")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

if __name__ == '__main__':
    unittest.main()
