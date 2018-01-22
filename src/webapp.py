# coding=utf-8
import atexit
import os
import sys

import easygui
from flask import Flask, render_template, request, json, send_from_directory, redirect, url_for

from src.building import Building
from src.dwelling import Dwelling
from src.filemanager import FileManager
from src.utilities import get_building_by_id, non_negative

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
    """ Intro page """
    return render_template('index.html')


@app.route('/', methods=['POST'])
def login():
    """ Logging using Intro page """
    global user_code
    user_code = request.form.get('inputCode', default='', type=str)

    global data_file
    data_file = f'../{user_code}.json'

    global buildings
    buildings = FileManager.load_buildings(data_file)
    atexit.register(lambda: FileManager.write_file(data_file, buildings))

    return redirect(url_for('menu'), code=307)


######
# Menu
######

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    """ Starting page for selecting building """
    return render_template('menu.html', buildings=buildings)


@app.route('/search', methods=['GET'])
def search():
    """ Returns only filtered out buildings """
    content = request.args.get('filter', default=None, type=str)

    filtered_buildings = [building
                          for building in buildings
                          if content in building.street or content in str(building.number)]

    return render_template('menu.html', buildings=filtered_buildings)


@app.route('/logout', methods=['POST'])
def logout():
    """ Returns only filtered out buildings """
    global user_code
    global data_file
    global buildings

    if data_file and buildings:
        FileManager.write_file(data_file, buildings)

    user_code = ''
    data_file = ''
    buildings = []

    return redirect('/')


@app.route('/load', methods=['POST'])
def load_buildings():
    """ Load buildings from external xml file """
    filename = easygui.fileopenbox('File to load xml content from', 'Save file', filetypes=['xml'])

    loaded_buildings = FileManager.load_buildings_from_xml(filename)

    global buildings
    if loaded_buildings:
        buildings = loaded_buildings

    return redirect(url_for('menu'))


@app.route('/save', methods=['POST'])
def save_buildings():
    """ Save buildings to external xml file """
    filename = easygui.filesavebox('File to save xml content', 'Save file')

    FileManager.save_file_as_xml(filename, buildings)

    return redirect(url_for('menu'))


###########
# Buildings
###########

@app.route('/menu/building', methods=['POST'])
def add_building():
    """ Add new building """
    buildings.append(Building('No street', 0))
    return redirect(url_for('menu'))


@app.route('/menu/building', methods=['DELETE'])
def delete_building():
    """ Delete a building """
    data = dict(request.form)
    identifier = data['id'][0]

    try:
        building = get_building_by_id(identifier, buildings)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    buildings.remove(building)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/', methods=['PUT'])
def update_buildings():
    """ Change building details """
    data = dict(request.form)
    identifier = data['id'][0]
    street = data['street'][0].strip()
    number = int(data['number'][0])

    try:
        building = get_building_by_id(identifier, buildings)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    building.street = street
    building.number = non_negative(number)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/building/<building_id>', methods=['GET'])
def building_screen(building_id: str):
    """ Page showing fist building """
    building = get_building_by_id(building_id)

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)


@app.route('/building/<building_id>', methods=['POST'])
def add_dwelling(building_id: str):
    """ Adds dwelling to the building """
    building = get_building_by_id(building_id)

    building.dwellings.append(Dwelling('A', 0, 0, 'A', 1))

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)
