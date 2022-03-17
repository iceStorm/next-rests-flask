from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey

from src import db
from .setting_constants import *


class EmailTemplates(db.Model):
  __tablename__ = 'EmailTemplates'
  __table_args__ = {'extend_existing': True}

  id = db.Column(Integer, primary_key=True)
  name = db.Column(String(SETTING_EMAIL_TEMPLATE_NAME_LENGTH), nullable=False, unique=True, index=True)
  content = db.Column(String(SETTING_EMAIL_TEMPLATE_CONTENT_LENGTH), nullable=False, unique=True)
