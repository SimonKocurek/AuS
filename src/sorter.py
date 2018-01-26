# coding=utf-8


class Sorter:
    """ Class managing different sorting types for data objects """

    def __init__(self):
        """ Constructor preparing all sorting possible sorting attributes """

        self._sort_functions = {
            'meno': lambda building: building.street,
            'cislo': lambda building: building.number,

            'blok': lambda dwelling: dwelling.block,
            'poschodie': lambda dwelling: dwelling.floor,
            'bunka': lambda dwelling: dwelling.cell,
            'volne_miesto': lambda dwelling: dwelling.free_spaces,
            'pocet_ludi': lambda dwelling: len(dwelling.people)
        }

        self._sort_orders = {
            'asc': False,
            'desc': True
        }

    def sort(self, list_of_items: list, sort_type: str):
        """ Sorts the provided list using a sort_type """
        sort_type_name = sort_type.split('-')[0]
        sort_type_order = sort_type.split('-')[1]

        list_of_items.sort(
            key=self._sort_functions[sort_type_name],
            reverse=self._sort_orders[sort_type_order]
        )
