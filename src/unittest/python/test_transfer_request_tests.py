"""class for testing the regsiter_order method"""
import unittest
import sys
import os

# Add the 'src/main/python' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main/python')))
# from uc3m_money import AccountManager
# from uc3m_money.transfer_request import transfer_request
# from uc3m_money.account_management_exception import AccountManagementException

#
# class MyTestCase(unittest.TestCase):
#     """class for testing the register_order method"""
#     def test_something( self ):
#         """dummy test"""
#         self.assertEqual(True, False)
#  def test_valid_transfer(self):
#         """Test a valid transfer request"""
#         result = transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "07/01/2025", 500.00)
#         self.assertIsInstance(result, str)  # Should return an MD5 hash string
#         self.assertEqual(len(result), 32)  # MD5 hashes are always 32 characters
#
#     def test_invalid_from_iban(self):
#         """Test invalid sender IBAN"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("INVALID_IBAN", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "07/01/2025", 500.00)
#
#     def test_invalid_to_iban(self):
#         """Test invalid receiver IBAN"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "INVALID_IBAN", "Payment invoice", "ORDINARY", "07/01/2025", 500.00)
#
#     def test_invalid_concept(self):
#         """Test invalid transfer concept (too short)"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Short", "ORDINARY", "07/01/2025", 500.00)
#
#     def test_invalid_transfer_type(self):
#         """Test invalid transfer type"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "FAST", "07/01/2025", 500.00)
#
#     def test_invalid_date_format(self):
#         """Test invalid date format"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "2025-01-07", 500.00)
#
#     def test_invalid_amount(self):
#         """Test invalid amount (too low)"""
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "07/01/2025", 5.00)
#
#     def test_duplicate_transfer(self):
#         """Test duplicate transfer exception"""
#         transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "07/01/2025", 500.00)
#         with self.assertRaises(AccountManagementException):
#             transfer_request("ES7921000813610123456789", "ES7921000813610987654321", "Payment invoice", "ORDINARY", "07/01/2025", 500.00)

if __name__ == '__main__':
    unittest.main()
