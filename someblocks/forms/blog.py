from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Length


class PostForm(Form):
    title = TextField("Title:", validators=[
        Required(message="A title is required"),
        Length(min=0, max=140)])

    body = TextAreaField("Content:", validators=[
        Required(message="You can't submit a post without a content")])


class CommentForm(Form):
    content = TextAreaField("Comment:", validators=[
        Required(message="You can't submit a comment without content")])
