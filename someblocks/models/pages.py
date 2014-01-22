from datetime import datetime

from ..extensions import db


class Page(db.Model):
    __tablename__ = "pages"

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    url = db.Column(db.String, unique=True)
    external = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))

    def __repr__(self):
        return "URL: %s" % self.url
