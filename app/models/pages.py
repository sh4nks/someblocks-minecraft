from datetime import datetime

from app import db


class Page(db.Model):
    __tablename__ = "pages"

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    category = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))

    def __repr__(self):
        return "Category: %s" % self.category
