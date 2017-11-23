# coding=utf-8
import xmltodict as xmltodict
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QPushButton, QAction, QListView
from PyQt5.uic import loadUi
from dict2xml import dict2xml  # dict -> xml


class Window(QMainWindow):
    """ User interface for the system """

    def __init__(self, buildings=None):
        """ Constructor creating initializing GUI """
        super(Window, self).__init__()

        if buildings is None:
            buildings = []

        self._buildings = buildings

        loadUi('gui.ui', self)

        saveFileButton = self.saveFile  # type: QAction
        openFileButton = self.openFile  # type: QAction

        removeBuildingButton = self.RemoveBuilding  # type: QPushButton
        addBuildingButton = self.addBuilding  # type: QPushButton
        buildingListView = self.buildingsListView  # type: QListView

        removeDwellingButton = self.removeDwelling  # type: QPushButton
        addDwellingButton = self.addDwelling  # type: QPushButton
        dwellingsListView = self.dwellingsListView  # type: QListView

        saveFileButton.trigger()
        openFileButton.trigger()
        model = QStandardItemModel()
        for building in buildings:
            item = QStandardItem(str(building))
            model.appendRow(item)

        buildingListView.setModel(model)

        self.show()

    def file_open(self) -> None:
        """ Replaces buildings with xml file content """
        # filename = filedialog.askopenfilename(
        #     initialdir='./',
        #     title='Výber súbor na otvorenie',
        #     filetypes=(('xml súbory', '*.xml'), ("všetky súbory", "*.*"))
        # )

        if not filename:
            return

        with open(filename, 'r') as file:
            xml = xmltodict.parse(file.read())
            root_element = dict(xml['buildings'])
            building_list = [dict(building) for building in root_element['building']]

        # clear all previously loaded buildings
        self._buildings[:] = []
        self._buildings.extend([Building.from_json(a) for a in building_list])

    def file_save(self) -> None:
        """ Saves buildings as xml file """
        # filename = filedialog.asksaveasfilename(
        #     initialdir='./',
        #     title='Vyber Súbor',
        #     filetypes=(('xml súbory', '*.xml'), ("všetky súbory", "*.*"))
        # )

        if not filename:
            return

        with open(filename, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<buildings>\n')

            dict = [building.to_json() for building in self._buildings]
            xml = dict2xml(dict, 'building')
            file.write(xml)

            file.write('\n</buildings>\n')
