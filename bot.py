from Models.User import User
from setup import app, db

import os
import telebot
from flask import request

bot = telebot.TeleBot(os.environ.get('TOKEN'))


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
    user = User(id=message.from_user.id, username=message.from_user.username, email=mail)
    db.session.add(user)
    db.session.commit()


@app.route('/' + os.environ.get('TOKEN'), methods=['POST'])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('APP_URL'))
    return "!", 200


app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
