from datetime import datetime


class Person:
    """Class holdin data about a single accommodated person"""

    def __init__(self, name: str, code: str, date_of_birth: datetime, birthplace: str, workspace: str):
        """Basic constructor"""
        if name is None or len(name) == 0:
            raise ValueError(f'Person must have a name, but got {name}')

        if code is None or len(code) == 0:
            raise ValueError(f'Person must have a code, but got {code}')

        self.name = name
        self._code = code
        self.workspace = workspace
        self.date_of_birth = date_of_birth
        self.birthplace = birthplace
        self.date_added = datetime.now()

    def refresh_added_date(self) -> None:
        """Reset the date the user was added to the current one"""
        self.date_added = datetime.now()

    @property
    def code(self) -> str:
        """Get unique code of the person"""
        return self._code

    def __ge__(self, other) -> bool:
        """Person is sooner in alphabetical sorting of names"""
        return type(self) == type(other) and \
               self.name > other.name

    def __eq__(self, other) -> bool:
        """Parameter is the same person"""
        return type(self) == type(other) and \
               self.code == other.code and \
               self.name == other.name and \
               self.date_of_birth == other.date_of_birth

    def __hash__(self) -> int:
        """Simple comparison based on unique code hash"""
        return hash(self.code)

    def __str__(self) -> str:
        return f'Name: {self.name}, ' \
               f'Code: {self._code}, ' \
               f'Workspace: {self.workspace}, ' \
               f'Date Of Birth: {self.date_of_birth}, ' \
               f'Birthplace: {self.birthplace}, ' \
               f'Added: {self.date_added}'

    __repr__ = __str__
