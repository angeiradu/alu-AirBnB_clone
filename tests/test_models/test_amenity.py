#!/usr/bin/python3
"""
Module documentation
"""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """ Test the Amenity class """

    def test_instance(self):
        """ Test instance """
        obj = Amenity()
        self.assertIsInstance(obj, Amenity)

    def test_is_subclass(self):
        """test the instance of sub classes"""
        amenity = Amenity()
        self.assertTrue(issubclass(type(amenity), BaseModel))

    def test_name(self):
        """test name"""
        amenity = Amenity()
        self.assertEqual(amenity.name, "")
        amenity.name = "Wifi"
        self.assertEqual(amenity.name, "Wifi")
        self.assertIsNotNone(amenity.id)


if __name__ == "__main__":
    unittest.main()
