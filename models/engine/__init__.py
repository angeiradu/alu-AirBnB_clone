#!/usr/bin/python3
"""The __init__ method for models directory"""
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place

storage = FileStorage()
storage.reload()

classes = {"BaseModel": BaseModel, "User": User,  "State": State,
           "City": City, "Amenity": Amenity, "Place": Place,
           "Review": Review}
