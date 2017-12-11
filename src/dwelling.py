# coding=utf-8
import uuid

from src.person import Person


class Dwelling:
    """Class holding data about a one room"""

    def __init__(self, block: str,
                 floor: int,
                 cell: int,
                 room: str,
                 space: int,
                 people: [Person] = None,
                 id: str = str(uuid.uuid4())):
        """Basic constructor"""

        if people is None:
            people = []

        if len(block) != 1:
            raise ValueError(f'Block shoul be one letter, but got {block}')

        if space <= 0:
            raise ValueError(f'Dwelling must be able to accommodate at least 1 person, but got {space}')

        self._id = id
        self._block = block.upper()
        self._floor = floor
        self._cell = cell
        self._room = room
        self._space = space
        self._people = people

    def add_person(self, person: Person) -> None:
        """
        Adds person to the dwelling
        :param person: Person to add
        """
        if person in self._people:
            raise ValueError(f'Person {person} is already inside dwelling {self}')

        if self.free_spaces() <= 0:
            raise ValueError(f'Can\'t add another person to dwelling {self}. It\'s already full')

        self._people.append(person)

    def remove_person(self, person: Person) -> None:
        """
        Person to remove from the dwelling
        :param person: Person to remove
        """
        if person not in self._people:
            raise ValueError(f'Person {person} isn\'t inside dwelling {self}')

        self._people.remove(person)

    def empty(self) -> None:
        """Empties the dwelling by removing all people from it"""
        self.people.clear()

    def free_spaces(self) -> int:
        """
        :return: Number of people that can still fit inside the dwelling
        """
        return self._space - len(self._people)

    @property
    def id(self) -> str:
        """Get dwelling id"""
        return self._id

    @property
    def block(self) -> str:
        """Get dwelling block"""
        return self._block

    @block.setter
    def block(self, value: str) -> None:
        """Set dwelling block"""
        self._block = value

    @property
    def floor(self) -> int:
        """Get floor number of dwelling"""
        return self._floor

    @floor.setter
    def floor(self, value: int) -> None:
        """Set dwelling floor"""
        self._floor = value

    @property
    def cell(self) -> int:
        """Get dwelling cell number"""
        return self._cell

    @cell.setter
    def cell(self, value: int) -> None:
        """Set dwelling cell number"""
        self._cell = value

    @property
    def room(self) -> str:
        """Get dwelling room id"""
        return self._room

    @room.setter
    def room(self, value: str) -> None:
        """Set dwelling room id"""
        self._room = value

    @property
    def space(self) -> int:
        """Get maximum number of people that can live inside the dwelling"""
        return self._space

    @space.setter
    def space(self, value: int) -> None:
        """Set maximum number of people that can live inside the dwelling"""
        self._space = value

    @property
    def people(self) -> [Person]:
        """Get people living in the dwelling"""
        return self._people

    def to_json(self) -> dict:
        """
        :return: Dwelling as a JSON object
        """
        return {
            'id': self.id,
            'block': self.block,
            'floor': self.floor,
            'cell': self.cell,
            'room': self.room,
            'space': self.space,
            'people': list(map(lambda person: person.to_json(), self.people))
        }

    @staticmethod
    def from_json(json: dict):
        """
        :return: Dwelling object created from json
        """
        if json['people'] is None:
            json['people'] = []

        return Dwelling(
            json['block'],
            json['floor'],
            json['cell'],
            json['room'],
            json['space'],
            list(map(lambda person: Person.from_json(person), json['people'])),
            json['id']
        )

    def __gt__(self, other) -> bool:
        """Dwelling is sooner in alphabetical sorting"""
        return type(self) == type(other) and \
               str(self) > str(other)

    def __eq__(self, other) -> bool:
        """Dwelling is same as parameter"""
        return type(self) == type(other) and \
               self.id == other.id and \
               self.block == other.block and \
               self.floor == other.floor and \
               self.cell == other.cell and \
               self.room == other.room

    def __hash__(self) -> int:
        """Create hash from dwelling id"""
        return hash(self.id)

    def __str__(self) -> str:
        """Exapmpe: A 223B"""
        return f'{self._block} {self._floor}{self._cell}{self._room}'

    __repr__ = __str__
