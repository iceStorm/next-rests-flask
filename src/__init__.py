"""
Entrypoint of the application.
"""

from .App import App

from flask_mail import Mail
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter


# INIT LOGGER
import logging as logger
logger.basicConfig(format='%(asctime)s - %(message)s', level=logger.INFO,)

# INIT DATABASE
print("\n[DEFINING DATABASE INSTANCE...]")
from .db import *

# INIT PRINCIPALS
from .permissions import *

# INIT RATE LIMITING
print("\n[DEFINING RATE LIMITING INSTANCE...]")
limiter = Limiter(key_func=get_remote_address)

# INIT MAIL
mail = Mail()


def create_app():
    """
    Initializing the App and plug-in extensions.
    Return a runnable Flask application.
    """
    print("\n[INITIALIZING THE APP...]")
    app = App()

    # loading environment variables
    app.load_environment_variables()

    # registering essential partials for the app
    app.register_logger()
    app.register_global_functions()
    app.register_blueprints()
    app.register_cors()
    # app.register_error_handlers()
    app.register_login_manager()

    app.init_db(db=db)
    app.start_seeding()

    app.init_protections(limiter=limiter, principals=principals)
    app.init_mail(mail=mail)

    print('\n\n[NEW APP RETURNED...]')
    return app
