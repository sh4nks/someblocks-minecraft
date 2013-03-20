# Hey!


This app is currently in development

You can view a working example [here](http://someblocks.com/)

Feedback and contributions are highly appreciated!

#LICENSE
GPL


# Installation
First of all create an virtualenv and install the dependencies as described below

* Create the virtualenv

    `virtualenv .venv`

* Activate your virtualenv

    `source .venv/bin/activate`

* Install dependencies via `requirements.txt`

    `pip install -r requirements.txt`

## Dependencies
* Flask

    `pip install flask`

* Flask-SQLAlchemy

    `pip install flask-sqlalchemy`

* Flask-WTF

    `pip install flask-wtf`

* Flask-Login

    `pip install flask-login`

* Flask-Script

    `pip install flask-script` - handles the manage.py file

* Flask-Misaka

    `pip install flask-misaka` - Markdown support

* Flask-Cache

    `pip install flask-cache` - Caching support

* feedparser

    `pip install feedparser`

* mcstatus

    `git submodule init` && `git submodule update`


# Resources used to learn how to build a webapp with Flask
* http://flask.pocoo.org/docs/
* https://github.com/mitsuhiko/flask/wiki/Large-app-how-to
* http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


# How To
* `python2 manage.py db_create`

    This will create the database

* `python2 manage.py db_content`

    This will create some basic content

* `python2 manage.py runserver`

    Running the development server

# ToDo-List
* Caching

* Migrations
