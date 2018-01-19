# coding=utf-8
import sys
import threading

import easygui
import os
import xmltodict
from dict2xml import dict2xml
from flask import json

from src.building import Building


class FileManager:
    """ Class for working with file system """

    @staticmethod
    def load_buildings(filename: str) -> [Building]:
        """ Loads file into a buildings array"""
        if not os.path.isfile(filename):
            return []

        try:
            content = ''
            with open(filename) as file:
                content += file.readline()

            return [Building.from_json(building) for building in json.loads(content)]
        except Exception as error:
            print(f'File {filename} failed reading', error, file=sys.stderr)
            threading.Timer(2, lambda: easygui.msgbox(f'File {filename} failed reading', 'Error')).start()

        return []

    @staticmethod
    def write_file(filename: str, buildings: [Building]) -> None:
        """ Writes buildings list as a json into a file """
        if not filename.endswith('.json'):
            filename += '.json'

        try:
            serialized = [building.to_json() for building in buildings]
            with open(filename, 'w') as file:
                file.write(json.dumps(serialized))

        except Exception as error:
            print(f'File {filename} failed writing, your progress might be lost.', error, file=sys.stderr)
            threading.Timer(
                2,
                lambda: easygui.msgbox(f'File {filename} failed writing, your progress might be lost.', 'Error')
            ).start()

    @staticmethod
    def load_buildings_from_xml(filename: str) -> [Building]:
        """ :return buildings with xml file content """
        if not filename:
            return []

        try:
            with open(filename) as file:
                xml = xmltodict.parse(file.read())
                root_element = dict(xml['buildings'])

                if not isinstance(root_element['building'], list):
                    root_element['building'] = [dict(root_element['building'])]

                return [Building.from_json(building) for building in root_element['building']]

        except Exception as error:
            print(f'XML file {filename} failed reading', error, file=sys.stderr)
            easygui.msgbox(f'Failed reading xml file.', 'Error')

    @staticmethod
    def save_file_as_xml(filename: str, buildings: [Building]) -> None:
        """ Saves buildings as xml file """
        if not filename:
            return

        if not filename.endswith('.xml'):
            filename += '.xml'

        try:
            with open(filename, 'w') as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<buildings>\n')

                buildings_dictionary = [building.to_json() for building in buildings]
                xml = dict2xml(buildings_dictionary, 'building')
                file.write(xml)

                file.write('\n</buildings>\n')
        except Exception as error:
            print(f'XML file {filename} failed writing', error, file=sys.stderr)
            easygui.msgbox(f'Failed writing xml file.', 'Error')
