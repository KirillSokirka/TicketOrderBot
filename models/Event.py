from helpers.jsonWorker import JSONWorker

import re
from datetime import datetime


class Event:

    __json_file = "json_files/events.json"
    __names = []
    __ids = []

    def __init__(self, id=None, name=None, date=None, number_of_tickets=None, ticket_cost=None):
        self.id = id
        self.name = name
        self.date = date
        self.number_of_tickets = number_of_tickets
        self.ticket_cost = ticket_cost

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value not in Event.__ids:
            list_of_id = JSONWorker.get_values_by_parameter_name(Event.__json_file, 'id')
            if not len(list_of_id):
                self.__id = 1
            else:
                self.__id = list_of_id[-1] + 1
        else:
            self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value is None:
            return
        if value not in Event.__names:
            if not JSONWorker.check_if_unique(Event.__json_file, 'name', value):
                raise ValueError('Івент з таким ім\'ям вже існує....')
            if not value or value == ' ':
                raise ValueError
            Event.__names.append(value)
        self.__name = value

    @property
    def number_of_tickets(self):
        return self.__number_of_ticket

    @number_of_tickets.setter
    def number_of_tickets(self, value):
        if value is None:
            return
        if not isinstance(value, int):
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
        if value is None:
            return
        if not isinstance(value, int):
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
        if value is None:
            self.__date = None
            return
        if isinstance(value, str):
            if re.match('(0?[1-9]|[12][0-9]|3[0-1])\/(0?[1-9]|1[0-2])\/(20[2-9][1-9])', value):
                if datetime.today() > datetime.strptime(value, '%d/%m/%Y'):
                    raise ValueError
                self.__date = datetime.strptime(value, '%d/%m/%Y')
            else:
                raise ValueError
        else:
            raise TypeError

    def __str__(self):
        return f'<b>id</b> - {self.id}\n' + \
               f'<b>назва</b> - {self.name}\n' + \
               f'<b>кількість квитків</b> - {self.__number_of_ticket}\n' + \
               f'<b>ціна</b> - {self.__ticket_cost}\n'+\
                f'<b>дата проведеня</b> - {self.__date.strftime("%d/%m/%y")}\n'

    def __dict__(self):
        return {
            "id" : self.__id,
            "name" : self.__name,
            "number_of_tickets" : self.__number_of_ticket,
            "ticket_cost" : self.__ticket_cost,
            "date" : self.__date.strftime("%d/%m/%Y")
        }
