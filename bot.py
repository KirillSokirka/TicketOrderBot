import re

from config import *
from models.Event import Event
from models.fake_models.EventForDeserialization import  EventForDeserialization
from models.fake_models.TicketForDeserialization import TicketForDeserialization
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
    user = User.query.filter_by(id=message.from_user.id).first()
    if user:
        bot.send_message(message.from_user.id, 'Ви вже зареєстровані!')
        return
    bot.send_message(message.from_user.id,
                     'Ввведіть свій email: example@exmpl.ex</b>',
                     parse_mode='html')
    bot.register_next_step_handler(message, complete_registration)


def complete_registration(message):
    if not re.match('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', message.text):
        bot.send_message(message.from_user.id, 'Некоректний email, спробуй ще')
        bot.register_next_step_handler(message, complete_registration)
    user = User(id=message.from_user.id, username=message.from_user.first_name, email=message.text)
    db.session.add(user)
    db.session.commit()
    bot.send_message(message.from_user.id, "Реєстрація пройшла успішно!\n"
                                           "Тепер ви можете приступити до покупки квитків")


@bot.message_handler(commands=['buy'])
def start_buying(message):
    S3Manager.download_object('json_files/events.json', EVENTS_KEY)
    S3Manager.download_object('json_files/tickets.json', TICKETS_KEY)
    names = JSONWorker.get_values_by_parameter_name('json_files/events.json', 'name')
    if len(names) == 0:
        bot.send_message(message.from_user.id, "На жаль, поки немає доступних івентів")
        return None
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    keyboard.add(types.KeyboardButton(text='Так'))
    keyboard.add(types.KeyboardButton(text='Ні'))
    bot.send_message(message.from_user.id, 'Ти студент?', reply_markup=keyboard)
    bot.register_next_step_handler(message, choose_event)


