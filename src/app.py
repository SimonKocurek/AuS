# coding=utf-8
import atexit  # Exit program callback

from flask import Flask, render_template

from src.filemanager import FileManager

DATA_FILE = '../data.json'

buildings = FileManager.load_buildings(DATA_FILE)
atexit.register(lambda : FileManager.write_file(DATA_FILE, buildings))

app = Flask(__name__, template_folder='../html')

@app.route("/")
def main():
    return render_template('index.html', buildings=buildings)

@app.route("/building/<building_name>")
def building(building_name: str):
    building = next((b for b in buildings if str(b) == building_name), None)

    if not building:
        raise ValueError('Incorrect url')

    return render_template('building.html',
                           building=building,
                           dwellings=building.dwellings)

if __name__ == "__main__":
    app.run(debug=True)
