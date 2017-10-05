import atexit
import json

from building import Building
from gui import Gui


def main() -> None:
    buildings = []

    medicka4 = Building('medicka', 4)
    buildings.append(medicka4)
    gui = Gui()
    atexit.register(exit_handler)


def exit_handler():
    list = [1, 2, (3, 4)]  # Note that the 3rd element is a tuple (3, 4)
    print(json.dumps(list))


if __name__ == '__main__':
    main()
