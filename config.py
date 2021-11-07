import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BOT_TOKEN = '2089991556:AAFb0igp6cEFMoKKTq7Wdcg9JIDTPEExzDU'
APP_URL = f'https://ticketeeeeeer.herokuapp.com/{BOT_TOKEN}'
LOCAL_DB = 'postgresql+psycopg2://postgres:aa6400vt@localhost:5432/ticketeerdb'
HEROKU_DB = 'postgres://migbjnrupsajgx:62aa9d096b73c7030aff5db3cd454318f8e87fc5b7cd2ac30af99bb8c205c5cd@ec2-3-214-121' \
            '-14.compute-1.amazonaws.com:5432/ddfmchhkrlkcvl '
ENV = 'prod'

app = Flask(__name__)
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB
else:
    uri = HEROKU_DB
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

FINAL_DB_URL = app.config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
