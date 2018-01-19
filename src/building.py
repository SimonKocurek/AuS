# coding=utf-8
import math
import uuid
from collections import OrderedDict
from functools import reduce

from src.dwelling import Dwelling
from src.person import Person


class Building:
    """Building as a list of dwellings"""

    def __init__(self, street: str, number: int, dwellings: [Dwelling] = None, identifier: str = None):
        if dwellings is None:
            dwellings = []

        if street is None or len(street) == 0:
            raise ValueError('You must provide a street name for the building')

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

    def filter_dwellings(self,
                         block: str = None,
                         floor: int = None,
                         cell: int = None,
                         room: str = None,
                         space: int = None,
                         people: [Person] = None,
                         minimum_free_spaces: int = 0,
                         maximum_free_spaces: int = math.inf) -> [Dwelling]:
        """
        :param block: Block to find dwellings from
        :param floor: Floor to find dwellings from
        :param cell: Cell to find dwellings from
        :param room: Find rooms with same id
        :param space: Find rooms with same amount of space
        :param people: Find dwellings these people live in
        :param minimum_free_spaces: The lowest number of free spaces in a dwelling (inclusive)
        :param maximum_free_spaces: The highest number of free spaces in a dwelling (inclusive)
        :return: Dwellings only matching provided parameters
        """

        result = self.dwellings

        if block:
            result = list(filter(lambda dwelling: dwelling.block == block, result))

        if floor:
            result = list(filter(lambda dwelling: dwelling.floor == floor, result))

        if cell:
            result = list(filter(lambda dwelling: dwelling.cell == cell, result))

        if room:
            result = list(filter(lambda dwelling: dwelling.room == room, result))

        if space:
            result = list(filter(lambda dwelling: dwelling.space == space, result))

        if people:
            result = list(filter(lambda dwelling: self.contains_person(people), result))

        if minimum_free_spaces:
            result = list(filter(lambda dwelling: dwelling.free_spaces() >= minimum_free_spaces, result))

        if maximum_free_spaces:
            result = list(filter(lambda dwelling: dwelling.free_spaces() <= maximum_free_spaces, result))

        return result

    def contains_person(self, searched: [Person]) -> bool:
        """
        :return: Searched contains a person from people
        """
        for person in self.all_people():
            if person in searched:
                return True
        return False

    def all_people(self) -> [Person]:
        """
        :return: All people living in this building
        """
        return list(set(
            reduce(lambda result, people: result + people, list(
                map(lambda dwelling: dwelling.people, self._dwellings)))))

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
