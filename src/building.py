# coding=utf-8
from functools import reduce

from src.dwelling import Dwelling
from src.person import Person


class Building:
    """Building as a list of dwellings"""

    def __init__(self, street: str, number: int, dwellings=None):

        if dwellings is None:
            dwellings = []

        if street is None or len(street) == 0:
            raise ValueError('You must provide a street name for the building')

        self._street = street
        self._number = number
        self._dwellings = dwellings

    @property
    def street(self) -> str:
        """Get the building street"""
        return self._street

    @property
    def number(self) -> int:
        """Get the building number"""
        return self._number

    @property
    def dwellings(self) -> list:
        """Get the buildings dwellings"""
        return self._dwellings

    def get_by_block(self, block: str):
        """

        :param block:
        :return:
        """
        return filter(lambda dwelling: dwelling.block == block, self._dwellings)

    def get_by_floor(self, block: str):
        """

        :param block:
        """
        pass

    def free_blocks(self):
        """

        """
        pass

    def free_cells(self, block):
        """

        :param block:
        """
        pass

    def free_rooms(self, block):
        """

        :param block:
        """
        pass

    def free_spaces(self):
        """
        :return: Number of free spaces in the building
        """
        pass

    def all_people(self) -> [Person]:
        """
        :return: All people living in this building
        """
        return reduce(
            lambda result, people: result + people,
            list(
                map(
                    lambda dwelling: dwelling.people,
                    self._dwellings)))

    def to_json(self) -> dict:
        """
        :return: Building as a JSON object
        """
        return {
            'street': self._street,
            'number': self._number,
            'dwellings': list(map(lambda dwelling: dwelling.to_json(), self._dwellings))
        }

    @staticmethod
    def from_json(json: dict):
        """
        :return: Building object created from json
        """
        if json['dwellings'] is None:
            json['dwellings'] = []

        return Building(
            json['street'],
            json['number'],
            map(lambda dwelling: Dwelling.from_json(dwelling), json['dwellings'])
        )

    def __ge__(self, other) -> bool:
        """The name of the building is sooner after alphabetical sort"""
        return str(self) > str(other)

    def __eq__(self, other) -> bool:
        """Building is same"""
        return str(self) == str(other)

    def __hash__(self) -> int:
        """Hash based on building number"""
        return self._number

    def __str__(self):
        """Basic buiding identifier"""
        return f'{self._street} {self._number}'

    __repr__ = __str__
