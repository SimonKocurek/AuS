# coding=utf-8
import sys
from flask import Flask, render_template, request, json

from src.building import Building

# Class can't be used here as Flask Framework is based on pure file approach
app = Flask(__name__, template_folder='../html')
buildings: [Building] = []


def get_building_by_id(id: str) -> Building:
    building = next((b for b in buildings if b.id == id), None)

    if not building:
        raise ValueError(f'Building with id {id} could not be found.')

    return building

@app.route("/", methods=['GET'])
def index():
    """ Starting page for selecting building """
    return render_template('index.html', buildings=buildings)


@app.route("/", methods=['PUT'])
def add_building():
    """ Add new building """
    buildings.append(Building('No street', 0))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=['DELETE'])
def delete_building():
    """ Delete a building """
    data = dict(request.form)
    id = data['id'][0]

    try:
        building = get_building_by_id(id)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    buildings.remove(building)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=['POST'])
def update_buildings():
    """ Change building details """
    data = dict(request.form)
    id = data['id'][0]
    street = data['street'][0].strip()
    number = int(data['number'][0])

    try:
        building = get_building_by_id(id)
    except ValueError as error:
        print(error, file=sys.stderr)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    building.street = street
    building.number = number

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/building/<building_id>")
def building_screen(building_id: str):
    """ Page showing fist building """
    building = get_building_by_id(building_id)

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)
