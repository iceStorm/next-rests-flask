import datetime
from flask_sqlalchemy import SQLAlchemy

from src.modules.user.user_model import gen_alternative_id


def start_seeding(db: SQLAlchemy):
    seed_roles(db)
    seed_root_user(db)
    seed_manager_users(db)


def seed_roles(db: SQLAlchemy):
    """
    Seeding roles for the app if there is no roles in the DB.
    """
    from .modules.user.user_model import Role

    # check if there is any Root role user
    root_user = db.session.query(Role).all()

    if len(root_user) == 0:
        print('\nNO ROLES DETECTED, START SEDDING...')

        app_roles = [
            Role(
                name='Quản trị viên',
                code='admin',
            ),
            Role(
                name='Người quản lý',
                code='manager',
            ),
            Role(
                name='Đại sứ',
                code='envoy',
            ),
        ]

        db.session.add_all(app_roles)
        db.session.commit()


def seed_root_user(db: SQLAlchemy):
    """
    Seeding root user for the app if there is no root role user in the DB.
    """
    from .modules.user.user_model import User

    # check if there is any Root role user
    root_user = db.session.query(User)\
        .filter(User.role_id == 1)\
        .first()

    # start sedding if there is no Root role user
    if root_user is None:
        print('\nNO ROOT USER DETECTED, START SEDDING...')

        root_user = User(
            first_name='Anh Tuấn',
            last_name='Nguyễn',
            activated=True,
            email='tuanna@student.bvu.edu.vn',
            phone_number='0333326585',
            raw_password='123456',
        )

        root_user.role_id = 1
        root_user.alternative_id = gen_alternative_id().hex

        db.session.add(root_user)
        db.session.commit()


def seed_manager_users(db: SQLAlchemy):
    """
    Seeding manager user for the app if there is no manager role user in the DB.
    """
    from .modules.user.user_model import User

    # check if there is any Manager role user
    manager_user = db.session.query(User)\
        .filter(User.role_id == 2)\
        .first()

    # start sedding if there is no Root role user
    if manager_user is None:
        print('\nNO MANAGER USER DETECTED, START SEDDING...')

        manager_user_1 = User(
            first_name='Anh Nhân',
            last_name='Nguyễn',
            activated=True,
            email='nhanna@student.bvu.edu.vn',
            phone_number='0033326585',
            raw_password='123456',
        )
        manager_user_1.role_id = 2
        manager_user_1.alternative_id = gen_alternative_id().hex
        manager_user_1.verified_time = datetime.datetime.now()

        manager_user_2 = User(
            first_name='Anh Tú',
            last_name='Lê',
            activated=True,
            email='tula@student.bvu.edu.vn',
            phone_number='0033326586',
            raw_password='123456',
        )
        manager_user_2.role_id = 2
        manager_user_2.alternative_id = gen_alternative_id().hex
        manager_user_2.verified_time = datetime.datetime.now()

        manager_user_3 = User(
            first_name='Anh Tuấn',
            last_name='Hà',
            activated=True,
            email='tuanha@student.bvu.edu.vn',
            phone_number='0033326587',
            raw_password='123456',
        )
        manager_user_3.role_id = 2
        manager_user_3.alternative_id = gen_alternative_id().hex
        manager_user_3.verified_time = datetime.datetime.now()

        db.session.add_all([manager_user_1, manager_user_2, manager_user_3])
        db.session.commit()
