"""
Transfer Request Module

This module provides functionality for managing transfer requests, including validation
of IBANs, transfer types, concepts, dates, and amounts. It also ensures duplicate
transfer detection and securely stores transfer data in a JSON file.

Classes:
    - AccountManagementException: Custom exception for invalid transfer requests.
    - TransferRequest: Represents and validates a transfer request.

Functions:
    - transfer_request: Creates, validates, and stores a transfer request.

Usage:
    from transfer_module import transfer_request

    transfer_code = transfer_request(
        from_iban="ES9121000418450200051332",
        to_iban="ES7921000418450200056789",
        concept="Payment for services",
        transfer_type="ORDINARY",
        date="15/04/2025",
        amount=150.75
    )
"""
import hashlib
import json
import re
from datetime import datetime, timezone


class AccountManagementException(Exception):
    """Custom exception for invalid transfer requests."""
    pass


class TransferRequest:
    """Class representing a transfer request."""

    VALID_TRANSFER_TYPES = {"ORDINARY", "URGENT", "IMMEDIATE"}

    def __init__(
        self, from_iban: str, transfer_type: str, to_iban: str,
        transfer_concept: str, transfer_date: str, transfer_amount: float
    ):
        """
        Initializes a TransferRequest instance with validated attributes.

        Args:
            from_iban (str): The sender's IBAN.
            transfer_type (str): The type of transfer.
            to_iban (str): The recipient's IBAN.
            transfer_concept (str): The transfer concept/description.
            transfer_date (str): The transfer date in 'DD/MM/YYYY' format.
            transfer_amount (float): The amount to transfer.
        """
        self.__from_iban = self.validate_iban(from_iban)
        self.__to_iban = self.validate_iban(to_iban)
        self.__transfer_type = self.validate_transfer_type(transfer_type)
        self.__concept = self.validate_concept(transfer_concept)
        self.__transfer_date = self.validate_date(transfer_date)
        self.__transfer_amount = self.validate_amount(transfer_amount)

        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Transfer:" + json.dumps(self.__dict__)

    def to_json(self):
        """Returns the object information in JSON format."""
        return {
            "from_iban": self.__from_iban,
            "to_iban": self.__to_iban,
            "transfer_type": self.__transfer_type,
            "transfer_amount": self.__transfer_amount,
            "transfer_concept": self.__concept,
            "transfer_date": self.__transfer_date,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.transfer_code,
        }

    @property
    def transfer_code(self):
        """Returns the MD5 signature (transfer code)."""
        return hashlib.md5(str(self).encode()).hexdigest()

    @staticmethod
    def validate_iban(iban: str):
        """
        Validates that the IBAN is a Spanish IBAN.

        Args:
            iban (str): The IBAN to validate.

        Returns:
            str: The validated IBAN.

        Raises:
            AccountManagementException: If the IBAN is invalid.
        """
        if not re.fullmatch(r"ES\d{22}", iban):
            raise AccountManagementException(
                "Invalid IBAN: Must start with 'ES' and contain 24 digits"
            )
        return iban

    @staticmethod
    def validate_concept(concept: str):
        """
        Validates the concept.

        Args:
            concept (str): The transfer concept.

        Returns:
            str: The validated concept.

        Raises:
            AccountManagementException: If the concept is invalid.
        """
        if not (10 <= len(concept) <= 30) or len(concept.split()) < 2:
            raise AccountManagementException(
                "Invalid concept: Must be 10-30 characters and contain at least two words"
            )
        return concept

    @classmethod
    def validate_transfer_type(cls, transfer_type: str):
        """
        Validates the transfer type.

        Args:
            transfer_type (str): The type of transfer.

        Returns:
            str: The validated transfer type.

        Raises:
            AccountManagementException: If the transfer type is invalid.
        """
        if transfer_type not in cls.VALID_TRANSFER_TYPES:
            raise AccountManagementException(
                "Invalid transfer type: Must be 'ORDINARY', 'URGENT', or 'IMMEDIATE'"
            )
        return transfer_type

    @staticmethod
    def validate_date(date_str: str):
        """
        Validates the transfer date.

        Args:
            date_str (str): The date string in 'DD/MM/YYYY' format.

        Returns:
            str: The validated date string.

        Raises:
            AccountManagementException: If the date format is incorrect
            or the date is outside the allowed range.
        """
        try:
            transfer_date = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError as exc:
            raise AccountManagementException(
                "Invalid date format: Must be 'DD/MM/YYYY'"
            ) from exc

        if not 2025 <= transfer_date.year <= 2050:
            raise AccountManagementException(
                "Invalid year: Must be between 2025 and 2050"
            )

        if transfer_date.date() < datetime.today().date():
            raise AccountManagementException("Invalid date: Cannot be in the past")

        return date_str

    @staticmethod
    def validate_amount(amount: float):
        """
        Validates the transfer amount.

        Args:
            amount (float): The amount to validate.

        Returns:
            float: The validated amount.

        Raises:
            AccountManagementException: If the amount is out of range
            or has more than two decimal places.
        """
        if not 10.00 <= amount <= 10000.00:
            raise AccountManagementException(
                "Invalid amount: Must be between 10.00 and 10000.00"
            )

        if len(str(amount).rsplit(".", maxsplit=1)[-1]) > 2:
            raise AccountManagementException(
                "Invalid amount: Can have at most 2 decimal places"
            )

        return amount


def transfer_request(
    from_iban: str, to_iban: str, concept: str, transfer_type: str, date: str, amount: float
) -> str:
    """
    Processes a transfer request and saves it to a JSON file.

    Args:
        from_iban (str): Sender's IBAN.
        to_iban (str): Recipient's IBAN.
        concept (str): Transfer concept.
        transfer_type (str): Type of transfer.
        date (str): Transfer date in 'DD/MM/YYYY' format.
        amount (float): Transfer amount.

    Returns:
        str: The transfer code.

    Raises:
        AccountManagementException: If there is a duplicate transfer.
    """
    transfer = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)
    transfer_data = transfer.to_json()

    file_name = "transfers.json"
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            transfers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        transfers = []

    if any(t["transfer_code"] == transfer.transfer_code for t in transfers):
        raise AccountManagementException("Duplicate transfer detected")

    transfers.append(transfer_data)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(transfers, f, indent=4)

    return transfer.transfer_code
