from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, TextAreaField


class LoginForm(FlaskForm):
    username = TextField('username')
    password = PasswordField('password')


class PostForm(FlaskForm):
    picture = StringField('IMG URL')
    title = StringField('Title')
    text = TextAreaField('Content')
    description = TextAreaField('Description')
    tags = StringField('Tags')