from config import *
from models.Event import Event

import telebot
import datetime
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

bot = telebot.TeleBot(BOT_TOKEN)
event = Event

ENV = 'dev'

app = Flask(__name__)
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB
else:
    uri = HEROKU_DB
    if uri.startswith("postgres"):
        uri = uri.replace("postgres", "postgresql+psycopg2")
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    admin = db.Column(db.BOOLEAN, unique=False, nullable=True)


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
    user.admin = True
    event.event_id = 1
    event.name = "Blayat"
    event.date = datetime.date.today()
    event.number_of_ticket = 120
    event.save_to_file()
    pass


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
    return "!", 200


if __name__ == "__main__":
    if ENV == 'dev':
        bot.remove_webhook()
        bot.polling(none_stop=True)
    else:
        app.debug = False
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
