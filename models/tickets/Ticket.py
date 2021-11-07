from abc import abstractmethod


class Ticket:

    def __init__(self, price):
        self.price = price

    @property
    @abstractmethod
    def code(self):
        pass

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
