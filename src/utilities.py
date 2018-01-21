from src.building import Building


def get_building_by_id(identifier: str, buildings: [Building]) -> Building:
    """
    :param identifier: id of building
    :return: Building with specified id
    """
    building = next((b for b in buildings if b.id == identifier), None)

    if not building:
        raise ValueError(f'Building with id {id} could not be found.')

    return building


def non_negative(number: int) -> int:
    """
    :return: Number, or 0 if number is negative
    """
    return max(0, number)
