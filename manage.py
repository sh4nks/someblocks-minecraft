#!/usr/bin/env python
from datetime import datetime

from werkzeug import generate_password_hash
from flask import current_app
from flask.ext.script import Manager, Server, Shell

from someblocks import create_app
from someblocks.extensions import db
from someblocks.models.users import User
from someblocks.models.blog import Post

app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server("localhost", port=8080))


def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def initdb():
    """ Creates the database """
    db.create_all()


@manager.command
def initall():
    """ Creates the database and adds some sample content """

    db.create_all()

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

    pw = generate_password_hash("change_me")

    user1 = User(username="admin", email="admin@example.com", password=pw,
                 regdate=datetime.utcnow(), admin=True)
    user2 = User(username="member", email="member@example.com", password=pw)

    db.session.add_all([user1, user2])

    post = Post(title=title_data, body=body_data,
                date_created=datetime.utcnow(), user_id=1)

    db.session.add(post)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
