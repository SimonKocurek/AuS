# coding=utf-8
import unittest
from datetime import datetime

from src.entity.building import Building
from src.entity.dwelling import Dwelling
from src.entity.person import Person


class SerializationTest(unittest.TestCase):

    def test_person_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI', identifier='123asdf')
        serialized = person.to_json()

        self.assertEqual(serialized, Person.from_json(serialized).to_json())

    def test_dwelling_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI', identifier='123asdf')
        person2 = Person('Jožka', '14aq34esadfasdfa', 'f', datetime.now(), 'Košice', 'UInf', identifier='456ghj')
        dwelling = Dwelling('B', 3, 200, 'A', 400, [person, person2])

        serialized = dwelling.to_json()

        self.assertEqual(serialized, Dwelling.from_json(serialized).to_json())

    def test_building_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI', identifier='123asdf')
        person2 = Person('Jožka', '14aq34esadfasdfa', 'f', datetime.now(), 'Košice', 'UInf', identifier='456ghj')
        dwelling = Dwelling('B', 3, 200, 'A', 4, [person, person2])

        person3 = Person('Ďurko', 'asdf', 'm', datetime.now(), 'Peking', 'UFV', identifier='890avbn')
        dwelling2 = Dwelling('B', 3, 201, 'A', 2, [person3])

        dwelling3 = Dwelling('B', 4, 301, 'A', 3, [person3])

        building = Building('Medická', 4, [dwelling, dwelling2, dwelling3])
        serialized = building.to_json()

        self.assertEqual(serialized, Building.from_json(serialized).to_json())


if __name__ == '__main__':
    unittest.main()
