from helpers.jsonWorker import JSONWorker

import re
from datetime import datetime


class Ticket:

    __filename = 'json_files/tickets.json'

    def __init__(self, id, name_of_buyer, id_of_event, date_of_buy):
        self.name_of_buyer = name_of_buyer
        self.id_of_event = id_of_event
        self.date_of_buy = date_of_buy
        self.id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        codes = JSONWorker.get_values_by_parameter_name(Ticket.__filename, 'id')
        if not codes:
            self.__id = f"{1}_{self.id_of_event}"
        else:
            parts = codes[-1].split("_")
            self.__id = f"{int(parts[0]) + 1}_{self.id_of_event}"

    @property
    def id_of_event(self):
        return self.__id_of_event

    @id_of_event.setter
    def id_of_event(self, value):
        if not isinstance(value, int):
            raise TypeError
        if value not in JSONWorker.get_values_by_parameter_name('json_files/events.json', 'id'):
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
            if re.match('(0?[1-9]|[12][0-9]|3[0-1])\/(0?[0-9]|1[0-2])\/(20[2-9][1-9])', value):
                self.__date_of_buy = datetime.strptime(value, '%d/%m/%Y')
                return
        elif not isinstance(value, datetime):
            raise TypeError
        self.__date_of_buy = value

    def __dict__(self):
        return {
            'id' : self.__id,
            'event_id' : self.__id_of_event,
            'name_of_buyer' : self.__name_of_buyer,
            'date_of_buy' : self.__date_of_buy.strftime("%d/%m/%Y"),
        }