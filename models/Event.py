import json
import datetime

class Event:

    __json_file = "json_files/events.json"

    @property
    def event_id(self):
        return self.__event_id

    @event_id.setter
    def event_id(self, value):
        if not isinstance(value, int):
            raise TypeError
        self.__event_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError
        if not value or value == ' ':
            raise ValueError
        self.__name = value

    @property
    def number_of_ticket(self):
        return self.__number_of_ticket

    @number_of_ticket.setter
    def number_of_ticket(self, value):
        if not isinstance(value, int):
            raise TypeError
        self.__number_of_ticket = value

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
            "id" : self.__event_id,
            "name" : self.__name,
            "number_of_tickets" : self.__number_of_ticket,
            "date" : self.__date.strftime("%d/%m/%y")
        }
