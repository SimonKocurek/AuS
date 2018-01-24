# coding=utf-8
from src.building import Building
from src.dwelling import Dwelling


class Sorter:
    """ Class managing different sorting types for data objects """

    def __init__(self):
        self._sort_functions = {
            'meno': lambda building: building.street,
            'cislo': lambda building: building.number
        }

        self._sort_orders = {
            'asc': False,
            'desc': True
        }

    def sort_buildings(self, buildings: [Building], sort_type: str):
        """
        :param buildings:
        :param sort_type:
        :return:
        """
        sort_type_name = sort_type.split('-')[0]
        sort_type_order = sort_type.split('-')[1]

        buildings.sort(
            key=self._sort_functions[sort_type_name],
            reverse=self._sort_orders[sort_type_order]
        )

    def sort_dwellings(self, dwellings: [Dwelling], sort_type: str):
        """
        :return:
        """
