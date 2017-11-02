import unittest


class Building(unittest.TestCase):

    def test_person_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI')
        serialized = person.to_json()

        self.assertEqual(serialized, Person.from_json(serialized).to_json())

    def test_dwelling_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI')
        person2 = Person('Jožka', '14aq34esadfasdfa', 'f', datetime.now(), 'Košice', 'UInf')
        dwelling = Dwelling('B', 3, 200, 'A', 400, [person, person2])

        serialized = dwelling.to_json()

        self.assertEqual(serialized, Dwelling.from_json(serialized).to_json())

    def test_building_serialization(self):
        person = Person('Jožko', '14aq34e21g90vha', 'm', datetime.now(), 'Košice', 'CAI')
        person2 = Person('Jožka', '14aq34esadfasdfa', 'f', datetime.now(), 'Košice', 'UInf')
        dwelling = Dwelling('B', 3, 200, 'A', 4, [person, person2])

        person3 = Person('Ďurko', 'asdf', 'm', datetime.now(), 'Peking', 'UFV')
        dwelling2 = Dwelling('B', 3, 201, 'A', 2, [person3])

        building = Building('Medická', 4, [dwelling, dwelling2])
        serialized = building.to_json()

        self.assertEqual(serialized, Building.from_json(serialized).to_json())


if __name__ == '__main__':
    unittest.main()
