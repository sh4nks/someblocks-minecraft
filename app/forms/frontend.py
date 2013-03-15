from flask.ext.wtf import Form, TextField, Required, Length, TextAreaField


class PageForm(Form):
    title = TextField("Title:", validators=[
        Required(message="A title is required"), Length(min=0, max=140)])
    content = TextAreaField("Content:", validators=[
        Required(message="You can't submit a post without a content")])
