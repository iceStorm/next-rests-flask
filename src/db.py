from sqlalchemy.orm.scoping import scoped_session
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def get_db_session() -> scoped_session:
    return db.session


db_session = get_db_session()
