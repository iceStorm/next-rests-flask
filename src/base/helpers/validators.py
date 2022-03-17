from wtforms.validators import Regexp, ValidationError
import re


EmailValidator = Regexp(
    regex='^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',
    message='The email format is invalid'
)


def PasswordValidator(form, field):
    """
    Base password validator for the application.
    @param form:
    @param field:
    """
    if len(field.data) < 6 or len(field.data) > 50:
        raise ValidationError(message='The password must between 6 and 50 characters')
    else:
        password_regex_pattern = '[a-zA-Z0-9]'
        if not re.match(password_regex_pattern, field.data):
            raise ValidationError(message='The password can only contains numbers, letters')


def PhoneNumberValidator(form, field):
    """
    Base phone number validator for the application.
    @param form:
    @param field:
    """
    if len(field.data) < 10 or len(field.data) > 11:
        raise ValidationError(message='The phone number can only between 10 or 11 characters')
    else:
        password_regex_pattern = '[0-9]'
        if not re.match(password_regex_pattern, field.data):
            raise ValidationError(message='The phone number format is invalid')


def CitizenIdValidator(form, field):
    """
    Base citizen id validator for the application.
    @param form:
    @param field:
    """
    if len(field.data) != 10 and len(field.data) != 12:
        raise ValidationError(message='The citizen id can only between 10 or 12 characters')
    else:
        citizen_id_regex_pattern = '(\d{10}|\d{12})'
        if not re.match(citizen_id_regex_pattern, field.data):
            raise ValidationError(message='The citizen id format is invalid')


def TaxIdValidator(form, field):
    """
    Base tax id validator for the application.
    @param form:
    @param field:
    """
    if len(field.data) != 10 and len(field.data) != 14:
        raise ValidationError(message='The tax id can only between 10 or 14 characters')
    else:
        tax_id_regex_pattern = '[0-9]'
        if not re.match(tax_id_regex_pattern, field.data):
            raise ValidationError(message='The tax id format is invalid')


def UrlSlugValidator(form, field):
    """
    Base tax id validator for the application.
    @param form:
    @param field:
    """
    slug_regex_pattern = '^[a-z0-9]+(?:-[a-z0-9]+)*$'
    print('field:', field.data.strip())
    if field.data.strip() != '' and not re.match(slug_regex_pattern, field.data):
        raise ValidationError(message='The slug format is invalid')
