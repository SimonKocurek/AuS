import atexit  # Exit program callback
import json  # Serialize object <-> json
import sys

from PyQt5.QtWidgets import QApplication

from src.building import Building
from src.window import Window

DATA_FILE = 'data.json'
buildings = []


def load_file(filename: str, buildings: list) -> None:
    """ Loads file into a buildings variable """
    content = ''
    with open(filename, 'r') as file:
        content += file.readline()

    buildings[:] = []
    buildings.extend([Building.from_json(building) for building in json.loads(content)])


def exit_handler():
    """ Executes at program shutdown"""
    write_file(DATA_FILE)


def write_file(filename: str) -> None:
    """ Writes buildings list as a json into a file """
    serialized = [building.to_json() for building in buildings]
    with open(filename, 'w') as file:
        file.write(json.dumps(serialized))

def main() -> None:
    load_file(DATA_FILE, buildings)
    atexit.register(exit_handler)

    app = QApplication(sys.argv)
    window = Window(buildings)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
