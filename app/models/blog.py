from datetime import datetime

from app import db
from app.models.users import User


class Post(db.Model):
    __tablename__ = "posts"

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
