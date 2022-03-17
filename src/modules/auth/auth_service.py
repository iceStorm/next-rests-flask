import os, uuid
import bcrypt

from flask import current_app, session
from itsdangerous import URLSafeTimedSerializer
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from src import db, logger, db_session
from src.modules.user.user_model import User
from src.modules.auth.forms.signup_form import SignUpForm


class AuthService:
    @staticmethod
    def get_user_from_email(email: str):
        return db_session.query(User).filter_by(email = email).first()

    def get_user_from_username(username: str):
        return db_session.query(User).filter_by(username = username).first()

    @staticmethod
    def is_user_already_exists(email):
        print(f'Checking user exists on the system: {email}');
        print(db_session.query(User).filter_by(email = email).first())
        return db_session.query(User).filter_by(email = email).first() is not None

    @staticmethod
    def is_user_activated(email):
        print(f'Checking user account activated on the system: {email}');
        return db_session.query(User).filter(User.email == email, User.activated == True).first() is not None

    @staticmethod
    def get_verify_tọken(expiration):
        s = URLSafeTimedSerializer(
            secret_key=current_app.config['SECRET_KEY'],
        )
        pass

    @staticmethod
    def register(new_user: User):
        try:
            db_session.add(new_user)
            db_session.commit()
            return new_user
        except Exception as e:
            logger.error(e)
            db_session.rollback()
            return None


    @staticmethod
    def send_register_confirm_email(receiver_email: str, receiver_name: str, code: str):
        from flask_mail import Message
        from src import mail
        msg = Message(f'Xác minh đăng ký tài khoản Đại sứ BVU', sender = current_app.config['MAIL_USERNAME'], recipients = [receiver_email])
        msg.html = f"""
        Xin chào {receiver_name},<br /><br />
        Đây là tin nhắn tự động được gửi từ hệ thống Cổng thông tin Đại sứ BVU.<br/>
        Vui lòng sao chép mã sau đây để hoàn tất quá trình đăng ký:
        <h1>{code}</h1>
        """
        mail.send(msg)
    

    @staticmethod
    async def send_reset_password_email(email: str, password: str) -> None:
        from flask_mail import Message
        from src import mail
        msg = Message(f'Khôi phục mật khẩu Đại sứ BVU', sender = current_app.config['MAIL_USERNAME'], recipients = [email])
        msg.html = f"""
        Xin chào {email},<br /><br />
        Đây là tin nhắn tự động được gửi từ hệ thống Cổng thông tin Đại sứ BVU.<br/>
        Sau đây là mật khẩu mới của bạn để đăng nhập:
        <h1>{password}</h1>
        """
        await mail.send(msg)


    @staticmethod
    def gen_registration_code() -> str:
        """
        Generating envoy registration code to send to email.
        """
        # getting 6 letters code
        code = ''.join(uuid.uuid1().hex.split('-'))[:6]
        return code
