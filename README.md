Hey!
============
I wanted to write an web application with python.. so I did :)

Python is my first programming language that I've learned (self-assessment: beginner) but I think I'm getting better ^^

Feedback is very appreciated!


btw, this app is currently in development - I'll add new features when I have time.

Working example: [someblocks.com](http://someblocks.com/)

LICENSE
============
GPL


Installation
============
First of all make an virtualenv and then you can install the dependencies with `venv_dir/bin/pip install -r requirements.txt`

Dependencies
------------
* Flask

    `pip install flask`

* Flask-SQLAlchemy

    `pip install flask-sqlalchemy`

* Flask-WTF

    `pip install flask-wtf`

* Flask-Login

    `pip install flask-login`

* Flask-Bootstrap

    `pip install flask-bootstrap`

* Flask-Script

    `pip install flask-script` - handles the manage.py file

* Flask-Misaka

    `pip install flask-misaka` - Markdown support

* Flask-Alembic

    `pip install -e git+https://github.com/tobiasandtobias/flask-alembic.git#egg=Package`

* alembic

    `pip install alembic`

* feedparser

    `pip install feedparser`

* mcstatus

    `git submodule init` && `git submodule update`


Resources used to learn how to build a webapp with Flask
==============
* http://flask.pocoo.org/docs/
* https://github.com/mitsuhiko/flask/wiki/Large-app-how-to
* http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


How To
==============
* `python2 manage.py db_create`

    This will create the database

* `python2 manage.py db_content`

    This will create some basic content

* `python2 manage.py db_migrate`

    Everytime you change a model you need to migrate your database

* `python2 manage.py runserver`

    Running the development server

To Do-List
==============
* Recovery E-Mail

* Caching?

* Groups (Admin, Member,...)

* Comments

* Maybe: Integrating a forum (MyBB?)
