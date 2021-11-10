from helpers.jsonWorker import JSONWorker
from models.tickets.Ticket import Ticket


class AdvanceTicket(Ticket):

    __filename = 'json_files/tickets.json'

    def __init__(self, price, event_id, name_of_buyer, date_of_buy, type='advance_ticket'):
        super(AdvanceTicket, self).__init__(None, name_of_buyer, event_id, date_of_buy)
        self.price = price
        self.type = type

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        codes = JSONWorker.get_list_of_parameter_values('json_files/tickets.json', 'code')
        if not codes or self.code not in codes:
            if not isinstance(value, int):
                raise TypeError
            if value <= 0:
                raise ValueError
            self.__price = int(value - 0.4 * value)
        else:
            self.__price = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__type = value

    def __str__(self):
        return f'<b>id</b> - {self.code}\n' + \
               f'<b>покупець</b> - {self.name_of_buyer}\n' + \
               f'<b>id івенту</b> - {self.id_of_event}\n' + \
               f'<b>тип квитка</b> - {self.type}\n' + \
               f'<b>дата покупки</b> - {self.date_of_buy.strftime("%d/%m/%y")}\n' + \
               f'<b>ціна</b> - {self.__price}\n'

    def __dict__(self):
        _dict = super(AdvanceTicket, self).__dict__()
        _dict['price'] = self.__price
        _dict['type'] = self.__type
        return _dict
