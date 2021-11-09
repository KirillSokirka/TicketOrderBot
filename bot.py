from config import *
from models.Event import Event
from models.User import User
from models.tickets.RegularTicket import RegularTicket
from helpers.s3manager import S3Manager
from helpers.jsonWorker import JSONWorker


import telebot
from telebot import types
from datetime import datetime
from flask import request


bot = telebot.TeleBot(BOT_TOKEN)
event = Event()


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


@bot.message_handler(commands=["admin"])
def start_as_admin(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    bot.send_message(message.from_user.id, "Введи данні, щоб продовжити як адмінстратор, за форматом:\n"
                                           "Admin: username|Password: ****")


@bot.message_handler(regexp=('Admin: admin|Password: admin'))
def create_event(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, "Спочатку зареєструйся")
        return None
    user.admin = True
    db.session.commit()
    bot.send_message(message.from_user.id, "Введіть назву івенту за форматом:\n"
                                           "EventName: event_name")


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
                                           "NumberOfTickets: number")


@bot.message_handler(regexp=('NumberOfTickets: [0-9]+'))
def add_event_number_of_tickets(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    number_of_ticket = message.text.split(' ')[1]
    try:
        event.number_of_ticket = number_of_ticket
    except Exception as e:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        return None
    bot.send_message(message.from_user.id, "Введіть дату проведення за форматом:\n"
                                           "DateOfEvent: dd/mm/yyyy")


@bot.message_handler(regexp=('DateOfEvent: (1[0-2]|0?[1-9]|3[0-1])\/(0?[0-9]|1[0-2])\/(20[2-9][1-9])'))
def add_event_date(message):
    status, erormes = check_user_as_admin(message.from_user.id)
    if not status:
        bot.send_message(message.from_user.id, erormes)
        return None
    date_in_string = message.text.split(' ')[1]
    try:
        event.date = datetime.strptime(date_in_string, '%d/%m/%Y')
    except Exception:
        bot.send_message(message.from_user.id, "Щось пішло не так, спробуй ще")
        return None
    bot.send_message(message.from_user.id, 'Якщо ти вніс усю необхідну інформацію: <b>введи: admin --save</b>, '
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
    if event.number_of_ticket is None:
        bot.send_message(id, "Введи, будь ласка, кількість квитків)")
        return None
    event.save_to_file()
    S3Manager.upload_object('json_files/events.json', 'events.json')


def check_user_as_admin(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return False, "Спочатку зареєструйся"
    if not user.admin:
        return False, "На жаль, у тебе немає прав на це"
    return True, ''


@bot.message_handler(commands=['buy'])
def start_buying(message):
    S3Manager.download_object('json_files/events.json', 'events.json')
    names = JSONWorker.get_list_of_parameter_values('json_files/events.json', 'name')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for name in names:
        keyboard.add(types.KeyboardButton(text=name))
    bot.send_message(message.from_user.id, 'Обери подію, яку хочеш відвідати', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_info_about_event)


def get_info_about_event(message):
    choosen_event = JSONWorker.get_event_by_param_value('json_files/events.json', 'name', message.text)
    if choosen_event['number_of_tickets'] == 0:
        bot.send_message(message.from_user.id, "На жаль, всі квитки на цю подію були розкуплені")
        return
    ticket = RegularTicket(choosen_event['price'], choosen_event['id'], )
    bot.send_message(message.from_user.id, 'Ось твій квиток:\n'
                                            f'<b>id</b> - {choosen_event["id"]}\n'
                                            f'<b>name</b> - {choosen_event["name"]}\n'
                                            f'<b>date</b> - {choosen_event["date"]}',
                     parse_mode='html')


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
