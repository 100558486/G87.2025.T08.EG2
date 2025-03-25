"""
This module provides functionality for processing account deposits, including
validating IBANs, amounts, and deposit dates, as well as handling JSON input.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
import re
from collections import OrderedDict
from uc3m_money.account_management_exception import AccountManagementException

class AccountDeposit:
    """Class representing the information required for a deposit."""

    def __init__(self, to_iban: str, deposit_amount: float):
        """
        Initializes an AccountDeposit instance.

        Args:
            to_iban (str): The IBAN to which the deposit is made.
            deposit_amount (float): The deposit amount in EUR.
        """
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """
        Returns the object data in JSON format.

        Returns:
            dict: The deposit details as a dictionary.
        """
        return {
            "alg": self.__alg,
            "type": self.__type,
            "to_iban": self.__to_iban,
            "deposit_amount": self.__deposit_amount,
            "deposit_date": self.__deposit_date,
            "deposit_signature": self.deposit_signature
        }

    def __signature_string(self):
        """
        Composes the string used for generating the signature hash.

        Returns:
            str: A string representation of the deposit data.
        """
        return "{alg:" + str(self.__alg) + ",typ:" + str(self.__type) + \
               ",iban:" + str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def deposit_signature(self):
        """
        Generates a SHA-256 signature for the deposit.

        Returns:
            str: The deposit signature.
        """
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def deposit_date(self):
        """
        Gets the deposit date.

        Returns:
            float: The timestamp of the deposit.
        """
        return self.__deposit_date


def validate_iban(iban: str) -> bool:
    """
    Validates the format of an IBAN.

    Args:
        iban (str): The IBAN string to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        AccountManagementException: If a duplicate IBAN is detected.
    """
    if not isinstance(iban, str) or not re.match(r'ES\d{22}', iban):
        return False

    iban_parts = iban.split()
    if len(set(iban_parts)) < len(iban_parts):  # Detect duplicate IBANs
        raise AccountManagementException("Duplicate IBAN value detected")

    return True


def validate_amount(amount: str) -> float:
    """
    Validates the amount format and converts it to float.

    Args:
        amount (str): The amount string in "EUR 1000.50" format.

    Returns:
        float: The numeric amount.

    Raises:
        AccountManagementException: If the amount format is invalid.
    """
    match = re.match(r'^EUR\s(\d+\.\d{2})$', amount)
    if match:
        return float(match.group(1))

    raise AccountManagementException("Invalid amount format")


def validate_date(date_str: str):
    """
    Validates the format of a deposit date.

    Args:
        date_str (str): The deposit date string.

    Raises:
        AccountManagementException: If the date format is invalid.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise AccountManagementException("Invalid deposit_date format") from exc


def load_json_with_duplicate_check(input_file):
    """
    Loads a JSON file while checking for duplicate keys.

    Args:
        input_file (str): The path to the JSON file.

    Returns:
        dict: The parsed JSON data.

    Raises:
        AccountManagementException: If duplicate keys are found.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        key_counts = {}

        def detect_duplicates(pairs):
            for key, _ in pairs:
                key_counts[key] = key_counts.get(key, 0) + 1
                if key_counts[key] > 1:
                    raise AccountManagementException(f"Duplicate {key} key found in JSON")
            return OrderedDict(pairs)

        return json.load(file, object_pairs_hook=detect_duplicates)


def deposit_into_account(input_file: str) -> str:
    """
    Processes a deposit from a JSON file.

    Args:
        input_file (str): The path to the JSON file.

    Returns:
        str: The deposit signature.

    Raises:
        AccountManagementException: If any validation fails.
    """
    if not os.path.exists(input_file):
        raise AccountManagementException("The data file is not found")

    try:
        data = load_json_with_duplicate_check(input_file)
    except json.JSONDecodeError as exc:
        raise AccountManagementException("The file is not in JSON format") from exc

    if not data:
        raise AccountManagementException("Empty JSON data")

    required_keys = {"alg", "typ", "iban", "amount", "deposit_date"}
    missing_keys = required_keys - data.keys()
    if missing_keys:
        raise AccountManagementException(f"Missing required keys: {', '.join(missing_keys)}")

    if data["alg"] != "SHA-256" or data["typ"] != "DEPOSIT":
        raise AccountManagementException("Invalid alg or typ value")

    if not validate_iban(data["iban"]):
        raise AccountManagementException("Invalid IBAN format")

    deposit_amount = validate_amount(data["amount"])
    validate_date(data["deposit_date"])

    deposit = AccountDeposit(data["iban"], deposit_amount)
    output_file = f"deposit_{data['iban']}_{int(deposit.deposit_date)}.json"

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(deposit.to_json(), file, indent=4)

    return deposit.deposit_signature
