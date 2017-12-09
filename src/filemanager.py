# coding=utf-8
import sys
from flask import json

from src.building import Building


class FileManager:
    """ Class for working with file system """

    @staticmethod
    def load_buildings(filename: str) -> [Building]:
        """ Loads file into a buildings array"""
        content = ''
        try:
            with open(filename, 'r') as file:
                content += file.readline()
        except EnvironmentError as error:
            print('File ' + filename + ' failed reading', error, file=sys.stderr)
            return []

        return [Building.from_json(building) for building in json.loads(content)]

    @staticmethod
    def write_file(filename: str, buildings: [Building]) -> None:
        """ Writes buildings list as a json into a file """
        try:
            serialized = [building.to_json() for building in buildings]
            with open(filename, 'w') as file:
                file.write(json.dumps(serialized))
        except EnvironmentError as error:
            print('File ' + filename + ' failed writing, your progress might be lost.', error, file=sys.stderr)
