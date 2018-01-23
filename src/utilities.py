# coding=utf-8
import atexit
import sys

from flask import render_template

from src import webapp
from src.building import Building


def get_building_by_id(identifier: str, buildings: [Building]) -> Building:
    """
    :param identifier: id of building
    :param buildings: list with buildings to search
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


def is_logged_out() -> bool:
    """
    :return: user is not logged in
    """
    return not webapp.user_code and not webapp.data_file


def logout_user():
    """ Logs out user out of the system """
    atexit._run_exitfuncs()
    atexit._clear()

    webapp.user_code = ''
    webapp.data_file = ''
    webapp.buildings = []


def error_checked(attempt: function(), error_message: str) -> any:
    try:
        return attempt()

    except Exception as error:
        print(error, file=sys.stderr)
        return render_template('error.html', error=error_message)
