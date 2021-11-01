import os
import telebot
from flask import Flask, request

TOKEN = "2089991556:AAFb0igp6cEFMoKKTq7Wdcg9JIDTPEExzDU"
APP_URL = f"https://tickeeeeter.herokuapp.com/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handlers(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, " + message.from_user.first_name)


@server.route("/" + TOKEN, method=["POST"])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates(update)
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
