from flask.ext.wtf import (Form, TextField, Required, Email, Length,
                           TextAreaField, URL, optional)


class PostForm(Form):
    title = TextField("Title:", validators=[
        Required(message="A title is required"),
        Length(min=0, max=140)])

    body = TextAreaField("Content:", validators=[
        Required(message="You can't submit a post without a content")])


class CommentForm(Form):
    nickname = TextField("Nickname:", validators=[
        Required(message="A nickname is required")])

    email = TextField("E-Mail:", validators=[
        Required(message="A E-Mail adress is required"),
        Email(message="A valid email is required")])

    website = TextField("Website:", validators=[
        optional(),
        URL(message="A valid URL is required")])

    comment = TextAreaField("Comment:", validators=[
        Required(message="You can't submit a comment without content")])
