from app import db


class Post(db.Model):
    __tablename__ = "posts"

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))
    comments = db.relationship("Comment", backref="comments", lazy="dynamic")

    def __repr__(self):
        return "Title: %s" % self.title


class Comment(db.Model):
    __tablename__ = "comments"

    cid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))
    date_created = db.Column(db.DateTime)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.pid"))
