from datetime import datetime

from app import db
from app.models.blog import Post


class User(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    about_me = db.Column(db.String(140))
    location = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    lastvisit = db.Column(db.DateTime)
    regdate = db.Column(db.DateTime, default=datetime.utcnow())
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.uid)

    def is_admin(self):
        if self.admin:
            return True
        return False

    def __repr__(self):
        return "User %s" % self.username
