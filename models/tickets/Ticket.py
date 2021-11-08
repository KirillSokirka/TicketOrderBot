from abc import abstractmethod
import json

class Ticket:



    def __init__(self, price, name_of_buyer, id_of_event):
        self.price = price
        self.name_of_buyer = name_of_buyer
        self.id_of_event = id_of_event

    @property
    @abstractmethod
    def code(self):
        pass

    @property
    def id_of_event(self):
        return self.__id_of_event

    @id_of_event.setter
    def id_of_event(self, value):
        if not isinstance(value, int):
            raise TypeError
        #some work with database should be here
        self.__id_of_event = value

    @property
    def name_of_buyer(self):
        return self.__name_of_buyer

    @name_of_buyer.setter
    def name_of_buyer(self, value):
        if not isinstance(value, str):
            raise TypeError
        if not value or value == ' ':
            raise ValueError
        self.__name_of_buyer = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise TypeError
        if value <= 0:
            raise ValueError
        self.__price = value

    @abstractmethod
    @staticmethod
    def write_to_json(json_file_Name):
        pass
