from flask.ext.wtf import (Form, TextField, Required, Length, TextAreaField,
                           ValidationError, regexp)

from app.models.pages import Page

is_url = regexp(r"^[\w.+-]+$",
                     message="You can only use letters, numbers or dashes")


class PageForm(Form):
    title = TextField("Title:", validators=[
        Required(message="A title is required"), Length(min=0, max=140)])
    content = TextAreaField("Content:", validators=[
        Required(message="You can't submit a post without a content")])
    url = TextField("Category:", validators=[
        Required(message="A category is required"), is_url])

    def validate_username(self, field):
        page = Page.query.filter_by(category=field.data).first()
        if page:
            raise ValidationError("The category needs to be unique!")
