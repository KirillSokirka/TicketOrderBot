from Ticket import Ticket
from helpers.jsonWorker import JSONWorker

import json


class RegularTicket(Ticket):

    __filename = 'json_files/tickets/regular_ticket.json'

    def __init__(self, price, id_event, name_of_buyer, date_of_buy):
        super(RegularTicket, self).__init__(price, name_of_buyer, id_event, date_of_buy)
        codes = JSONWorker.get_list_of_parameter_values(RegularTicket.__filename, 'code')
        if not codes:
            self.__code = 1
        else:
            self.__code = codes[-1] + 1
        pass

    @property
    def code(self):
        return self.__code

    def save_to_file(self):
        with open(RegularTicket.__filename, "r+") as f:
            data = json.load(f)
            data.append(self.__dict__())
            f.seek(0)
            json.dump(data, f, indent=2)

    def __dict__(self):
        _dict = super(RegularTicket, self).__dict__()
        _dict['code'] = self.__code
        return _dict