from flask_wtf import FlaskForm, RecaptchaField

from wtforms.fields import StringField, PasswordField, IntegerField, RadioField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired, Optional

from src.modules.user.user_constants import *
from src.base.helpers.validators import *


def IsEmailExists(form, field):
    from src.modules.user.user_model import User, db
    if db.session.query(User).filter(User.email == field.data).first() is not None:
        raise ValidationError(message='The email is already registered')


class SignUpForm(FlaskForm):
    email = EmailField(
        label='Email',
        render_kw={'autocomplete': 'email', 'maxlength': USER_EMAIL_LENGTH, },

        filters=[
            # discarding all redundant spaces
            lambda string: str(string).strip() if string else '',
        ],
        validators=[
            InputRequired(),
            EmailValidator,
        ]
    )

    phone = StringField(
        label='Số điện thoại',
        render_kw={'autocomplete': 'tel', 'maxlength': USER_PHONE_LENGTH, },
        description={
            'icon': {
                'origin': 'icons/fluent/outline/number.svg',
            },
            'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
        filters=[
            # discarding all redundant spaces
            lambda string: str(string).strip() if string else '',
        ],
        validators=[
            InputRequired(),
            PhoneNumberValidator,
        ]
    )


    def validate(self):
        # first, validate the above requirements by: passing this instance to the FlaskForm.validate()
        # ensure all fields are filled
        if not FlaskForm.validate(self):
            return False

        form_passed = True
        from src.modules.user.user_model import User

        if User.is_email_already_exists(self.email.data):
            self.email.errors.append('This email already exists')
            form_passed = False

        if User.is_phone_already_exists(self.phone.data):
            self.phone.errors.append('This phone number already exists')
            form_passed = False

        if User.is_address_already_exists(self.address.data):
            self.address.errors.append('This address already exists')
            form_passed = False

        # awalys return True
        return form_passed
