# coding=utf-8
import atexit

import easygui
from flask import render_template, request, redirect, url_for

from src import webapp
from src.building import Building
from src.dwelling import Dwelling
from src.filemanager import FileManager
from src.sorter import Sorter
from src.utilities import is_logged_out, logout_user, get_building_by_id, non_negative, redirect_with_query_params


class Business:
    """ Implementations for webapp functions """

    @staticmethod
    def index():
        """ Intro page """
        return render_template('index.html')

    @staticmethod
    def login():
        """ Logging using Intro page """
        if not is_logged_out():
            logout_user()

        webapp.user_code = request.form.get('inputCode', default='', type=str)
        webapp.data_file = f'../{webapp.user_code}.json'
        webapp.buildings = FileManager.load_buildings(webapp.data_file)

        atexit.register(lambda: FileManager.write_file(webapp.data_file, webapp.buildings))

        return redirect(url_for('menu'))

    @staticmethod
    def menu():
        """ Starting page for selecting building """
        if is_logged_out():
            return redirect('/')

        webapp.filter = request.args.get('filter', default='', type=str)
        webapp.sort_type = request.args.get('triedenie', default='', type=str)

        buildings = webapp.buildings.copy()

        if webapp.filter:
            buildings = [building for building in buildings if webapp.filter in str(building)]

        if webapp.sort_type:
            sorter = Sorter()
            sorter.sort_buildings(buildings, webapp.sort_type)

        return render_template('menu.html', buildings=buildings)

    @staticmethod
    def logout():
        """ Returns only filtered out buildings """
        if is_logged_out():
            return redirect('/')

        logout_user()
        return redirect('/')

    @staticmethod
    def load_buildings():
        """ Load buildings from external xml file """
        if is_logged_out():
            return redirect('/')

        filename = easygui.fileopenbox('File to load xml content from', 'Save file', filetypes=['xml'])

        loaded_buildings = FileManager.load_buildings_from_xml(filename)

        if loaded_buildings:
            webapp.buildings = loaded_buildings

        return redirect(url_for('menu'))

    @staticmethod
    def save_buildings():
        """ Save buildings to external xml file """
        if is_logged_out():
            return redirect('/')

        filename = easygui.filesavebox('File to save xml content', 'Save file')

        FileManager.save_file_as_xml(filename, webapp.buildings)

        return redirect_with_query_params('menu', filter=webapp.filter, triedenie=webapp.sort_type)

    @staticmethod
    def filter_buildings():
        """ Set search filter for webapp """
        filter = request.form.get('filter', default='', type=str)

        return redirect_with_query_params('menu', filter=filter, triedenie=webapp.sort_type)

    @staticmethod
    def sort_buildings():
        """ Set sort type for webapp """
        previous_sort_type = webapp.sort_type
        sort_type: str = request.form.get('triedenie', default='', type=str)

        if f'{sort_type}-asc' == previous_sort_type:
            sort_type = f'{sort_type}-desc'
        else:
            sort_type = f'{sort_type}-asc'

        return redirect_with_query_params('menu', filter=webapp.filter, triedenie=sort_type)

    @staticmethod
    def add_building():
        """ Add new building """
        if is_logged_out():
            return redirect('/')

        webapp.buildings.append(Building('', 0))
        return redirect_with_query_params('menu', filter=webapp.filter, triedenie=webapp.sort_type)

    @staticmethod
    def delete_building(args: dict):
        """ Delete a building """
        if is_logged_out():
            return redirect('/')

        building_id = args['building_id']

        building = get_building_by_id(building_id, webapp.buildings)
        webapp.buildings.remove(building)

        return redirect_with_query_params('menu', filter=webapp.filter, triedenie=webapp.sort_type)

    @staticmethod
    def update_buildings(args: dict):
        """ Change building details """
        if is_logged_out():
            return redirect('/')

        building_id = args['building_id']

        building = get_building_by_id(building_id, webapp.buildings)

        street = request.form.get('street', default='', type=str)
        number = request.form.get('number', default=0, type=int)

        building.street = street
        building.number = non_negative(number)

        return redirect_with_query_params('menu', filter=webapp.filter, triedenie=webapp.sort_type)

    @staticmethod
    def building_screen(args: dict):
        """ Page showing fist building """
        building_id = args['building_id']
        building = get_building_by_id(building_id, webapp.buildings)

        return render_template('building.html', building=building, dwellings=building.dwellings)

    @staticmethod
    def add_dwelling(args: dict):
        """ Adds dwelling to the building """
        building_id = args['building_id']
        building = get_building_by_id(building_id, webapp.buildings)

        building.dwellings.append(Dwelling('', 0, 0, '', 1))

        return render_template('building.html', building=building, dwellings=building.dwellings)
