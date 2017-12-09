# coding=utf-8
import unittest
from datetime import datetime

from src.building import Building
from src.dwelling import Dwelling
from src.person import Person


class BuildingTest(unittest.TestCase):
    def test_building_filtering(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI')
        person2 = Person('Jožka', '14aq34esadfasdfa', 'f', datetime.now(), 'Košice', 'UInf')
        dwelling = Dwelling('B', 3, 200, 'A', 4, [person, person2])

        person3 = Person('Ďurko', 'asdf', 'm', datetime.now(), 'Peking', 'UFV')
        dwelling2 = Dwelling('B', 3, 201, 'A', 2, [person3])

        dwelling3 = Dwelling('B', 4, 301, 'A', 3, [person3])

        building = Building('Medická', 4, [dwelling, dwelling2, dwelling3])

        self.assertSetEqual(set(building.all_people()), {person, person2, person3})
        self.assertSetEqual(set(building.filter_dwellings(block='B')), {dwelling, dwelling2, dwelling3})
        self.assertSetEqual(set(building.filter_dwellings(block='B', floor=3)), {dwelling, dwelling2})
        self.assertSetEqual(set(building.filter_dwellings(block='B', floor=4)), {dwelling3})
        self.assertSetEqual(set(building.filter_dwellings(minimum_free_spaces=2, maximum_free_spaces=-1)), set({}))
        self.assertSetEqual(set(building.filter_dwellings(maximum_free_spaces=1)), {dwelling2})


if __name__ == '__main__':
    unittest.main()
