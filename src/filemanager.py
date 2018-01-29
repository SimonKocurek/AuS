# coding=utf-8
import os
import sys
import traceback

import xmltodict
from dict2xml import dict2xml
from flask import json

from src.entity.building import Building


class FileManager:
    """ Class for working with file system """

    @staticmethod
    def load_buildings(filename: str) -> [Building]:
        """ Loads file into a buildings array"""
        if not os.path.isfile(filename):
            return []

        loaded = FileManager._error_checked(
            FileManager._load_from_json_file,
            f'File {filename} failed reading',
            {'filename': filename}
        )

        if loaded:
            return loaded
        else:
            return []

    @staticmethod
    def _load_from_json_file(args: dict) -> [Building]:
        """ Loads buildings from JSON file """
        content = ''
        with open(args['filename']) as file:
            content += file.readline()

        return [Building.from_json(building) for building in json.loads(content)]

    @staticmethod
    def write_file(filename: str, buildings: [Building]) -> None:
        """ Writes buildings list as a json into a file """
        if not filename.endswith('.json'):
            filename += '.json'

        FileManager._error_checked(
            FileManager._write_to_json_file,
            f'File {filename} failed writing, your progress might be lost.',
            {'filename': filename, 'buildings': buildings}
        )

    @staticmethod
    def _write_to_json_file(args: dict) -> None:
        """ Writes to json file """
        serialized = [building.to_json() for building in args['buildings']]
        with open(args['filename'], 'w') as file:
            file.write(json.dumps(serialized))

    @staticmethod
    def load_buildings_from_xml(filename: str) -> [Building]:
        """ :return buildings with xml file content """
        if not filename:
            return []

        return FileManager._error_checked(
            FileManager._load_from_xml_file,
            f'XML file {filename} failed reading',
            {'filename': filename}
        )

    @staticmethod
    def _load_from_xml_file(args: dict) -> [Building]:
        """ Reads building list from file """
        with open(args['filename']) as file:
            xml = xmltodict.parse(file.read())
            root_element = dict(xml['buildings'])

            if root_element['building'] is None:
                root_element['building'] = []

            elif not isinstance(root_element['building'], list):
                root_element['building'] = [dict(root_element['building'])]

            return [Building.from_json(building) for building in root_element['building']]

    @staticmethod
    def save_file_as_xml(filename: str, buildings: [Building]) -> None:
        """ Saves buildings as xml file """
        if not filename:
            return

        if not filename.endswith('.xml'):
            filename += '.xml'

        FileManager._error_checked(
            FileManager._write_to_xml_file,
            f'XML file {filename} failed writing',
            {'filename': filename, 'buildings': buildings}
        )

    @staticmethod
    def _write_to_xml_file(args: dict) -> None:
        """ Writes the buildings to a file """
        with open(args['filename'], 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<buildings>\n')

            buildings_dictionary = [building.to_json() for building in args['buildings']]
            xml = dict2xml(buildings_dictionary, 'building')
            file.write(xml)

            file.write('\n</buildings>\n')

    @staticmethod
    def _error_checked(attempt: callable, error_message: str, attempt_args: dict = None) -> any:
        """ Executes function with logging and error callback """
        try:
            if attempt_args:
                return attempt(attempt_args)
            else:
                return attempt()

        except Exception as error:
            print(error_message, error, file=sys.stderr)
            traceback.print_exc()
