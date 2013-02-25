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
    regdate = db.Column(db.DateTime)
    timeonline = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, db.ForeignKey("user_groups.gid"))
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
        perm = Permission.query.join(
            Group, (Permission.group_id == Group.gid)).\
            filter(Permission.group_id == self.group_id,
                   Permission.admin == True).first()
        if perm:
            return True
        return False

    def can_compose_post(self):
        perm = Permission.query.join(
            Group, (Permission.group_id == Group.gid)).\
            filter(Permission.group_id == self.group_id,
                   Permission.compose_post == True).first()

        if perm:
            return True
        return False

    def can_post_comment(self):
        perm = Permission.query.join(
            Group, (Permission.group_id == Group.gid)).\
            filter(Permission.group_id == self.group_id,
                   Permission.post_comment == True).first()

        if perm:
            return True
        return False

    def can_edit_post(self, post_id):
        perm = Post.query.filter(Post.pid == post_id,
                                 Post.user_id == self.uid).first()

        if perm:
            return True
        return False

    def __repr__(self):
        return "User %s" % self.username


class Permission(db.Model):
    __tablename__ = "permissions"

    pid = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("user_groups.gid"))
    admin = db.Column(db.Boolean)
    edit_post = db.Column(db.Boolean)
    compose_post = db.Column(db.Boolean)
    post_comment = db.Column(db.Boolean)
    banned = db.Column(db.Boolean)

    def __repr__(self):
        return "admin %s ## edit_post %s" % (self.admin, self.edit_post)


class Group(db.Model):
    __tablename__ = "user_groups"

    gid = db.Column(db.Integer, primary_key=True)
    grouptitle = db.Column(db.String(120))
    usertitle = db.Column(db.String(120))
    userstyle = db.Column(db.String(200))
    description = db.Column(db.Text)
    rank = db.Column(db.Integer)
    rankimage = db.Column(db.String(120))
    user = db.relationship("User", backref="account", lazy="dynamic")

    def __init__(self, grouptitle=None, usertitle=None):
        self.grouptitle = grouptitle
        self.usertitle = usertitle

    def get_gid(self):
        return unicode(self.gid)

    def get_grouptitle(self):
        return unicode(self.grouptitle)

    def __repr__(self):
        return "Group %s" % self.grouptitle
