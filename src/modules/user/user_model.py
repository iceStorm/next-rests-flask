from datetime import datetime
from uuid import uuid1, uuid4
import bcrypt
from sqlalchemy.orm import relationship
from flask import request
from flask_login import UserMixin, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey

# from werkzeug.security import generate_password_hash, check_password_hash

from .user_constants import *

from src import db, db_session


def gen_alternative_id():
    return uuid1().hex


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}

    # BASE USER FIELDS ----------------------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)

    # id sử dụng cho việc đăng nhập | admin có thể thay đổi id này để chặn các phiên đăng nhập cũ
    # (đổi mật khẩu trên một máy client thì cần chặn các máy client khác | deactivate..)
    alternative_id = Column(String(), unique=True, nullable=False)

    email = Column(String(USER_EMAIL_LENGTH), nullable=False, unique=True, index=True)
    phone_number = Column(String(USER_PHONE_LENGTH), nullable=False, unique=True, index=True)
    first_name = Column(String(USER_FIRST_NAME_LENGTH), index=True)
    last_name = Column(String(USER_LAST_NAME_LENGTH), index=True)
    password_hash = Column(String(USER_PASSWORD_LENGTH))
    avatar_url = Column(String(USER_AVATAR_URL_LENGTH))
    username = Column(String(USER_USERNAME_LENGTH), index=True, unique=True)
    activated = Column(Boolean, nullable=False, default=False)
    created_time = Column(DateTime, nullable=False, default=datetime.now())
    verified_time = Column(DateTime) # thời gian chấp nhận tài khoản được đăng ký

    # roleId:3 == Envoy
    role_id = Column(Integer, ForeignKey('Role.id'), nullable=False, default=3)
    role = relationship('Role', backref='users')

    def __init__(self, email: str, phone_number: str, 
        first_name: str=None, last_name: str=None, 
        raw_password=None, avatar_url=None, 
        activated=False, role_id=3):
        """
        Creating a new User instance.
        raw_password: this field will be encrypted automatically.
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.avatar_url = avatar_url
        self.phone_number = phone_number
        self.activated = activated
        self.avatar_url = avatar_url
        self.role_id = 3 # default user is envoy to restrict permissions

        # if raw_password provided through the constructor
        if raw_password:
            self.password_hash = User.gen_password_hash(raw_password)
            print(f'hashing the password {raw_password}:', self.password_hash)

    def get_id(self):
        """
        Overriding the get_id to return id - that we used at the primary key. Use for flask-login.
        Below using alternative_id for prevent old user sessions.
        """
        return self.alternative_id
    

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"<User: full name: {self.full_name}, email: {self.email}>"

    @staticmethod
    def gen_password_hash(raw_password):
        # return generate_password_hash(raw_password)
        return Bcrypt().generate_password_hash(raw_password)

    def check_password(self, raw_password: str):
        """
        Checking if the raw_password matches the password of this User instance.
        """
        # return check_password_hash(self.password_hash, raw_password)
        return Bcrypt().check_password_hash(self.password_hash, raw_password) if self.password_hash is not None else None

    @staticmethod
    def is_email_already_exists(email: str) -> bool:
        """
        Checking if any email in DB matchs :email.
        """
        return db.session.query(User).filter(User.email == email).first() is not None

    @staticmethod
    def is_phone_already_exists(phone: str) -> bool:
        """
        Checking if any phone in DB matchs :phone.
        """
        return db.session.query(User).filter(User.phone_number == phone).first() is not None
    
    @staticmethod
    def is_address_already_exists(address: str) -> bool:
        """
        Checking if any address in DB matchs :address.
        """
        return db.session.query(User).filter(User.address == address).first() is not None

    @staticmethod
    def is_citizen_id_already_exists(citizen_id: str) -> bool:
        """
        Checking if any citizen_id in DB matchs :citizen_id.
        """
        return db.session.query(User).filter(User.citizen_id == citizen_id).first() is not None

    @staticmethod
    def is_organization_name_already_exists(name: str) -> bool:
        """
        Checking if any organization_name in DB matchs :name.
        """
        return db.session.query(User).filter(User.organization_name == name).first() is not None

    @staticmethod
    def is_organization_representer_name_already_exists(name: str) -> bool:
        """
        Checking if any organization_representer_person_name in DB matchs :name.
        """
        return db.session.query(User).filter(User.organization_representer_person_name == name).first() is not None

    @staticmethod
    def is_organization_taxid_already_exists(tax_id: str) -> bool:
        """
        Checking if any organization_tax_id in DB matchs :tax_id.
        """
        return db.session.query(User).filter(User.organization_tax_id == tax_id).first() is not None

    @staticmethod
    def is_organization_email_already_exists(tax_id: str) -> bool:
        """
        Checking if any organization_tax_id in DB matchs :tax_id.
        """
        return db.session.query(User).filter(User.organization_tax_id == tax_id).first() is not None


class Role(db.Model):
    __tablename__ = 'Role'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(USER_ROLE_LENGTH), nullable=False, unique=True, index=True)
    code = Column(String(USER_ROLE_LENGTH), nullable=False, unique=True, index=True)
