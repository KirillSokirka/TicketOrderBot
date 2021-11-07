from config import db


class User(db.Model):
    __tablename__ = "usersss"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=True)
    email = db.Column(db.String(200), unique=False, nullable=True)
