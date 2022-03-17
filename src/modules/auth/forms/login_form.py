from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired

import re
from src.modules.user.user_model import User
from src.modules.auth.auth_service import AuthService
from src.base.helpers.validators import *


def IsEmailExists(form, field):
    """
    Checking if the email that client entered is have already exist.
    """
    if not AuthService.is_user_already_exists(field.data):
        raise ValidationError(message='The email is not registered')

def IsAccountActivated(form, field):
    """
    Checking if the email that client entered is activated.
    """
    if not AuthService.is_user_activated(field.data):
        raise ValidationError(message='The account associated with this email is not activated. Please wait or contact for admin confirmation.')


class LoginForm(FlaskForm):
    email = EmailField(
        label='Email',
        description={
            'icon': {
                'origin': 'icons/fluent/outline/mail.svg',
            },
        },
        render_kw={
            'autocomplete': 'email',
        },
        validators=[
            DataRequired(),
            EmailValidator,
            IsEmailExists,
            IsAccountActivated,
        ]
    )

    password = PasswordField(
        label='Mật khẩu',
        render_kw={'autocomplete': 'current-password'},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/lock-closed.svg',
                'alternate': 'icons/fluent/outline/lock-open.svg',
            },
        },
        validators=[
            InputRequired(message='Please fill out this field'),
            PasswordValidator,
        ]
    )

    remember = BooleanField(
        label='Remember',
    )


    # overriding the validate function
    def validate(self):
        # first, validate the above requirements by: passing this instance to the FlaskForm.validate()
        if not FlaskForm.validate(self):
            return False

        # checking if the provided password is not True (with the one in the database)
        # the user instance below is always exists because the form's email validation did check.
        user = AuthService.get_user_from_email(self.email.data)
        # print(user)

        if not user.check_password(self.password.data):
            self.password.errors.append('The password you just provided was wrong')
            return False

        return True
