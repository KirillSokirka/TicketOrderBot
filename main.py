import os
import telebot
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

bot = telebot.TeleBot(os.environ.get('TOKEN'))
server = Flask(__name__)
db = SQLAlchemy(server)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, " + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


@server.route('/' + os.environ.get('TOKEN'), methods=['POST'])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('APP_URL'))
    return "!", 200


uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

server.config['SQLALCHEMY_DATABASE_URI'] = uri
server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
