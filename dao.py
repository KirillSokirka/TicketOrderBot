from imports import server

import os


def initialize_db():
    uri = os.environ.get('DATABASE_URL')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    server.config['SQLALCHEMY_DATABASE_URI'] = uri
