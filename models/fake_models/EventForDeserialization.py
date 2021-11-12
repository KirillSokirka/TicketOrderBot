
class EventForDeserialization:

    def __init__(self, id, name, date, number_of_tickets, ticket_cost):
        self.id = id
        self.name = name
        self.date = date
        self.number_of_tickets = number_of_tickets
        self.ticket_cost = ticket_cost

    def __str__(self):
        return f'<b>id</b> - {self.id}\n' + \
               f'<b>назва</b> - {self.name}\n' + \
               f'<b>кількість квитків</b> - {self.number_of_tickets}\n' + \
               f'<b>ціна</b> - {self.ticket_cost}\n'+\
                f'<b>дата проведеня</b> - {self.date}\n'