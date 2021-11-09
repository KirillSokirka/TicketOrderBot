from abc import abstractmethod
from datetime import datetime

from helpers.jsonWorker import JSONWorker


class Ticket:

    def __init__(self, price, name_of_buyer, id_of_event, date_of_buy):
        self.price = price
        self.name_of_buyer = name_of_buyer
        self.id_of_event = id_of_event
        self.date_of_buy = date_of_buy

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
        if value not in JSONWorker.get_list_of_parameter_values('json_files/events.json', 'id'):
            raise ValueError
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

    @property
    def date_of_buy(self):
        return self.__date_of_buy

    @date_of_buy.setter
    def date_of_buy(self, value):
        if not isinstance(value, datetime):
            raise TypeError
        self.__date_of_buy = value

    @abstractmethod
    def save_to_file(self):
        pass

    def __dict__(self):
        return {
            'event_id' : self.__id_of_event,
            'price' : self.__price,
            'name_of_buyer' : self.__name_of_buyer,
            'date_of_buy' : self.__date_of_buy
        }