from helpers.jsonWorker import JSONWorker

import datetime


class EventForDeserialization:

    def __init__(self, event_id, name, number_of_tickets, tickets_cost, date):
        self.event_id = event_id
        self.name = name
        self.number_of_tickets = number_of_tickets
        self.tickets_cost = tickets_cost
        self.date = date

class Event:

    __json_file = "json_files/events.json"

    def __init__(self):
        list_of_id = JSONWorker.get_list_of_parameter_values(Event.__json_file, 'event_id')
        if not len(list_of_id):
            self.__id = 1
        else:
            self.__id = list_of_id[-1] + 1
        self.__name = None
        self.__date = None
        self.__number_of_tickets = None
        self.__ticket_cost = None

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not JSONWorker.check_if_unique(Event.__json_file, 'name', value):
            raise ValueError('Івент з таким ім\'ям вже існує....')
        if not value or value == ' ':
            raise ValueError
        self.__name = value

    @property
    def number_of_tickets(self):
        return self.__number_of_ticket

    @number_of_tickets.setter
    def number_of_tickets(self, value):
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

    def __dict__(self):
        return {
            "event_id" : self.__id,
            "name" : self.__name,
            "number_of_tickets" : self.__number_of_ticket,
            "ticket_cost" : self.__ticket_cost,
            "date" : self.__date.strftime("%d/%m/%y")
        }
