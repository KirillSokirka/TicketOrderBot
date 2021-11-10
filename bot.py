from config import *
from models.Event import Event, EventForDeserialization
from models.User import User
from models.tickets.RegularTicket import RegularTicket
from models.tickets.StudentTicket import StudentTicket
from models.tickets.AdvanceTicket import AdvanceTicket
from models.tickets.LateTicket import LateTicket
from helpers.s3manager import S3Manager
from helpers.jsonWorker import JSONWorker


import telebot
from telebot import types
from datetime import date, datetime
from flask import request


bot = telebot.TeleBot(BOT_TOKEN)
event = Event()
student_status = ''

S3Manager.upload_object('json_files/tickets.json', TICKETS_KEY)
S3Manager.upload_object('json_files/events.json', EVENTS_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_animation(message.from_user.id, open(HelloSticker, 'rb'))
    bot.send_message(message.from_user.id, "Привіт, " + message.from_user.first_name +
                 "\nЯ - <b>Ticketeeeer</b>! З моєю допомогою ти зможеш купувати*"
                 " квитки на різноманітні круті івенти. "
                 "\nПеред використанням, ознайомтеся, будь ласка, з доступним командами.",
                 parse_mode='html')


@bot.message_handler(commands=['register'])
def register(message):
    bot.send_message(message.from_user.id,
                     'Ввведіть свій email за форматом: <b>Email: example@exmpl.ex</b>',
                     parse_mode='html')


@bot.message_handler(regexp=('Email: [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'))
def complete_registration(message):
    mail = message.text.split(' ')[1]
    user = User(id=message.from_user.id, username=message.from_user.first_name, email=mail)
    db.session.add(user)
    db.session.commit()
    bot.send_message(message.from_user.id, "Реєстрація пройшла успішно!\n"
                                           "Тепер ви можете приступити до покупки квитків")


@bot.message_handler(commands=['admin'])
def start_as_admin(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    bot.send_message(message.from_user.id, "Введи данні, щоб продовжити як адмінстратор, за форматом:\n"
                                           "Admin: username|Password: ****")


@bot.message_handler(commands=['tickets'])
def get_all_tickets(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    list_of_tickets_dict = JSONWorker.get_list_of_object_by_key('json_files/tickets.json', 'name_of_buyer', message.from_user.first_name)
    if len(list_of_tickets_dict) == 0:
        bot.send_message(message.from_user.id, 'Ти ще не купив жодного квитка')
        return None
    bot.send_message(message.from_user.id, 'Твої квитки:')
    obj_list = []
    for ticket_dict in list_of_tickets_dict:
        obj_list.append(DeserializeTickets(ticket_dict, ticket_dict['type']))
    for obj in obj_list:
        bot.send_message(message.from_user.id, obj.__str__(), parse_mode='html')


def DeserializeTickets(tickets_dict, type):
    if type == 'regular_ticket':
        return RegularTicket(**tickets_dict)
    elif type == 'student_ticket':
        return StudentTicket(**tickets_dict)
    elif type == 'advance_ticket':
        return AdvanceTicket(**tickets_dict)
    elif type == 'late_ticket':
        return LateTicket(**tickets_dict)

@bot.message_handler(regexp=('Admin: admin|Password: admin'))
def create_event(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    user.admin = True
    db.session.commit()
    bot.send_message(message.from_user.id, "Введіть назву івенту за форматом:\n"
                                           "<b>EventName: event_name</b>", parse_mode='html')


@bot.message_handler(regexp=('EventName: \w+'))
def add_event_name(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    event_name = message.text.split(' ')[1]
    try:
        event.name = event_name
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще" + e.__str__())
    bot.send_message(message.from_user.id, "Введіть кількіст квитків за форматом:\n"
                                           "<b>NumberOfTickets: number</b>", parse_mode='html')


@bot.message_handler(regexp=('NumberOfTickets: [0-9]+'))
def add_event_number_of_tickets(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    number_of_ticket = message.text.split(' ')[1]
    try:
        event.number_of_tickets = number_of_ticket
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        return None
    bot.send_message(message.from_user.id, "Введіть вартість квитка:\n"
                                           "<b>Price: number</b>", parse_mode='html')


@bot.message_handler(regexp='Price: [0-9]+')
def add_event_number_of_tickets(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    price = message.text.split(' ')[1]
    try:
        event.ticket_cost = price
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        return None
    bot.send_message(message.from_user.id, "Введіть дату проведення за форматом:\n"
                                           "<b>Date: dd/mm/yyyy</b>", parse_mode='html')


@bot.message_handler(regexp=('Date: (1[0-2]|0?[1-9]|3[0-1])\/(0?[0-9]|1[0-2])\/(20[2-9][1-9])'))
def add_event_date(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    date_in_string = message.text.split(' ')[1]
    try:
        event.date = datetime.strptime(date_in_string, '%d/%m/%y')
    except Exception:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        return None
    bot.send_message(message.from_user.id, 'Якщо ти вніс усю необхідну інформацію, введи <b>admin --save</b>, '
                     'щоб зберегти подію', parse_mode='html')


@bot.message_handler(regexp='admin --save')
def save_ivent(message):
    id = message.from_user.id
    status, eror_mess = check_user_as_admin(id)
    if not status:
        bot.send_message(id, eror_mess)
        return None
    if event.name is None:
        bot.send_message(id, "У події немає назви, зроби з цим щось")
        return None
    if event.date is None:
        bot.send_message(id, "Цікаво, івент без дати, ти впевнений, що все з тобою добре, введи, будь ласка, дату"
                             " і сходи до лікаря)")
        return None
    if event.number_of_tickets is None:
        bot.send_message(id, "Введи, будь ласка, кількість квитків)")
        return None
    JSONWorker.save_to_json('json_files/events.json', event)
    S3Manager.upload_object('json_files/events.json', EVENTS_KEY)


def check_user_as_admin(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return False, "Спочатку зареєструйся"
    if not user.admin:
        return False, "На жаль, у тебе немає прав на це"
    return True, ''


@bot.message_handler(commands=['buy'])
def start_buying(message):
    S3Manager.download_object('json_files/events.json', EVENTS_KEY)
    S3Manager.download_object('json_files/tickets.json', TICKETS_KEY)
    names = JSONWorker.get_list_of_parameter_values('json_files/events.json', 'name')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    keyboard.add(types.KeyboardButton(text='Так'))
    keyboard.add(types.KeyboardButton(text='Ні'))
    bot.send_message(message.from_user.id, 'Ти студент?', reply_markup=keyboard)
    bot.register_next_step_handler(message, choose_event)


def choose_event(message):
    global student_status
    student_status = message.text
    names = JSONWorker.get_list_of_parameter_values('json_files/events.json', 'name')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for name in names:
        keyboard.add(types.KeyboardButton(text=name))
    bot.send_message(message.from_user.id, 'Обери подію, яку хочеш відвідати: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_info_about_event)


def get_info_about_event(message):
    chosen_event_dict = JSONWorker.get_event_by_param_value('json_files/events.json', 'name', message.text)
    if chosen_event_dict['number_of_tickets'] == 0:
        bot.send_message(message.from_user.id, "На жаль, всі квитки на цю подію були розкуплені")
        return
    JSONWorker.update_value(json_filename='json_files/events.json',
                            name_of_key_value='event_id',
                            obj_id_to_update=chosen_event_dict['event_id'],
                            name_to_update='number_of_tickets',
                            new_value=chosen_event_dict['number_of_tickets'] - 1)
    ticket = ticket_factory(chosen_event_dict, message.from_user.first_name, student_status)
    JSONWorker.save_to_json('json_files/tickets.json', ticket)
    S3Manager.upload_object('json_files/tickets.json', TICKETS_KEY)
    bot.send_message(message.from_user.id, f'Ось твій квиток:\n{ticket.__str__()}', parse_mode='html')
    bot.send_message(message.from_user.id, 'Щоб подивитися список всіх куплених квитків, обери команду: <b>/tickets</b>',
                                           parse_mode='html')


def ticket_factory(_event, user_name, student_status):
    if student_status == 'Так':
        return StudentTicket(_event['ticket_cost'], _event['event_id'], user_name, datetime.today())
    date_of_event = datetime.strptime(_event['date'], '%d/%m/%y')
    event_date = date(date_of_event.year, date_of_event.month, date_of_event.day)
    delta = abs(date.today() - event_date)
    if delta.days > 60:
        return AdvanceTicket(_event['ticket_cost'], _event['event_id'], user_name, datetime.today())
    if delta.days <= 10:
        return LateTicket(_event['ticket_cost'], _event['event_id'], user_name, datetime.today())
    return RegularTicket(_event['ticket_cost'], _event['event_id'], user_name, datetime.today())


@bot.message_handler(content_types='text')
def respond_to_absurd(message):
    bot.send_animation(message.from_user.id, open(UnknownText, 'rb'))
    bot.send_message(message.from_user.id, "Вибач, але я не знаю, що ти маєш на увазі :(")
    pass


@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "Author is konch", 200


if __name__ == "__main__":
    if ENV == 'dev':
        bot.remove_webhook()
        bot.polling(none_stop=True)
    else:
        app.debug = False
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
