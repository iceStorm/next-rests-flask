from datetime import datetime
from uuid import uuid1, uuid4
from src import db, logger
from src.modules.user.user_model import User, gen_alternative_id
from flask import current_app

class UserService:

    @staticmethod
    def activate(user: User):
        """
        Kích hoạt lại tài khoản đã khóa trước đó.
        """
        try:
            user.activated = True
            db.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False
    

    @staticmethod
    def deactivate(user: User):
        """
        Bỏ kích hoạt lại tài khoản đã khóa trước đó.
        """
        try:
            user.activated = False
            user.alternative_id = gen_alternative_id() # lấy mã mới để loại bỏ các phiên đăng nhập cũ trên các máy client khác
            db.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False
    
    
    @staticmethod
    def verify(user: User):
        """
        Xác thực lần đầu tài khoản đại sứ.
        """
        try:
            user_random_password = ''.join(uuid1().hex.split('-'))[:10]

            user.activated = True
            user.password_hash = user.gen_password_hash(user_random_password)
            user.verified_time = datetime.now()
            db.session.commit()

            UserService.send_register_success_email(
                receiver_email=user.email, 
                receiver_name=user.organization_representer_person_name, 
                password=user_random_password,
            )

            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False


    @staticmethod
    def send_register_success_email(receiver_email: str, receiver_name: str, password: str):
        from flask_mail import Message
        from src import mail
        msg = Message(f'Thông báo xét duyệt tài khoản Đại sứ BVU', sender = current_app.config['MAIL_USERNAME'], recipients = [receiver_email])
        msg.html = f"""
        Xin chào {receiver_name},<br /><br />
        Đây là tin nhắn tự động được gửi từ hệ thống Cổng thông tin Đại sứ BVU.<br/>

        </br/>Tài khoản của bạn đã được chấp thuận, bây giờ bạn có thể đăng nhập vào website thông qua mật khẩu được cung cấp dưới đây:
        <h1>{password}</h1>
        """
        mail.send(msg)
