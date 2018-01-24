# coding=utf-8
import atexit
import sys

from flask import render_template, redirect, url_for

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


def error_checked(attempt: callable, error_message: str, attempt_args: dict = None) -> any:
    """ Executes function with logging and error callback """
    try:
        if attempt_args:
            return attempt(attempt_args)
        else:
            return attempt()

    except Exception as error:
        print(error, file=sys.stderr)
        return render_template('error.html', error=error_message)


def redirect_with_query_params(function_name: str, **params):
    """ Function with provided query params"""
    if len(params) == 0:
        return redirect(url_for(function_name))

    query_params = []
    for key, value in params.items():
        query_params.append(f'{key}={value}')

    return redirect(f'{url_for(function_name)}?{"&".join(query_params)}')
