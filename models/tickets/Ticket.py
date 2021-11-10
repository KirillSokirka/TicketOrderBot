import re
from datetime import datetime

from helpers.jsonWorker import JSONWorker


class Ticket:

    __filename = 'json_files/tickets.json'
    __list_of_codes = []

    def __init__(self, code, name_of_buyer, id_of_event, date_of_buy):
        self.name_of_buyer = name_of_buyer
        self.id_of_event = id_of_event
        self.date_of_buy = date_of_buy
        self.code = code


    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if value not in Ticket.__list_of_codes:
            codes = JSONWorker.get_list_of_parameter_values(Ticket.__filename, 'code')
            if not codes:
                self.__code = f"{1}_{self.id_of_event}"
            else:
                parts = codes[-1].split("_")
                self.__code = f"{int(parts[0]) + 1}_{self.id_of_event}"
            Ticket.__list_of_codes.append(self.__code)
        else:
            self.__code = value

    @property
    def id_of_event(self):
        return self.__id_of_event

    @id_of_event.setter
    def id_of_event(self, value):
        if not isinstance(value, int):
            raise TypeError
        if value not in JSONWorker.get_list_of_parameter_values('json_files/events.json', 'event_id'):
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
    def date_of_buy(self):
        return self.__date_of_buy

    @date_of_buy.setter
    def date_of_buy(self, value):
        if isinstance(value, str):
            if re.match('(1[0-2]|0?[1-9]|3[0-1])\/(0?[0-9]|1[0-2])\/([2-9][1-9])', value):
                self.__date_of_buy = datetime.strptime(value, '%d/%m/%y')
                return
        elif not isinstance(value, datetime):
            raise TypeError
        self.__date_of_buy = value

    def __dict__(self):
        return {
            'code' : self.__code,
            'event_id' : self.__id_of_event,
            'name_of_buyer' : self.__name_of_buyer,
            'date_of_buy' : self.__date_of_buy.strftime("%d/%m/%y"),
        }