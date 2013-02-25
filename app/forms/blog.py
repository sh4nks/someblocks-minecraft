from flask.ext.wtf import Form, TextField, Required, Length, TextAreaField


class PostForm(Form):
    title = TextField("Title:", validators=[
        Required(message="A title is required"),
        Length(min=0, max=140)])

    body = TextAreaField("Content:", validators=[
        Required(message="You can't submit a post without a content")])


class CommentForm(Form):
    content = TextAreaField("Comment:", validators=[
        Required(message="You can't submit a comment without content")])
