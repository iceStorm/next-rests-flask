from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, ValidationError, Optional

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


class ResetPasswordForm(FlaskForm):
  email = EmailField(
    label="Email cần khôi phục mật khẩu",
    validators=[
      InputRequired(),
      EmailValidator,
      Optional(),
      IsEmailExists,
      Optional(),
      IsAccountActivated,
    ],
    description={
      "icon":{
        "origin": "icons/fluent/outline/mail.svg",
      }
    },
    render_kw={
        'autocomplete': 'email',
    },
  )
