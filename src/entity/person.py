# coding=utf-8
import uuid
from datetime import datetime


class Person:
    """Class holding data about a single accommodated person"""

    def __init__(self,
                 name: str = '',
                 code: str = '',
                 gender: str = 'm',
                 date_of_birth: datetime = None,
                 birthplace: str = '',
                 workspace: str = '',
                 date_added: datetime = None,
                 id: str = None):
        """Basic constructor"""
        if gender not in ['m', 'f']:
            raise ValueError(f'Person must have a one letter gender [m, f], but got {gender}')

        if id is None or len(id.strip()) == 0:
            id = str(uuid.uuid4())

        if not date_of_birth:
            date_of_birth = datetime.now()

        if not date_added:
            date_added = datetime.now()

        if not isinstance(date_of_birth, str):
            date_of_birth = date_of_birth.strftime('%Y-%m-%d')

        self._id = id
        self.name = name
        self.code = code
        self.gender = gender
        self.workspace = workspace
        self.date_of_birth = date_of_birth
        self.birthplace = birthplace
        self.date_added = date_added

    def refresh_added_date(self) -> None:
        """Reset the date the user was added to the current one"""
        self.date_added = datetime.now()

    @property
    def id(self) -> str:
        """Get the person id """
        return self._id

    @property
    def name(self) -> str:
        """Get the person name """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the person name """
        self._name = value

    @property
    def code(self) -> str:
        """Get the person code """
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        """Set the person code """
        self._code = value

    @property
    def gender(self) -> str:
        """Get the person name """
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        """Set the person name """
        if value not in ['m', 'f']:
            raise ValueError(f'Person must have a one letter gender [m, f], but got {value}')

        self._gender = value

    @property
    def workspace(self) -> str:
        """Get the person workspace """
        return self._workspace

    @workspace.setter
    def workspace(self, value: str) -> None:
        """Set the person workspace """
        self._workspace = value

    @property
    def date_of_birth(self) -> str:
        """Get the person date of birth """
        return self._date_of_birth.strftime('%Y-%m-%d')

    @date_of_birth.setter
    def date_of_birth(self, value: str) -> None:
        """Set the person date of birth """
        self._date_of_birth = datetime.strptime(value, '%Y-%m-%d')

    @property
    def birthplace(self) -> str:
        """Get the person birthplace """
        return self._birthplace

    @birthplace.setter
    def birthplace(self, value: str) -> None:
        """Set the person birthplace"""
        self._birthplace = value

    @property
    def date_added(self) -> str:
        """Get the person added date"""
        return self._date_added.strftime('%Y-%m-%d')

    @date_added.setter
    def date_added(self, value: datetime) -> None:
        """Set the person added date"""
        self._date_added = value

    def to_json(self) -> dict:
        """
        :return: Person as JSON object
        """
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'gender': self.gender,
            'date_of_birth': str(self.date_of_birth),
            'birthplace': self.birthplace,
            'workspace': self.workspace
        }

    @staticmethod
    def from_json(json: dict):
        """
        :return: Person object created from json
        """
        return Person(
            json['name'],
            json['code'],
            json['gender'],
            json['date_of_birth'],
            json['birthplace'],
            json['workspace'],
            id=json['id']
        )

    def __lt__(self, other) -> bool:
        """Person is sooner in alphabetical sorting of names"""
        return type(self) == type(other) and \
               self.name < other.name

    def __eq__(self, other) -> bool:
        """Parameter is the same person"""
        return type(self) == type(other) and \
               self._id == other.id and \
               self.code == other.code and \
               self.name == other.name and \
               self.gender == other.gender and \
               self.date_of_birth == other.date_of_birth

    def __hash__(self) -> int:
        """Simple comparison based on unique person id"""
        return hash(self._id)

    def __str__(self) -> str:
        """Person Name"""
        return self.name

    __repr__ = __str__
