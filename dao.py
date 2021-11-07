import config

from sqlalchemy import create_engine

ENV = 'dev'
if ENV == 'dev':
    engine = create_engine(config.LOCAL_DB)
else:
    uri = config.HEROKU_DB
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    engine = create_engine(uri)
