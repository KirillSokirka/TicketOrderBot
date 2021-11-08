import os


HelloSticker = 'stickers/HelloUser.tgs'
UnknownText = 'stickers/UnknownText.tgs'
BOT_TOKEN = '2089991556:AAFb0igp6cEFMoKKTq7Wdcg9JIDTPEExzDU'
APP_URL = f'https://tickteeeeeeeer.herokuapp.com/{BOT_TOKEN}'
LOCAL_DB = 'postgresql+psycopg2://postgres:aa6400vt@localhost:5432/ticketsdb'
HEROKU_DB = os.getenv('DATABASE_URL')
