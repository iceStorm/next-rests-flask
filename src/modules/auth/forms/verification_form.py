from flask_wtf.form import FlaskForm
from wtforms.fields.core import RadioField, StringField
from wtforms.validators import InputRequired, Length


class RegisterVerificationForm(FlaskForm):
  verification_code = StringField(
    render_kw={ 'min': 6, 'max': 6 },
    filters=[
      lambda string: string.strip() if string else '',
    ],
    validators=[
        InputRequired(),
        Length(min=6, max=6),
    ],
  )
