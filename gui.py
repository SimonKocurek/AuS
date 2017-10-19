import tkinter
from tkinter import filedialog

import xmltodict as xmltodict
from dict2xml import dict2xml  # dict -> xml

from building import Building


class Gui:
    """ User interface for the system """

    def __init__(self, buildings):
        """ Constructor creating initializing GUI """
        self._buildings = buildings

        root = tkinter.Tk()
        root.title('Ubytovací Informačný Systém')

        menubar = tkinter.Menu(root)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Otvor", command=self.file_open)
        filemenu.add_command(label="Ulož", command=self.file_save)
        menubar.add_cascade(label="Súbor", menu=filemenu)

        listbox = tkinter.Listbox(root)
        listbox.pack()

        # listbox.

        add_button = tkinter.Button(root, text="+", command=self.nothing)
        add_button.pack(side=tkinter.LEFT)
        remove_button = tkinter.Button(root, text="-", command=self.nothing)
        remove_button.pack(side=tkinter.LEFT)

        root.config(menu=menubar)
        root.mainloop()

    def nothing(self):
        """

        :return:
        """
        pass

    def file_open(self) -> None:
        """ Replaces buildings file with xml file content """
        filename = filedialog.askopenfilename(
            initialdir='./',
            title='Výber súbor na otvorenie',
            filetypes=(('xml súbory', '*.xml'), ("všetky súbory", "*.*"))
        )

        if not filename:
            return

        with open(filename, 'r') as file:
            xml = xmltodict.parse(file.read())
            root_element = dict(xml['buildings'])
            building_list = [dict(building) for building in root_element['building']]

        print(self._buildings)

        # clear all previously loaded buildings
        self._buildings[:] = []
        self._buildings.extend([Building.from_json(a) for a in building_list])
        print(self._buildings)

    def file_save(self) -> None:
        """ Saves buildings as xml file """
        filename = filedialog.asksaveasfilename(
            initialdir='./',
            title='Výber Súbor',
            filetypes=(('xml súbory', '*.xml'), ("všetky súbory", "*.*"))
        )

        if not filename:
            return

        with open(filename, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<buildings>\n')

            dict = [building.to_json() for building in self._buildings]
            xml = dict2xml(dict, 'building')
            file.write(xml)

            file.write('\n</buildings>\n')
