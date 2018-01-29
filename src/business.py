# coding=utf-8
import atexit

import easygui
from flask import render_template, request, redirect, url_for, jsonify

from src import webapp
from src.entity.building import Building
from src.entity.dwelling import Dwelling
from src.entity.person import Person
from src.filemanager import FileManager
from src.sorter import Sorter
from src.utilities import logout_user, non_negative, redirect_with_query_params, get_dwellings_from_args, get_building_from_args, \
    get_dwelling_from_args, non_numeric, positive, get_person_from_args


class Business:
    """ Implementations for webapp functions """

    @staticmethod
    def index():
        """ Intro page """
        return render_template('index.html')

    @staticmethod
    def login():
        """ Logging using Intro page """
        webapp.user_code = request.form.get('inputCode', default='', type=str)
        webapp.data_file = f'../data/{webapp.user_code}.json'
        webapp.buildings = FileManager.load_buildings(webapp.data_file)

        atexit.register(lambda: FileManager.write_file(webapp.data_file, webapp.buildings))

        return redirect(url_for('menu'))

    @staticmethod
    def menu(filter=None, sort_type=None):
        """ Starting page for selecting building """

        if filter is None:
            webapp.filter = request.args.get('filter', default='', type=str)
        else:
            webapp.filter = filter

        if sort_type is None:
            webapp.sort_type = request.args.get('triedenie', default='', type=str)
        else:
            webapp.sort_type = sort_type

        buildings = webapp.buildings.copy()

        if webapp.filter:
            buildings = [building for building in buildings if webapp.filter in str(building)]

        if webapp.sort_type:
            sorter = Sorter()
            sorter.sort(buildings, webapp.sort_type)

        return render_template('menu.html', buildings=buildings)

    @staticmethod
    def logout():
        """ Returns only filtered out buildings """
        logout_user()
        return redirect('/')

    @staticmethod
    def load_buildings():
        """ Load buildings from external xml file """
        filename = easygui.fileopenbox('File to load xml content from', 'Load file', filetypes=['xml'])

        loaded_buildings = FileManager.load_buildings_from_xml(filename)

        if loaded_buildings:
            webapp.buildings = loaded_buildings

        return Business.menu()

    @staticmethod
    def save_buildings():
        """ Save buildings to external xml file """
        filename = easygui.filesavebox('File to save xml content', 'Save file')

        FileManager.save_file_as_xml(filename, webapp.buildings)

        return jsonify(result='success')

    @staticmethod
    def filter_buildings():
        """ Set search filter for webapp """
        filter = request.form.get('filter', default='', type=str)

        return Business.menu(filter=filter)

    @staticmethod
    def sort_buildings():
        """ Set sort type for webapp """
        previous_sort_type = webapp.sort_type
        sort_type = request.form.get('triedenie', default='', type=str)

        if f'{sort_type}-asc' == previous_sort_type:
            sort_type = f'{sort_type}-desc'
        else:
            sort_type = f'{sort_type}-asc'

        return Business.menu(sort_type=sort_type)

    @staticmethod
    def add_building():
        """ Add new building """
        webapp.buildings.insert(0, Building('', 0))

        return Business.menu()

    @staticmethod
    def delete_building(args: dict):
        """ Delete a building """
        building = get_building_from_args(args)
        webapp.buildings.remove(building)

        return Business.menu()

    @staticmethod
    def update_building(args: dict):
        """ Change building details """
        building = get_building_from_args(args)

        street = request.form.get('street', default='', type=str)
        number = request.form.get('number', default=0, type=int)

        building.street = street
        building.number = non_negative(number)

        return redirect_with_query_params(url_for('menu'), filter=webapp.filter, triedenie=webapp.sort_type)

    @staticmethod
    def building_screen(args: dict):
        """ Page showing fist building """
        webapp.filter = request.args.get('filter', default='', type=str)
        webapp.sort_type = request.args.get('triedenie', default='', type=str)

        building = get_building_from_args(args)
        dwellings = get_dwellings_from_args(args).copy()

        if webapp.filter:
            dwellings = building.filter_dwellings(webapp.filter)

        if webapp.sort_type:
            sorter = Sorter()
            sorter.sort(dwellings, webapp.sort_type)

        return render_template('building.html', building=building, dwellings=dwellings)

    @staticmethod
    def sort_dwellings(args: dict):
        """ Set sort type for webapp """
        previous_sort_type = webapp.sort_type
        sort_type: str = request.form.get('triedenie', default='', type=str)

        if f'{sort_type}-asc' == previous_sort_type:
            sort_type = f'{sort_type}-desc'
        else:
            sort_type = f'{sort_type}-asc'

        return redirect_with_query_params(
            url_for('building_screen', building_id=args['building_id']),
            filter=webapp.filter,
            triedenie=sort_type
        )

    @staticmethod
    def filter_dwellings(args: dict):
        """ Set search filter for webapp """
        filter = request.form.get('filter', default='', type=str)

        return redirect_with_query_params(
            url_for('building_screen', building_id=args['building_id']),
            filter=filter,
            triedenie=webapp.sort_type
        )

    @staticmethod
    def add_dwelling(args: dict):
        """ Adds dwelling to the building """
        building = get_building_from_args(args)
        building.dwellings.append(Dwelling())

        return redirect_with_query_params(
            url_for('building_screen', building_id=args['building_id']),
            filter=webapp.filter,
            triedenie=webapp.sort_type
        )

    @staticmethod
    def update_dwelling(args: dict):
        """ Change dwelling details """
        dwelling = get_dwelling_from_args(args)

        block = request.form.get('block', default='', type=str)
        floor = request.form.get('floor', default=0, type=int)
        cell = request.form.get('cell', default='', type=str)
        room = request.form.get('room', default='', type=str)
        space = request.form.get('space', default=1, type=int)

        dwelling.block = non_numeric(block).upper()
        dwelling.floor = floor
        dwelling.cell = cell
        dwelling.room = room
        dwelling.space = positive(space)

        return redirect_with_query_params(
            url_for('building_screen', building_id=args['building_id']),
            filter=webapp.filter,
            triedenie=webapp.sort_type
        )

    @staticmethod
    def delete_dwelling(args: dict):
        """ Delete a dwelling """
        dwellings = get_dwellings_from_args(args)
        removed_dwelling = get_dwelling_from_args(args)

        dwellings.remove(removed_dwelling)

        return redirect_with_query_params(
            url_for('building_screen', building_id=args['building_id']),
            filter=webapp.filter,
            triedenie=webapp.sort_type
        )

    @staticmethod
    def dwelling_screen(args: dict):
        """ Show details about dwelling """
        building = get_building_from_args(args)
        dwelling = get_dwelling_from_args(args)

        return render_template('dwelling.html', building=building, dwelling=dwelling)

    @staticmethod
    def add_person(args: dict):
        """ Add person to a dwelling """
        dwelling = get_dwelling_from_args(args)

        if dwelling.free_spaces() == 0:
            return redirect_with_query_params(url_for('dwelling_screen', building_id=args['building_id'], dwelling_id=args['dwelling_id']))

        dwelling.add_person(Person())
        return redirect_with_query_params(url_for('dwelling_screen', building_id=args['building_id'], dwelling_id=args['dwelling_id']))

    @staticmethod
    def update_person(args: dict):
        """ Change person data """
        person = get_person_from_args(args)

        name = request.form.get('name', default='', type=str)
        code = request.form.get('code', default='', type=str)
        gender = request.form.get('gender', default='m', type=str)
        birthplace = request.form.get('birthplace', default='', type=str)
        date_of_birth = request.form.get('date_of_birth', default='', type=str)
        workspace = request.form.get('workspace', default='', type=str)

        person.name = non_numeric(name)
        person.code = code
        person.gender = gender
        person.birthplace = birthplace
        person.date_of_birth = date_of_birth
        person.workspace = workspace

        return redirect_with_query_params(url_for('dwelling_screen', building_id=args['building_id'], dwelling_id=args['dwelling_id']))

    @staticmethod
    def remove_person(args: dict):
        """ Remove a person from dwelling """
        dwelling = get_dwelling_from_args(args)
        person = get_person_from_args(args)

        dwelling.remove_person(person)

        return redirect_with_query_params(url_for('dwelling_screen', building_id=args['building_id'], dwelling_id=args['dwelling_id']))
