"""MODULE: transfer_request. Contains the transfer request class"""
import hashlib
import json
from datetime import datetime, timezone


class InvalidTransferRequest(Exception):
    """Custom exception for invalid transfer requests"""
    pass

class TransferRequest:
    """Class representing a transfer request"""
    def __init__(self,
                 from_iban: str,
                 transfer_type: str,
                 to_iban:str,
                 transfer_concept:str,
                 transfer_date:str,
                 transfer_amount:float):
        self.__from_iban = from_iban
        self.__to_iban = to_iban
        self.__transfer_type = transfer_type
        self.__concept = transfer_concept
        self.__transfer_date = transfer_date
        self.__transfer_amount = transfer_amount
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
    def from_iban(self):
        """Sender's iban"""
        return self.__from_iban

    @from_iban.setter
    def from_iban(self, value):
        self.__from_iban = value

    @property
    def to_iban(self):
        """receiver's iban"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def transfer_type(self):
        """Property representing the type of transfer: REGULAR, INMEDIATE or URGENT """
        return self.__transfer_type
    @transfer_type.setter
    def transfer_type(self, value):
        self.__transfer_type = value

    @property
    def transfer_amount(self):
        """Property respresenting the transfer amount"""
        return self.__transfer_amount
    @transfer_amount.setter
    def transfer_amount(self, value):
        self.__transfer_amount = value

    @property
    def transfer_concept(self):
        """Property representing the transfer concept"""
        return self.__transfer_concept
    @transfer_concept.setter
    def transfer_concept(self, value):
        self.__transfer_concept = value

    @property
    def transfer_date( self ):
        """Property representing the transfer's date"""
        return self.__transfer_date
    @transfer_date.setter
    def transfer_date( self, value ):
        self.__transfer_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def transfer_code(self):
        """Returns the md5 signature (transfer code)"""
        return hashlib.md5(str(self).encode()).hexdigest()


def transfer_request(from_iban: str, to_iban: str, concept: str, type: str, date: str, amount: float) -> str:
    try:
        transfer = TransferRequest(from_iban, to_iban, type, concept, date, amount)
        transfer_data = transfer.to_json()

        file_name = "transfers.json"
        try:
            with open(file_name, "r") as f:
                transfers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            transfers = []

        if any(t["transfer_code"] == transfer.transfer_code for t in transfers):
            raise InvalidTransferRequest("Duplicate transfer detected")

        transfers.append(transfer_data)
        with open(file_name, "w") as f:
            json.dump(transfers, f, indent=4)

        return transfer.transfer_code
    except InvalidTransferRequest as e:
        return str(e)