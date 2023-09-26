#!/usr/bin/python3
"""
Module documentation
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class Docs"""
    place_id = ""
    user_id = ""
    text = ""
