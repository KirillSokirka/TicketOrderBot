from Ticket import Ticket


class RegularTicket(Ticket):

    def __init__(self, price, id_event, name):
        super(RegularTicket, self).__init__(price, name, id_event)
        pass

    @property
    def code(self):
        pass

    @staticmethod
    def write_to_json(json_file_Name):
        pass