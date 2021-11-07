import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

HelloSticker = 'stickers/HelloUser.tgs'
UnknownText = 'stickers/UnknownText.tgs'
BOT_TOKEN = '2089991556:AAFb0igp6cEFMoKKTq7Wdcg9JIDTPEExzDU'
APP_URL = f'https://tickteeeeeeeer.herokuapp.com/{BOT_TOKEN}'
LOCAL_DB = 'postgresql+psycopg2://postgres:aa6400vt@localhost:5432/ticketeerdb'
HEROKU_DB = os.getenv('DATABASE_URL')
ENV = 'prod'

app = Flask(__name__)
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB
else:
    uri = HEROKU_DB
    if uri.startswith("postgres"):
        uri = uri.replace("postgres", "postgresql+psycopg2")
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

FINAL_DB_URL = app.config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
