# coding=utf-8
import os
import sys
import traceback

from flask import Flask, render_template, send_from_directory
from flask_jsglue import JSGlue

from src.business import Business
from src.entity.building import Building
from src.utilities import checked

app = Flask(__name__, template_folder='../html')
jsglue = JSGlue(app)

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
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'jquery-3.3.1.min.js')


@app.route('/popper.js')
def popper():
    """
    :return: Popper code
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'popper.min.js')


@app.route('/noty.js')
def noty():
    """
    :return: Notty javascript notifications code
    """
    return send_from_directory(os.path.join(app.template_folder, 'bootstrap'), 'noty.min.js')


@app.route('/menu.js')
def menu_javascript():
    """
    :return: Menu javascript code
    """
    return send_from_directory(os.path.join(app.template_folder, 'code'), 'menu.js')


@app.route('/building.js')
def building_javascript():
    """
    :return: Building javascript code
    """
    return send_from_directory(os.path.join(app.template_folder, 'code'), 'building.js')


@app.route('/dwelling.js')
def dwelling_javascript():
    """
    :return: Dwelling javascript code
    """
    return send_from_directory(os.path.join(app.template_folder, 'code'), 'dwelling.js')


#######
# Login
#######

@app.route('/', methods=['GET'])
def index():
    """ Intro page header """
    return checked(Business.index, 'Zlyhalo získavanie úvodnej stránky.', check_login=False)


@app.route('/', methods=['POST'])
def login():
    """ Logging using Intro page """
    return checked(Business.login, 'Zlyhalo prihlasovanie.', check_login=False)


######
# Menu
######

@app.route('/menu', methods=['GET'])
def menu():
    """ Starting page for selecting building """
    return checked(Business.menu, 'Zlyhalo získavanie budov.')


@app.route('/odhlasit', methods=['POST'])
def logout():
    """ Returns only filtered out buildings """
    return checked(Business.logout, 'Zlyhalo odhlasovanie.')


@app.route('/nacitat', methods=['POST'])
def load_buildings():
    """ Load buildings from external xml file """
    return checked(Business.load_buildings, 'Zlyhalo načítanie z XML súboru.')


@app.route('/ulozit', methods=['POST'])
def save_buildings():
    """ Save buildings to external xml file """
    return checked(Business.save_buildings, 'Zlyhalo ukladanie XML súboru.')


@app.route('/menu/filter', methods=['POST'])
def filter_buildings():
    """ Set buildings filter """
    return checked(Business.filter_buildings, 'Zlyhalo nastavovanie vyhľadávacieho filtera.')


@app.route('/menu/triedit', methods=['POST'])
def sort_buildings():
    """ Set buildings sorting method """
    return checked(Business.sort_buildings, 'Zlyhalo nastavenie triediacej podmienky.')


@app.route('/menu/budova/pridat', methods=['POST'])
def add_building():
    """ Add new building """
    return checked(Business.add_building, 'Zlyhalo vytvaranie novej budovy.')


@app.route('/menu/budova/<building_id>/zmazat', methods=['POST'])
def delete_building(building_id: str):
    """ Delete a building """
    return checked(Business.delete_building, 'Zlyhalo mazanie budovy.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>/update', methods=['POST'])
def update_building(building_id: str):
    """ Change building details """
    return checked(Business.update_building, 'Zlyhala zmena údajov budovy.', {'building_id': building_id})


###############
# Building menu
###############

@app.route('/menu/budova/<building_id>', methods=['GET'])
def building_screen(building_id: str):
    """ Page showing building detail """
    return checked(Business.building_screen, 'Zlyhalo načítanie izieb budovy.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>/filter', methods=['POST'])
def filter_dwellings(building_id: str):
    """ Set dwelling filter """
    return checked(Business.filter_dwellings, 'Zlyhalo nastavovanie vyhľadávacieho filtera.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>/triedit', methods=['POST'])
def sort_dwellings(building_id: str):
    """ Set dwelling sorting method """
    return checked(Business.sort_dwellings, 'Zlyhalo nastavenie triediacej podmienky.', {'building_id': building_id})


###########
# Dwellings
###########

@app.route('/menu/budova/<building_id>/pridat', methods=['POST'])
def add_dwelling(building_id: str):
    """ Adds dwelling to the building """
    return checked(Business.add_dwelling, 'Zlyhala tvorba izby.', {'building_id': building_id})


@app.route('/menu/budova/<building_id>/izba/<dwelling_id>/zmazat', methods=['POST'])
def delete_dwelling(building_id: str, dwelling_id: str):
    """ Delete a dwelling from building """
    return checked(Business.delete_dwelling, 'Zlyhalo mazanie izby.', {'building_id': building_id, 'dwelling_id': dwelling_id})


@app.route('/menu/budova/<building_id>/<dwelling_id>/update', methods=['POST'])
def update_dwelling(building_id: str, dwelling_id: str):
    """ Change dwelling details """
    return checked(Business.update_dwelling, 'Zlyhala zmena údajov izby.', {'building_id': building_id, 'dwelling_id': dwelling_id})


@app.route('/menu/budova/<building_id>/<dwelling_id>/update_info', methods=['POST'])
def update_dwelling_info(building_id: str, dwelling_id: str):
    """ Change dwelling details """
    return checked(Business.update_dwelling_info, 'Zlyhala zmena údajov izby.', {'building_id': building_id, 'dwelling_id': dwelling_id})


#################
# Dwelling Screen
#################

@app.route('/menu/budova/<building_id>/izba/<dwelling_id>', methods=['GET'])
def dwelling_screen(building_id: str, dwelling_id: str):
    """ Show details about dwelling """
    return checked(Business.dwelling_screen, 'Zlyhala zobrazovanie detailu izby.', {'building_id': building_id, 'dwelling_id': dwelling_id})


########
# People
########


@app.route('/menu/budova/<building_id>/izba/<dwelling_id>/pridaj_cloveka', methods=['POST'])
def add_person(building_id: str, dwelling_id: str):
    """ Add person to a dwelling """
    return checked(
        Business.add_person,
        'Zlyhalo pridávanie ľudí.',
        {'building_id': building_id, 'dwelling_id': dwelling_id}
    )


@app.route('/menu/budova/<building_id>/izba/<dwelling_id>/clovek/<person_id>', methods=['POST'])
def update_person(building_id: str, dwelling_id: str, person_id: str):
    """ Change person data """
    return checked(
        Business.update_person,
        'Zlyhala zmena údajov ubytovaného.',
        {'building_id': building_id, 'dwelling_id': dwelling_id, 'person_id': person_id}
    )


@app.route('/menu/budova/<building_id>/izba/<dwelling_id>/clovek/<person_id>/vyhod_cloveka', methods=['POST'])
def delete_person(building_id: str, dwelling_id: str, person_id: str):
    """ Remove a person from dwelling """
    return checked(
        Business.delete_person,
        'Zlyhalo mazanie ubytovaného.',
        {'building_id': building_id, 'dwelling_id': dwelling_id, 'person_id': person_id}
    )


################
# Error handling
################

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    traceback.print_exc()
    return render_template('error.html', error='404 Stránka sa nenašla.')


@app.errorhandler(Exception)
def webapp_error(error):
    print(error, file=sys.stderr)
    traceback.print_exc()
    return render_template('error.html', error='500 Nastala chyba servera.')
