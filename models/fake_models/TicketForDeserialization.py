
class TicketForDeserialization:

    def __init__(self, id, name_of_buyer, event_id, date_of_buy, price, type):
        self.name_of_buyer = name_of_buyer
        self.id_of_event = event_id
        self.date_of_buy = date_of_buy
        self.id = id
        self.price = price
        self.type = type

    def __str__(self):
        return  f'<b>id</b> - {self.id}\n' + \
                f'<b>покупець</b> - {self.name_of_buyer}\n' + \
                f'<b>id івенту</b> - {self.id_of_event}\n' + \
                f'<b>тип квитка</b> - {self.type}\n' + \
                f'<b>дата покупки</b> - {self.date_of_buy}\n' + \
                f'<b>ціна</b> - {self.price}\n'