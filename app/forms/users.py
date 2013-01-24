from flask import request
from flask.ext.wtf import (Form, TextField, PasswordField, BooleanField, HiddenField,
                           RecaptchaField, Required, Email, EqualTo, Length,
                           TextAreaField, SelectField, ValidationError, regexp)

from app import db
from app.models.users import User


is_username = regexp(r'^[\w.+-]+$',
                     message="You can only use letters, numbers or dashes")


class LoginForm(Form):
    username = TextField("Username", validators=[
        Required(message="Username required")])

    password = PasswordField("Password", validators=[
        Required(message="Password required")])

    remember_me = BooleanField("Remember Me", default=False)


class RegisterForm(Form):
    username = TextField("Username", validators=[
        Required(message="Username required"),
        is_username])

    email = TextField("E-Mail", validators=[
        Required(message="Email adress required"),
        Email(message="This email is invalid")])

    password = PasswordField("Password", validators=[
        Required(message="Password required")])

    confirm_password = PasswordField("Confirm Password", [
        Required(message="Confirm Password required"),
        EqualTo("password", message="Passwords do not match")
        ])

    accept_tos = BooleanField("Accept Terms of Service", default=True)

    #recaptcha = RecaptchaField()

    def validate_username(self, field):
        user = User.query.filter_by(username = field.data).first()
        if user:
            raise ValidationError("This username is taken")

    def validate_email(self, field):
        email = User.query.filter_by(email = field.data).first()
        if email:
            raise ValidationError("This email is taken")


class ResetPasswordForm(Form):
    email = TextField("E-Mail", validators=[
        Required(message="Email required"),
        Email(message="This email is invalid")])

    username = TextField("Username", validators=[
        Required(message="Username required")])

    def validate_username(self, field):
        user = User.query.filter_by(username = field.data).first()
        if not user:
            raise ValidationError("Wrong username?")

    def validate_email(self, field):
        email = User.query.filter_by(email = field.data).first()
        if not email:
            raise ValidationError("Wrong E-Mail?")


class ProfileForm(Form):
    fullname = TextField("Your Name:", validators=[
        Length(min = 0, max = 50)])

    location = TextField("Location:", validators=[
        Length(min = 0, max = 50)])

    sex = SelectField("Sex:", default="Undisclose", choices=[
        ("Undisclose", "Undisclose"),
        ("Male", "Male"),
        ("Female", "Female")])

    about_me = TextAreaField("About Me:", validators=[
        Length(min = 0, max = 140)])
