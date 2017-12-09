# coding=utf-8
from datetime import datetime


class Person:
    """Class holding data about a single accommodated person"""

    def __init__(
            self,
            name: str,
            code: str,
            gender: str,
            date_of_birth: datetime,
            birthplace: str,
            workspace: str,
            date_added=datetime.now()):
        """Basic constructor"""
        if name is None or len(name) == 0:
            raise ValueError(f'Person must have a name, but got {name}')

        if code is None or len(code) == 0:
            raise ValueError(f'Person must have a code, but got {code}')

        if gender is None or len(gender) != 1:
            raise ValueError(f'Person must have a one letter gender [m, f], but got {gender}')

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

    def to_json(self) -> dict:
        """
        :return: Person as JSON object
        """
        return {
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
            json['workspace']
        )

    def __ge__(self, other) -> bool:
        """Person is sooner in alphabetical sorting of names"""
        return type(self) == type(other) and \
               self.name > other.name

    def __eq__(self, other) -> bool:
        """Parameter is the same person"""
        return type(self) == type(other) and \
               self.code == other.code and \
               self.name == other.name and \
               self.gender == other.gender and \
               self.date_of_birth == other.date_of_birth

    def __hash__(self) -> int:
        """Simple comparison based on unique code hash"""
        return hash(self.code)

    def __str__(self) -> str:
        """Person details"""
        return f'Name: {self.name}, ' \
               f'Code: {self.code}, ' \
               f'Gender: {self.gender}, ' \
               f'Workspace: {self.workspace}, ' \
               f'Date Of Birth: {self.date_of_birth}, ' \
               f'Birthplace: {self.birthplace}, ' \
               f'Added: {self.date_added}'

    __repr__ = __str__
