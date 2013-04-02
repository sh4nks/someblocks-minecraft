from flask.ext.wtf import (Form, TextField, Required, Length, TextAreaField,
                           ValidationError, regexp, BooleanField, IntegerField,
                           url)
from app.models.pages import Page


class PageForm(Form):
    title = TextField("Title", validators=[
        Required(message="A title is required"), Length(min=0, max=140)])
    content = TextAreaField("Content")
    position = IntegerField("Page Position", default=1)


class NewPageForm(PageForm):
    external = BooleanField("External Link", default=False)
    url = TextField("URL", validators=[Required(message="A URL is required")])


    def validate_url(self, field):
        page = Page.query.filter_by(url=field.data).first()
        if page:
            raise ValidationError("The URL needs to be unique!")
