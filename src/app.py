# coding=utf-8
import atexit
import threading
import webbrowser

from src import webapp
from src.filemanager import FileManager


def main():
    """ Starting method """
    data_file = '../data.json'

    webapp.buildings = FileManager.load_buildings(data_file)
    atexit.register(lambda: FileManager.write_file(data_file, webapp.buildings))

    port = 5431
    threading.Timer(1.25, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    webapp.app.run(port=port, debug=False)


if __name__ == "__main__":
    main()
