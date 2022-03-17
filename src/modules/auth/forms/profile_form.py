from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired
from flask import request
from flask_login import current_user

import re
from src.modules.user.user_model import User
from src.modules.auth.auth_service import AuthService


class UpdateForm(FlaskForm):
    # print('current user email in UpdateForm:', None if not request.method == 'GET' else current_user.get_id())
    print('current user fullname in UpdateForm:', None if not request.method == 'GET' else User.query.get(current_user.get_id()).full_name)

    email = EmailField(
        label='Email',
        render_kw={'disabled': True},
    )

    full_name = StringField(
        label='Full name',
        validators=[
            DataRequired(message='Please fill out this field'),
            Length(min=2, max=50, message='The length must between 2 and 50 letters'),
        ]
    )

    avatar = FileField(
        label='Avatar image',
        render_kw={'accept': 'image/png, image/jpeg'},
        validators=[
            FileAllowed(
                upload_set=['png', 'jpg'],
                message='Only png or jpg image allowed'
            ),
        ]
    )
