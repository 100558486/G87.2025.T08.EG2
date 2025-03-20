"""Contains the class OrderShipping"""
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from src.main.python.uc3m_money import AccountManagementException


class AccountDeposit():
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount):
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def deposit_signature(self):
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()


def validate_iban(iban: str) -> bool:
    return bool(re.match(r'ES\d{22}', iban))


def validate_amount(amount: str) -> float:
    match = re.match(r'^EUR\s(\d+\.\d{2})$', amount)
    if match:
        return float(match.group(1))
    raise AccountManagementException("Invalid amount format")


def deposit_into_account(input_file: str) -> str:
    if not os.path.exists(input_file):
        raise AccountManagementException("The data file is not found")

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise AccountManagementException("The file is not in JSON format")

    if not all(key in data for key in ["IBAN", "AMOUNT"]):
        raise AccountManagementException("The JSON does not have the expected structure")

    iban = data["IBAN"]
    amount = data["AMOUNT"]

    if not validate_iban(iban):
        raise AccountManagementException("Invalid IBAN format")

    deposit_amount = validate_amount(amount)

    deposit = AccountDeposit(iban, deposit_amount)

    output_file = f"deposit_{iban}_{int(deposit.deposit_date)}.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(deposit.to_json(), file, indent=4)

    return deposit.deposit_signature