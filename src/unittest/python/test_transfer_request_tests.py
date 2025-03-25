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


if __name__ == '__main__':
    unittest.main()
