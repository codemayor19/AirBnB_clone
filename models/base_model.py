#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime

class BaseModel:
    """BaseModel for creating and managing instances"""

    def __init__(self, *args, **kwargs):
        """initialize an instance of the basemodel"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        return obj_dict

    def save(self):
        self.updated_at = datetime.now()

    def __str__(self):
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
