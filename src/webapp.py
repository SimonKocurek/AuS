# coding=utf-8
import os
import sys

import easygui
from flask import Flask, render_template, request, json, send_from_directory

from src.building import Building
from src.dwelling import Dwelling
from src.filemanager import FileManager

app = Flask(__name__, template_folder='../html')
buildings: [Building] = []


def get_building_by_id(identifier: str) -> Building:
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


@app.route('/favicon.ico')
def favicon():
    """
    :return: Favicon icon
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route("/", methods=['GET'])
def index():
    """ Starting page for selecting building """
    return render_template('index.html', buildings=buildings)


@app.route('/search', methods=['POST'])
def search():
    """ Returns only filtered out buildings """
    content = request.form['filter']

    filtered_buildings = [building
                          for building in buildings
                          if content in building.street or content in str(building.number)]

    return render_template('index.html', buildings=filtered_buildings)


@app.route("/load", methods=['GET'])
def load_buildings():
    """ Load buildings from external xml file """
    filename = easygui.fileopenbox('File to load xml content from', 'Save file', filetypes=['xml'])

    loaded_buildings = FileManager.load_buildings_from_xml(filename)

    global buildings
    if loaded_buildings:
        buildings = loaded_buildings

    return render_template('index.html', buildings=buildings)


@app.route('/save', methods=['GET'])
def save_buildings():
    """ Save buildings to external xml file """
    filename = easygui.filesavebox('File to save xml content', 'Save file')

    FileManager.save_file_as_xml(filename, buildings)

    return render_template('index.html', buildings=buildings)


@app.route("/", methods=['POST'])
def add_building():
    """ Add new building """
    buildings.append(Building('No street', 0))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=['DELETE'])
def delete_building():
    """ Delete a building """
    data = dict(request.form)
    identifier = data['id'][0]

    try:
        building = get_building_by_id(identifier)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    buildings.remove(building)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=['PUT'])
def update_buildings():
    """ Change building details """
    data = dict(request.form)
    identifier = data['id'][0]
    street = data['street'][0].strip()
    number = int(data['number'][0])

    try:
        building = get_building_by_id(identifier)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    building.street = street
    building.number = non_negative(number)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/building/<building_id>", methods=['GET'])
def building_screen(building_id: str):
    """ Page showing fist building """
    building = get_building_by_id(building_id)

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)


@app.route("/building/<building_id>", methods=['POST'])
def add_dwelling(building_id: str):
    """ Adds dwelling to the building """
    building = get_building_by_id(building_id)

    building.dwellings.append(Dwelling('A', 0, 0, 'A', 1))

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)
