#!/usr/bin/python3
"""This is a base model class for the Airbnb project"""
import uuid
from sqlalchemy import String, DateTime, Column
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import models


Base = declarative_base()


class BaseModel:
    """This class will defines all of the common attributes
    for other classes - other classes will inherit here
    """

    id = Column(String(60), unique=True, nullable=False,
                primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiating the base model class
        Args:
            args: not applicable
            kwargs:   BaseModel arguments for the constructor
        Attributes:
            id: unique id will be generated
            created_at:  date created
            updated_at: date updated
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs.keys():
                setattr(self, "id", str(uuid.uuid4()))
            time = datetime.now()
            if "created_at" not in kwargs.keys():
                setattr(self, "created_at", time)
            if "updated_at" not in kwargs.keys():
                setattr(self, "updated_at", time)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """returns a string
        Return:
            returns a string of class name, id, and dictionary
        """
        dic = self.to_dict()
        # del dic['__class__']
        # dic['created_at'] = datetime.strptime(dic['created_at'],
        #                                       "%Y-%m-%dT%H:%M:%S")
        # dic['updated_at'] = datetime.strptime(dic['updated_at'],
        #                                       "%Y-%m-%dT%H:%M:%S")
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, dic)

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """updates the public instance attribute updated_at to current
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        if '_sa_instance_state' in my_dict.keys():
            my_dict.pop('_sa_instance_state', None)
        return my_dict

    def delete(self):
        """Deletes the current instance from the storage
        (models.storage) by calling the method delete"""
        models.storage.delete(self)
