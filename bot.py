from config import *
from models.user import User

import telebot
from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, " + message.from_user.first_name)


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

    from sqlalchemy_utils import database_exists, drop_database, create_database
    if database_exists(FINAL_DB_URL):
        drop_database(FINAL_DB_URL)
    if not database_exists(FINAL_DB_URL):
        create_database(FINAL_DB_URL)
    db.create_all()

if ENV == 'dev':
    bot.remove_webhook()
    bot.polling(none_stop=True)
else:
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
