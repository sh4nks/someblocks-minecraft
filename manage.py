#!/usr/bin/env python
from datetime import datetime

from werkzeug import generate_password_hash
from flask import current_app
from flask.ext.script import Manager, Server, Shell
from flask.ext.alembic import ManageMigrations

from app import app, db
from app.models.users import User, Group, Permission
from app.models.blog import Post


manager = Manager(app)
manager.add_command("runserver", Server("localhost", port=8080))


def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command("migrate", ManageMigrations())


@manager.command
def db_create():
    """ Creates the database """
    db.create_all()


@manager.command
def db_content():
    """ Adds sample content """

    title_data = "Markdown Example"

    body_data = """# This is an H1

## This is an H2

###### This is an H6




> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
>
> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
> id sem consectetuer libero luctus adipiscing.




> This is the first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.




> ## This is a header.
>
> 1.   This is the first list item.
> 2.   This is the second list item.
>
> Here's some example code:
>
>     return shell_exec("echo $input | $markdown_script");




*   Red
*   Green
*   Blue



1.  Bird
2.  McHale
3.  Parish




##### Code-Block
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

    if __name__ == "__main__":
        app.run()"""

    groups = [('Administrators', 'Administrator'),
              ('Moderators', 'Moderator'),
              ('Members', 'Member'),
              ('Banned', 'Banned'),
              ('Inactive', 'Inactive')]

    for grouptitle, usertitle in groups:
        group = Group(grouptitle, usertitle)
        db.session.add(group)

    pw = generate_password_hash("change_me")

    user1 = User(username="admin", email="admin@example.com", password=pw,
                 regdate=datetime.utcnow(), group_id=1)
    user2 = User(username="mod", email="mod@example.com", password=pw,
                regdate=datetime.utcnow(), group_id=2)
    user3 = User(username="member", email="member@example.com", password=pw,
                regdate=datetime.utcnow(), group_id=3)
    user4 = User(username="inactive", email="inactiv@example.com", password=pw,
                regdate=datetime.utcnow(), group_id=5)
    user5 = User(username="test_user", email="test@example.com", password=pw,
                regdate=datetime.utcnow())

    db.session.add_all([user1, user2, user3, user4, user5])

    post = Post(title=title_data, body=body_data,
                date_created=datetime.utcnow(), user_id=1)

    db.session.add(post)

    perms = [(1, True, True, True, True, False),
             (2, False, True, True, True, False),
             (3, False, False, True, True, False),
             (4, False, False, False, False, True),
             (5, False, False, False, True, False)]

    for group_id, admin, edit_post, compose_post, post_comment, banned in perms:
        perm = Permission(group_id=group_id, admin=admin,
                          edit_post=edit_post, compose_post=compose_post,
                          post_comment=post_comment, banned=banned)

        db.session.add(perm)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
