from flask import render_template
from flask.ext.mail import Message
from app import mail
from decorators import async


def send_new_password(user, password):
    send_email("Password Reset", user.email,
        render_template("email/reset_password.txt", user=user, password=password),
        render_template("email/reset_password.html", user=user, password=password)
    )


@async
def send_async_email(msg):
    mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender=''):
    if not sender:
        msg = Message(subject, recipients=recipients)
    else:
        msg = Message(subject, sender=sender, recipients=recipients)

    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)
