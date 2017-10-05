class Building(list):
    """Building as a list of dwellings"""

    def __init__(self, street: str, number: int):
        super().__init__()

    def free_blocks(self):
        pass

    def free_cells(self, block):
        pass

    def free_rooms(self, block):
        pass

    def free_spaces(self, block):
        pass

    def all_people(self):
        pass

    def all_people(self, block):
        pass

    def __ge__(self, x: List[_T]) -> bool:
        return super().__ge__(x)

    def __eq__(self, other) -> bool:
        pass

    def __hash__(self) -> int:
        return super().__hash__()

    def __str__(self):
        pass

    __repr__ = __str__
