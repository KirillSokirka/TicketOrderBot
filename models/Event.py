from helpers.jsonWorker import JSONWorker

import json
import datetime


class Event:

    __json_file = "json_files/events.json"

    def __init__(self):
        list_of_id = JSONWorker.get_list_of_parameter_values(Event.__json_file, 'id')
        if not len(list_of_id):
            self.__id = 1
        else:
            self.__id = list_of_id[-1] + 1
        self.__name = None
        self.__date = None
        self.__number_of_ticket = None
        self.__ticket_cost = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if JSONWorker.check_if_unique(Event.__json_file, 'name', value):
            raise ValueError('Івент з таким ім\'ям вже існує....')
        if not value or value == ' ':
            raise ValueError
        self.__name = value

    @property
    def number_of_ticket(self):
        return self.__number_of_ticket

    @number_of_ticket.setter
    def number_of_ticket(self, value):
        if not isinstance(value, str):
            raise TypeError
        if not value.isdigit():
            raise ValueError
        value = int(value)
        if value <= 0:
            raise ValueError
        self.__number_of_ticket = value

    @property
    def ticket_cost(self):
        return self.__ticket_cost

    @ticket_cost.setter
    def ticket_cost(self, value):
        if not isinstance(value, str):
            raise TypeError
        if not value.isdigit():
            raise ValueError
        value = int(value)
        if value <= 0:
            raise ValueError
        self.__ticket_cost = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime.date):
            raise TypeError
        self.__date = value

    def save_to_file(self):
        with open(Event.__json_file, "r+") as f:
            data = json.load(f)
            data.append(self.__dict__())
            f.seek(0)
            json.dump(data, f, indent=2)

    def __dict__(self):
        return {
            "id" : self.__id,
            "name" : self.__name,
            "number_of_tickets" : self.__number_of_ticket,
            "ticket_cost" : self.__ticket_cost,
            "date" : self.__date.strftime("%d/%m/%y")
        }
