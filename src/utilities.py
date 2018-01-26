# coding=utf-8
import atexit
import sys
import traceback

from flask import render_template, redirect

from src import webapp
from src.entity.building import Building
from src.entity.dwelling import Dwelling


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


def get_building_from_args(args: dict) -> Building:
    """ Extract building from dictionary containing needed identifiers """
    building_id = args['building_id']
    return get_building_by_id(building_id, webapp.buildings)


def get_dwellings_from_args(args: dict) -> [Dwelling]:
    """ Extract dwelling list from dictionary containing needed identifiers """
    return get_building_from_args(args).dwellings


def get_dwelling_from_args(args: dict) -> Dwelling:
    """ Extract dwelling list from dictionary containing needed identifiers """
    for dwelling in get_building_from_args(args).dwellings:
        if dwelling.id == args['dwelling_id']:
            return dwelling

    raise IndexError


def positive(number: int) -> int:
    """
    :return: Number, or 1 if number is negative or 0
    """
    return max(1, number)


def non_negative(number: int) -> int:
    """
    :return: Number, or 0 if number is negative
    """
    return max(0, number)


def non_numeric(string: str) -> str:
    """ Removes all numbers from the string """
    return ''.join(letter for letter in string if not letter.isdigit())


def is_logged_out() -> bool:
    """
    :return: user is not logged in
    """
    return not webapp.user_code and not webapp.data_file


def logout_user():
    """ Logs out user out of the system """
    clear_state()


def clear_state():
    """ Sets the webapp state to the initial """
    atexit._run_exitfuncs()
    atexit._clear()

    webapp.user_code = ''
    webapp.data_file = ''
    webapp.buildings = []

    webapp.filter = ''
    webapp.sort_type = ''


def checked(attempt: callable, error_message: str, attempt_args: dict = None, check_login=True) -> any:
    """ Executes function with logging and error callback """
    try:
        if check_login and is_logged_out():
            return redirect('/')

        if attempt_args:
            return attempt(attempt_args)
        else:
            return attempt()

    except Exception as error:
        print(error, file=sys.stderr)
        traceback.print_exc()
        return render_template('error.html', error=error_message)


def redirect_with_query_params(url: str, **params):
    """ Function with provided query params """
    if len(params) == 0:
        return redirect(url)

    query_params = []
    for key, value in params.items():
        query_params.append(f'{key}={value}')

    return redirect(f'{ url }?{ "&".join(query_params) }')
