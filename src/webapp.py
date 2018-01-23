# coding=utf-8
import os
import sys

import easygui
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

from src.building import Building
from src.business import Business
from src.dwelling import Dwelling
from src.filemanager import FileManager
from src.utilities import get_building_by_id, non_negative, is_logged_out, logout_user, error_checked

app = Flask(__name__, template_folder='../html')

buildings: [Building] = []
user_code: str = None
data_file: str = None


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

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    """ Starting page for selecting building """
    return error_checked(Business.menu, 'Zlyhalo získavanie budov.')


@app.route('/search', methods=['GET'])
def search():
    """ Returns only filtered out buildings """
    if is_logged_out():
        return redirect('/')

    content = request.args.get('filter', default=None, type=str)

    filtered_buildings = [building
                          for building in buildings
                          if content in building.street or content in str(building.number)]

    return render_template('menu.html', buildings=filtered_buildings)


@app.route('/sort', methods=['GET'])
def sort():
    """

    :return:
    """
    pass


@app.route('/logout', methods=['POST'])
def logout():
    """ Returns only filtered out buildings """
    if is_logged_out():
        return redirect('/')

    logout_user()
    return redirect('/')


@app.route('/load', methods=['POST'])
def load_buildings():
    """ Load buildings from external xml file """
    if is_logged_out():
        return redirect('/')

    filename = easygui.fileopenbox('File to load xml content from', 'Save file', filetypes=['xml'])

    loaded_buildings = FileManager.load_buildings_from_xml(filename)

    global buildings
    if loaded_buildings:
        buildings = loaded_buildings

    return redirect(url_for('menu'))


@app.route('/save', methods=['POST'])
def save_buildings():
    """ Save buildings to external xml file """
    if is_logged_out():
        return redirect('/')

    filename = easygui.filesavebox('File to save xml content', 'Save file')

    FileManager.save_file_as_xml(filename, buildings)

    return redirect(url_for('menu'))


###########
# Buildings
###########

@app.route('/menu/building/add', methods=['POST'])
def add_building():
    """ Add new building """
    if is_logged_out():
        return redirect('/')

    buildings.append(Building('', 0))
    return redirect(url_for('menu'))


@app.route('/menu/building/<building_id>/delete', methods=['POST'])
def delete_building(building_id: str):
    """ Delete a building """
    if is_logged_out():
        return redirect('/')

    try:
        building = get_building_by_id(building_id, buildings)
        buildings.remove(building)

    except ValueError as error:
        print(error, file=sys.stderr)
        return render_template('error.html', error='Zlyhalo mazanie budovy')

    return redirect(url_for('menu'))


@app.route('/menu/building/<building_id>/update', methods=['POST'])
def update_buildings(building_id: str):
    """ Change building details """
    if is_logged_out():
        return redirect('/')

    try:
        building = get_building_by_id(building_id, buildings)

        street = request.form.get('street', default='', type=str)
        number = request.form.get('number', default=0, type=int)

        building.street = street
        building.number = non_negative(number)

    except ValueError as error:
        print(error, file=sys.stderr)
        return render_template('error.html', error='Zlyhalo update-ovanie budovy')

    return redirect(url_for('menu'))


###############
# Building menu
###############

@app.route('/menu/building/<building_id>', methods=['GET'])
def building_screen(building_id: str):
    """ Page showing fist building """
    building = get_building_by_id(building_id)

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)


@app.route('/menu/building/<building_id>', methods=['POST'])
def add_dwelling(building_id: str):
    """ Adds dwelling to the building """
    building = get_building_by_id(building_id)

    building.dwellings.append(Dwelling('A', 0, 0, 'A', 1))

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)
