#!/usr/bin/env python
from werkzeug import generate_password_hash
from datetime import datetime

from flask import current_app

from flask.ext.script import Manager, Command, Server, Shell
from flask.ext.alembic import ManageMigrations

from app import app, db
from app.models.users import User, Groups
from app.models.blog import Post


manager = Manager(app)
manager.add_command("runserver", Server("localhost", port=8000))


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



    # I still need to implement this
    groups = [
        [('Administrators'), ('Administrator')],
        [('Moderators'), ('Moderator')],
        [('Members'), ('Member')],
        [('Guests'), ('Guest')],
        [('Banned'), ('Banned')],
        [('Inactive'), ('Inactive')]
    ]

    user = User("admin", "admin@example.com", \
            generate_password_hash("change_me"))
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username = "admin").first()
    user.regdate = datetime.utcnow()
    user.usergroup = 1
    db.session.add(user)

    for grouptitle, usertitle in groups:
        group = Groups(grouptitle, usertitle)
        db.session.add(group)

    post = Post(title=title_data, body=body_data, \
                date_created=datetime.utcnow(), user_id=1)

    db.session.add(post)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
