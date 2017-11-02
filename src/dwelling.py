from src.person import Person


class Dwelling:
    """Class holding data about a one room"""

    def __init__(self, block: str, floor: int, cell: int, room: str, space: int, people=None):
        """Basic constructor"""

        if people is None:
            people = []

        if len(block) != 1:
            raise ValueError(f'Block shoul be one letter, but got {block}')

        if space <= 0:
            raise ValueError(f'Dwelling must be able to accommodate at least 1 person, but got {space}')

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
        self._people.clear()

    def free_spaces(self) -> int:
        """
        :return: Number of people that can still fit inside the dwelling
        """
        return len(self._people) - self._space

    @property
    def block(self) -> str:
        """Get dwelling block"""
        return self._block

    @property
    def floor(self) -> int:
        """Get floor number of dwelling"""
        return self._floor

    @property
    def cell(self) -> int:
        """Get dwelling cell number"""
        return self._cell

    @property
    def room(self) -> str:
        """Get dwelling room id"""
        return self._room

    @property
    def space(self) -> int:
        """Get maximum number of people that can live inside the dwelling"""
        return self._space

    @property
    def people(self) -> [Person]:
        """Get people living in the dwelling"""
        return self._people

    def to_json(self) -> dict:
        """
        :return: Dwelling as a JSON object
        """
        return {
            'block': self.block,
            'floor': self.floor,
            'cell': self.cell,
            'room': self.room,
            'space': self.space,
            'people': list(map(lambda person: person.to_json(), self._people))
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
            map(lambda person: Person.from_json(person), json['people'])
        )

    def __gt__(self, other) -> bool:
        """Dwelling is sooner in alphabetical sorting"""
        return type(self) == type(other) and \
               str(self) > str(other)

    def __eq__(self, other) -> bool:
        """Dwelling is same as parameter"""
        return type(self) == type(other) and \
               self._block == other.block and \
               self._floor == other.floor and \
               self._cell == other.cell and \
               self.room == other.room

    def __hash__(self) -> int:
        """Create hash from dwelling identifier"""
        return hash(str(self))

    def __str__(self) -> str:
        """Exapmpe: A 223B"""
        return f'{self._block} {self._floor}{self._cell}{self._room}'

    __repr__ = __str__
