"""
This module provides functionality for managing bank account transactions,
validating IBANs, and calculating balances from a transactions file.
"""

import json
import os
import re
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException


class AccountManager:
    """
    Manages bank account transactions, including balance calculations
    and IBAN validation.
    """

    def __init__(self, transactions_file="transactions.json"):
        """
        Initializes the AccountManager with a transactions file.

        Args:
            transactions_file (str): Name of the transactions file. Defaults to "transactions.json".
        """
        self.transactions_file = transactions_file

    @staticmethod
    def validate_iban(iban: str) -> bool:
        """
        Checks if the IBAN follows the valid Spanish IBAN format.

        Args:
            iban (str): The IBAN to validate.

        Returns:
            bool: True if the IBAN is valid, False otherwise.
        """
        return isinstance(iban, str) and bool(re.match(r"ES\d{22}", iban))

    def calculate_balance(self, iban_number: str) -> bool:
        """
        Calculates the balance for a given IBAN and
        records the result.

        Args:
            iban_number (str): The IBAN for which to calculate the balance.

        Returns:
            bool: True if the balance was successfully calculated and saved.

        Raises:
            AccountManagementException: If any validation or file-related errors occur.
        """
        if not self.validate_iban(iban_number):
            raise AccountManagementException("Invalid IBAN format")

        if not os.path.exists(self.transactions_file):
            raise AccountManagementException("Transactions file not found")

        try:
            with open(self.transactions_file, "r", encoding="utf-8") as file:
                transactions = json.load(file)
        except json.JSONDecodeError as exc:
            raise AccountManagementException("Error decoding JSON file") from exc

        if not isinstance(transactions, list):
            raise AccountManagementException("Invalid transactions data format")

        balance = 0.0
        found = False

        for transaction in transactions:
            if not isinstance(transaction, dict) or "IBAN" not in transaction or "amount" not in transaction:
                continue

            if transaction["IBAN"] == iban_number:
                try:
                    balance += float(transaction["amount"].replace(",", "."))
                    found = True
                except ValueError as exc:
                    raise AccountManagementException(
                        "Invalid amount format in transactions file"
                    ) from exc

        if not found:
            raise AccountManagementException("IBAN not found in transactions file")

        timestamp = datetime.now(timezone.utc).timestamp()

        balance_record = {
            "IBAN": iban_number,
            "timestamp": timestamp,
            "balance": balance,
        }

        output_file = f"balance_{iban_number}.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(balance_record, file, indent=4)

        return True
