# coding=utf-8

class Sorter:
    """ Class managing different sorting types for data objects """

    def __init__(self):

        if webapp.sort_type == 'meno-asc':
            buildings.sort()
        elif webapp.sort_type == 'meno-desc':
            buildings.sort()
        elif webapp.sort_type == 'cislo-asc':
            buildings.sort()
        elif webapp.sort_type == 'cislo-desc':

    def sort_buildings(self):
        ut.sort(key=lambda x: x.count, reverse=True)

    def sort_dwellings(self):
