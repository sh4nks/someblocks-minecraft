from datetime import datetime

from ..extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    cid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))
    date_created = db.Column(db.DateTime)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.pid",
                                                  use_alter=True,
                                                  name="fk_post_id"))


class Post(db.Model):
    __tablename__ = "posts"

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))
    comments = db.relationship("Comment", backref="comments", lazy="joined")

    comment_count = db.column_property(
        db.select([db.func.count(Comment.cid)]).
            where(Comment.post_id == pid).as_scalar())

    def __repr__(self):
        return "Title: %s" % self.title
