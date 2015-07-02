#!/usr/bin/env python
from flask import current_app
from flask.ext.script import Manager, Server, Shell

from someblocks import create_app

app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server("localhost", port=8080))


def make_shell_context():
    return dict(app=current_app)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()
