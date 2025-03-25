import hashlib
import json
import re
from datetime import datetime, timezone


class AccountManagementException(Exception):
    """Custom exception for invalid transfer requests"""
    pass


class TransferRequest:
    """Class representing a transfer request"""

    VALID_TRANSFER_TYPES = {"ORDINARY", "URGENT", "IMMEDIATE"}

    def __init__(self, from_iban: str, transfer_type: str, to_iban: str, transfer_concept: str, transfer_date: str,
                 transfer_amount: float):
        # ✅ Calling validation functions before assignment
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
        """returns the object information in json format"""
        return {
            "from_iban": self.__from_iban,
            "to_iban": self.__to_iban,
            "transfer_type": self.__transfer_type,
            "transfer_amount": self.__transfer_amount,
            "transfer_concept": self.__concept,
            "transfer_date": self.__transfer_date,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.transfer_code
        }

    @property
    def transfer_code(self):
        """Returns the md5 signature (transfer code)"""
        return hashlib.md5(str(self).encode()).hexdigest()

    # ✅ IBAN VALIDATION
    @staticmethod
    def validate_iban(iban: str):
        """Validates that the IBAN is a Spanish IBAN (starts with ES and is 24 characters long)"""
        if not re.fullmatch(r"ES\d{22}", iban):
            raise AccountManagementException("Invalid IBAN: Must start with 'ES' and contain 24 digits")
        return iban

    # ✅ CONCEPT VALIDATION
    @staticmethod
    def validate_concept(concept: str):
        """Validates the concept (10-30 characters, must contain at least two words)"""
        if not (10 <= len(concept) <= 30) or len(concept.split()) < 2:
            raise AccountManagementException("Invalid concept: Must be 10-30 characters and contain at least two words")
        return concept

    # ✅ TRANSFER TYPE VALIDATION
    @classmethod
    def validate_transfer_type(cls, transfer_type: str):
        """Validates that the transfer type is one of the allowed values"""
        if transfer_type not in cls.VALID_TRANSFER_TYPES:
            raise AccountManagementException("Invalid transfer type: Must be 'ORDINARY', 'URGENT', or 'IMMEDIATE'")
        return transfer_type

    # ✅ DATE VALIDATION
    @staticmethod
    def validate_date(date_str: str):
        """Validates the transfer date (must be in 'DD/MM/YYYY' format, between 2025 and 2050, and not before today)"""
        try:
            transfer_date = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise AccountManagementException("Invalid date format: Must be 'DD/MM/YYYY'")

        # Ensure year is between 2025 and 2050
        if not (2025 <= transfer_date.year <= 2050):
            raise AccountManagementException("Invalid year: Must be between 2025 and 2050")

        # Ensure date is not before today
        if transfer_date.date() < datetime.today().date():
            raise AccountManagementException("Invalid date: Cannot be in the past")

        return date_str

    # ✅ AMOUNT VALIDATION
    @staticmethod
    def validate_amount(amount: float):
        """Validates the transfer amount (must be between 10.00 and 10000.00 with max 2 decimal places)"""
        if not (10.00 <= amount <= 10000.00):
            raise AccountManagementException("Invalid amount: Must be between 10.00 and 10000.00")
        if len(str(amount).split(".")[-1]) > 2:
            raise AccountManagementException("Invalid amount: Can have at most 2 decimal places")
        return amount


def transfer_request(from_iban: str, to_iban: str, concept: str, transfer_type: str, date: str, amount: float) -> str:
    transfer = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)
    transfer_data = transfer.to_json()

    file_name = "transfers.json"
    try:
        with open(file_name, "r") as f:
            transfers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        transfers = []

    # duplicate transfer detection
    if any(t["transfer_code"] == transfer.transfer_code for t in transfers):
        raise AccountManagementException("Duplicate transfer detected")

    transfers.append(transfer_data)
    with open(file_name, "w") as f:
        json.dump(transfers, f, indent=4)

    return transfer.transfer_code