def choose_event(message):
    global student_status
    student_status = message.text
    names = JSONWorker.get_values_by_parameter_name('json_files/events.json', 'name')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for name in names:
        keyboard.add(types.KeyboardButton(text=name))
    message = bot.send_message(message.from_user.id, 'Обери подію, яку хочеш відвідати: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_info_about_event)


def get_info_about_event(message):
    S3Manager.download_object('json_files/events.json', EVENTS_KEY)
    chosen_event_dict = JSONWorker.get_object_by_key('json_files/events.json', 'name', message.text)
    _event = EventForDeserialization(**chosen_event_dict)
    bot.send_message(message.from_user.id, 'Івент:\n' + _event.__str__(), parse_mode='html')
    if _event.number_of_tickets == 0:
        bot.send_message(message.from_user.id, "На жаль, всі квитки на цю подію були розкуплені")
        return None
    sell_ticket(message.from_user.id, message.from_user.first_name, _event)


def sell_ticket(chat_id, first_name, _event : EventForDeserialization):
    JSONWorker.update_value(json_filename='json_files/events.json',
                            name_of_key_value='id',
                            obj_id_to_update=_event.id,
                            name_to_update='number_of_tickets',
                            new_value=_event.number_of_tickets - 1)
    ticket = ticket_factory(_event, first_name, student_status)
    JSONWorker.save_to_json('json_files/tickets.json', ticket)
    S3Manager.upload_object('json_files/tickets.json', TICKETS_KEY)
    bot.send_message(chat_id, f'Ось твій квиток:\n{ticket.__str__()}', parse_mode='html')
    bot.send_message(chat_id, 'Щоб подивитися список всіх куплених квитків, обери команду: <b>/tickets</b>',
                     parse_mode='html')


def ticket_factory(_event, user_name, student_status):
    if student_status == 'Так':
        return StudentTicket(_event.ticket_cost, _event.id, user_name, datetime.today())
    date_of_event = datetime.strptime(_event.date, '%d/%m/%Y')
    event_date = date(date_of_event.year, date_of_event.month, date_of_event.day)
    delta = abs(date.today() - event_date)
    if delta.days > 60:
        return AdvanceTicket(_event.ticket_cost, _event.id, user_name, datetime.today())
    if delta.days <= 10:
        return LateTicket(_event.ticket_cost, _event.id, user_name, datetime.today())
    return RegularTicket(_event.ticket_cost, _event.id, user_name, datetime.today())


@bot.message_handler(commands=['events'])
def get_all_events(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    S3Manager.download_object('json_files/events.json', EVENTS_KEY)
    list_of_events_dict = JSONWorker.get_all_objects('json_files/events.json')
    if len(list_of_events_dict) == 0:
        bot.send_message(message.from_user.id, 'На жаль, поки немає доступних івентів :(')
    events = []
    for event_dict in list_of_events_dict:
        events.append(EventForDeserialization(**event_dict))
    bot.send_message(message.from_user.id, 'Доступні івенти: ')
    for event in events:
        bot.send_message(message.from_user.id, event.__str__(), parse_mode='html')


@bot.message_handler(commands=['tickets'])
def get_all_tickets(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    S3Manager.download_object('json_files/tickets.json', TICKETS_KEY)
    list_of_tickets_dict = JSONWorker.get_list_of_object_by_key('json_files/tickets.json', 'name_of_buyer', message.from_user.first_name)
    if len(list_of_tickets_dict) == 0:
        bot.send_message(message.from_user.id, 'Ти ще не купив жодного квитка')
        return None
    obj_list = []
    for ticket_dict in list_of_tickets_dict:
        obj_list.append(TicketForDeserialization(**ticket_dict))
    bot.send_message(message.from_user.id, 'Твої квитки:')
    for obj in obj_list:
        bot.send_message(message.from_user.id, obj.__str__(), parse_mode='html')


@bot.message_handler(commands=['admin'])
def start_admin_registration(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    bot.send_message(message.from_user.id, "Введи данні, щоб продовжити як адмінстратор, за форматом:\n"
                                           "Admin: username|Password: ****")
    bot.register_next_step_handler(message, register_as_admin)


def register_as_admin(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    if not re.match('Admin: admin|Password: admin',message.text):
        bot.send_message(message.from_user.id, 'Ви ввели некоректні данні, спробуйте ще раз, почавши процес реєстрації знову')
        return None
    user.admin = True
    db.session.commit()
    bot.send_message(message.from_user.id, 'Вітаю Вас, тепер ви можете створювати події')


@bot.message_handler(commands=['create_event'])
def create_event(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    bot.send_message(message.from_user.id, "Введіть назву івенту:")
    bot.register_next_step_handler(message, add_event_name)


def add_event_name(message):
    try:
        global event
        event.name = message.text
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        bot.register_next_step_handler(message, add_event_name)
        return
    bot.send_message(message.from_user.id, "Введіть кількість квитків: ")
    bot.register_next_step_handler(message, add_event_number_of_tickets)


def add_event_number_of_tickets(message):
    try:
        global event
        event.number_of_tickets = message.text
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        bot.register_next_step_handler(message, add_event_number_of_tickets)
        return
    bot.send_message(message.from_user.id, "Введіть вартість одного квитка:")
    bot.register_next_step_handler(message, add_event_cost_of_tickets)


def add_event_cost_of_tickets(message):
    try:
        global event
        event.ticket_cost = message.text
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        bot.register_next_step_handler(message, add_event_number_of_tickets)
        return
    bot.send_message(message.from_user.id, "Введіть дату проведення за форматом:\n"
                                           "<b>dd/mm/yyyy</b>", parse_mode='html')
    bot.register_next_step_handler(message, add_event_date)


def add_event_date(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return
    try:
        event.date = message.text
    except Exception:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        bot.register_next_step_handler(message, add_event_date)
        return
    try:
        JSONWorker.save_to_json('json_files/events.json', event)
        S3Manager.upload_object('json_files/events.json', EVENTS_KEY)
    except Exception as e:
        bot.send_message(message.from_user.id, "Під час збереження івенту щось пішло не так, спробуйте трохи пізніше")
        bot.register_next_step_handler(message, add_event_date)
        return
    bot.send_message(message.from_user.id, 'Вітаю івент створено')
    return


def check_user_as_admin(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return False, "Спочатку зареєструйся"
    if not user.admin:
        return False, "На жаль, у тебе немає прав на це"
    return True, ''


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
    return "Ok", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "Ok", 200


if __name__ == "__main__":
    if ENV == 'dev':
        bot.remove_webhook()
        bot.polling(none_stop=True)
    else:
        app.debug = False
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
