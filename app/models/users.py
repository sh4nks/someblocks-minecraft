from app import db


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
    regdate = db.Column(db.DateTime)
    timeonline = db.Column(db.DateTime)
    usergroup = db.Column(db.Integer, db.ForeignKey("usergroups.gid"))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.uid)

    def __repr__(self):
        return self.username


class Groups(db.Model):
    __tablename__ = "usergroups"

    gid = db.Column(db.Integer, primary_key=True)
    grouptitle = db.Column(db.String(120))
    usertitle = db.Column(db.String(120))
    userstyle = db.Column(db.String(200))
    description = db.Column(db.Text)
    rank = db.Column(db.Integer)
    rankimage = db.Column(db.String(120))

    def __init__(self, grouptitle=None, usertitle=None):
        self.grouptitle = grouptitle
        self.usertitle = usertitle
