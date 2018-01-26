# coding=utf-8
import uuid

from src.entity.dwelling import Dwelling


class Building:
    """Building as a list of dwellings"""

    def __init__(self, street: str, number: int, dwellings: [Dwelling] = None, identifier: str = None):
        if dwellings is None:
            dwellings = []

        if number < 0:
            raise ValueError(f'You must provide non negative street number, got {number}')

        if not identifier or not identifier.strip():
            identifier = str(uuid.uuid4())

        self._id = identifier
        self._street = street
        self._number = int(number)
        self._dwellings = dwellings

    @property
    def id(self) -> str:
        """Get the building id """
        return self._id

    @property
    def street(self) -> str:
        """Get the building street"""
        return self._street

    @street.setter
    def street(self, value: str) -> None:
        """Set the building street"""
        self._street = value

    @property
    def number(self) -> int:
        """Get the building number"""
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        """Set the building number"""
        self._number = value

    @property
    def dwellings(self) -> list:
        """Get the buildings dwellings"""
        return self._dwellings

    def filter_dwellings(self, dwelling_filter: str) -> [Dwelling]:
        """
        :return: Dwellings only matching provided parameters
        """

        return list(
            filter(
                lambda dwelling:
                dwelling_filter in str(dwelling) or
                dwelling_filter in str(dwelling.free_spaces()) or
                dwelling_filter in ''.join([str(person) for person in dwelling.people]),
                self.dwellings
            )
        )

    def to_json(self) -> dict:
        """
        :return: Building as a JSON object
        """
        return {
            'id': self.id,
            'street': self.street,
            'number': self.number,
            'dwellings': list(map(lambda dwelling: dwelling.to_json(), self.dwellings))
        }

    @staticmethod
    def from_json(json: dict):
        """
        :return: Building object created from json
        """
        if json['dwellings'] is None:
            json['dwellings'] = []

        if not isinstance(json['dwellings'], list):
            json['dwellings'] = [dict(json['dwellings'])]

        return Building(
            json['street'],
            int(json['number']),
            list(map(lambda dwelling: Dwelling.from_json(dwelling), json['dwellings'])),
            json['id']
        )

    def __ge__(self, other) -> bool:
        """The name of the building is sooner after alphabetical sort"""
        return str(self) > str(other)

    def __eq__(self, other) -> bool:
        """Building is same"""
        return type(self) == type(other) and \
               self.id == other.id and \
               self.street == other.street and \
               self.number == other.number

    def __hash__(self) -> int:
        """Hash based on building id"""
        return hash(self.id)

    def __str__(self):
        """Basic building identifier"""
        return f'{self._street} {self.number}'

    __repr__ = __str__
