# coding=utf-8
import os
import sys

from flask import Flask, render_template, send_from_directory

from src.building import Building
from src.business import Business
from src.utilities import error_checked

app = Flask(__name__, template_folder='../html')

buildings: [Building] = []
user_code: str = ''
data_file: str = ''

filter: str = ''
sort_type: str = ''


#########
# Imports
#########

@app.route('/favicon.ico')
def favicon():
    """
    :return: Favicon icon
    """
    return send_from_directory(app.template_folder, 'favicon.png')


@app.route('/style.css')
def style():
    """
    :return: Styles file
    """
    return send_from_directory(app.template_folder, 'style.css')


@app.route('/bootstrap.css')
def bootstrap_styles():
    """
    :return: Bootstrap looks
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'bootstrap.min.css')


@app.route('/bootstrap.js')
def bootstrap_javascript():
    """
    :return: Bootstrap code
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'bootstrap.min.js')


@app.route('/jquery.js')
def jquery():
    """
    :return: Jquery code
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'jquery-3.2.1.slim.min.js')


@app.route('/popper.js')
def popper():
    """
    :return: Popper code
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'popper.min.js')


#######
# Login
#######

@app.route('/', methods=['GET'])
def index():
    """ Intro page header """
    return error_checked(Business.index, 'Zlyhalo získavanie úvodnej stránky.')


@app.route('/', methods=['POST'])
def login():
    """ Logging using Intro page """
    return error_checked(Business.login, 'Zlyhalo prihlasovanie.')


######
# Menu
######

@app.route('/menu', methods=['GET'])
def menu():
    """ Starting page for selecting building """
    return error_checked(Business.menu, 'Zlyhalo získavanie budov.')


@app.route('/odhlasit', methods=['POST'])
def logout():
    """ Returns only filtered out buildings """
    return error_checked(Business.logout, 'Zlyhalo odhlasovanie.')


@app.route('/nacitat', methods=['POST'])
def load_buildings():
    """ Load buildings from external xml file """
    return error_checked(Business.load_buildings, 'Zlyhalo načítanie z XML súboru.')


@app.route('/ulozit', methods=['POST'])
def save_buildings():
    """ Save buildings to external xml file """
    return error_checked(Business.save_buildings, 'Zlyhalo ukladanie XML súboru.')


@app.route('/menu/filter', methods=['POST'])
def filter_buildings():
    """ Set buildings filter """
    return error_checked(Business.filter_buildings, 'Zlyhalo nastavovanie vyhľadávacieho filtera.')


@app.route('/menu/triedit', methods=['POST'])
def sort_buildings():
    """ Set buildings sorting method """
    return error_checked(Business.sort_buildings, 'Zlyhalo nastavenie triediacej podmienky.')


###########
# Buildings
###########

@app.route('/menu/budova/pridat', methods=['POST'])
def add_building():
    """ Add new building """
    return error_checked(Business.add_building, 'Zlyhalo vytvaranie novej budovy.')


@app.route('/menu/budova/<building_id>/zmazat', methods=['POST'])
def delete_building(building_id: str):
    """ Delete a building """
    return error_checked(Business.delete_building, 'Zlyhalo mazanie budovy.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>/update', methods=['POST'])
def update_buildings(building_id: str):
    """ Change building details """
    return error_checked(Business.update_buildings, 'Zlyhala zmena údajov budovy.', {'building_id': building_id})


###############
# Building menu
###############

@app.route('/menu/budova/<building_id>', methods=['GET'])
def building_screen(building_id: str):
    """ Page showing fist building """
    return error_checked(Business.building_screen, 'Zlyhala zmena údajov budovy.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>', methods=['POST'])
def add_dwelling(building_id: str):
    """ Adds dwelling to the building """
    return error_checked(Business.add_dwelling, 'Zlyhala zmena údajov budovy.', {'building_id': building_id})


################
# Error handling
################

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('error.html', error='404 Stránka sa nenašla.')


@app.errorhandler(Exception)
def webapp_error(error):
    print(error, file=sys.stderr)
    return render_template('error.html', error='500 Nastala chyba servera.')
