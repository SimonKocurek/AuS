# coding=utf-8
import atexit

from flask import render_template, request, redirect, url_for

from src import webapp
from src.filemanager import FileManager
from src.utilities import is_logged_out, logout_user


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
        webapp.data_file = f'../{user_code}.json'
        webapp.buildings = FileManager.load_buildings(webapp.data_file)

        atexit.register(lambda: FileManager.write_file(webapp.data_file, webapp.buildings))

        return redirect(url_for('menu'))

    @staticmethod
    def menu():
        """ Starting page for selecting building """
        if is_logged_out():
            return redirect('/')

        return render_template('menu.html', buildings=webapp.buildings)
