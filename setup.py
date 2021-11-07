import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


server = Flask(__name__)
uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
server.config['SQLALCHEMY_DATABASE_URI'] = uri
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)