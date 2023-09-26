#!usr/bin/python3
""" Module for testing the BaseModel class """

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """
        Unittests to test instantiation of the 'BaseModel' class.
    """

    def test_no_args_instantiates(self):
        # It checks if the class BaseModel is,
        # the same type as the instance of BaseModel.
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        # It checks if the BaseModel object is in the storage.all().values()
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        # It checks if the type of the id attribute,
        # of the BaseModel class is a string.
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        # It checks if the type of the created_at attribute is datetime.
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        # It checks if the type of the updated_at attribute is datetime.
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self):
        # 1. We’re creating a datetime object.
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        # 1. We create a new instance of the BaseModel class.
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        # 1. We create a datetime object with the current time.

        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """
        Unittests to test save method of the 'BaseModel' class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        my_model = BaseModel()
        sleep(0.05)
        initial_updated_at = my_model.updated_at
        my_model.save()
        self.assertLess(initial_updated_at, my_model.updated_at)

    def test_two_saves(self):
        my_model = BaseModel()
        sleep(0.05)
        initial_updated_at = my_model.updated_at
        my_model.save()
        new_updated_at = my_model.updated_at
        self.assertLess(initial_updated_at, new_updated_at)
        sleep(0.05)
        my_model.save()
        self.assertLess(new_updated_at, my_model.updated_at)

    def test_save_with_arg(self):
        my_model = BaseModel()
        with self.assertRaises(TypeError):
            my_model.save(None)

    def test_save_updates_file(self):
        my_model = BaseModel()
        my_model.save()
        my_model_id = "BaseModel." + my_model.id
        with open("file.json", "r") as f:
            self.assertIn(my_model_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """
        Unittests to test 'to_dict' method of the 'BaseModel' class.
    """

    def setUp(self):
        self.my_model = BaseModel()

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.my_model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.my_model.to_dict())
        self.assertIn("created_at", self.my_model.to_dict())
        self.assertIn("updated_at", self.my_model.to_dict())
        self.assertIn("__class__", self.my_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.my_model.name = "Holberton"
        self.my_model.my_number = 98
        self.assertIn("name", self.my_model.to_dict())
        self.assertIn("my_number", self.my_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        model_dict = self.my_model.to_dict()
        self.assertEqual(str, type(model_dict["created_at"]))
        self.assertEqual(str, type(model_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.my_model.to_dict(), self.my_model.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.my_model.to_dict(None)

if __name__ == "__main__":
    unittest.main()
