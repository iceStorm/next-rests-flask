from flask import Flask
import os
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, Identity, AnonymousIdentity, identity_loaded, UserNeed, RoleNeed
from flask_mail import Mail


class App(Flask):
    def __init__(self):
        super(App, self).__init__(import_name=__name__)


    def load_environment_variables(self):
        """
        Loading the configured environment variables.
        """
        from dotenv import load_dotenv
        load_dotenv()  # take environment variables from .env file.
        print('/n', os.environ)

        # USING DEFAULT CONFIG
        from .config import DefaultEnvironment
        self.config.from_object(DefaultEnvironment)

        # LOAD/OVERRIDE DEVELOPER SPECIFIED ENV
        environment_configuration = os.environ.get('CONFIG_FILE')
        assert environment_configuration is not None, "Please provide the CONFIG_FILE env"
        self.config.from_object(environment_configuration)

        print('\n', self.config, '\n\n')


    def register_logger(self):
        import logging
        from logging.handlers import SMTPHandler

        if not self.debug:
            if self.config['MAIL_SERVER']:
                auth = None
                if self.config['MAIL_USERNAME'] or self.config['MAIL_PASSWORD']:
                    auth = (self.config['MAIL_USERNAME'], self.config['MAIL_PASSWORD'])

                secure = None
                if self.config['MAIL_USE_TLS']:
                    secure = ()

                mail_handler = SMTPHandler(
                    mailhost=(self.config['MAIL_SERVER'], self.config['MAIL_PORT']),
                    fromaddr=self.config['MAIL_SERVER'],
                    toaddrs=self.config['MAIL_SERVER'], subject='BVU Envoy Failure',
                    credentials=auth, secure=secure
                )

                mail_handler.setLevel(logging.ERROR)
                self.logger.addHandler(mail_handler)


    def register_global_functions(self):
        """
        Registering jinja global functions (allow calling from any jinja templates)
        """
        from .base.helpers.jinja_env_functions import extract_avatar_url, get_svg_content, server_name
        self.jinja_env.globals.update(extract_avatar_url=extract_avatar_url)
        self.jinja_env.globals.update(get_svg_content=get_svg_content)
        self.jinja_env.globals.update(server_name=server_name)


    def register_blueprints(self):
        """
        Registering the app's blueprints.
        """
        # PORTAL subdomain
        from .modules.auth.auth_controller import auth
        from .modules.user.user_controller import user
        self.register_blueprint(auth, url_prefix="/")
        self.register_blueprint(user, url_prefix="/users")


    def register_cors(self):
        """Adding CORS origins (all) for client ajax calling."""
        from flask_cors import CORS
        cors = CORS(app=self, resources={r"/*": {"origins": "*"}})


    def register_error_handlers(self):
        """
        Registering custom error handlers that show custom view (html page) for the src.
        """
        from .base.helpers.error_handlers import ErrorHandler

        self.register_error_handler(403, ErrorHandler.forbidden)
        self.register_error_handler(404, ErrorHandler.not_found)
        self.register_error_handler(429, ErrorHandler.too_many_requests)
        self.register_error_handler(500, ErrorHandler.server_error)


    def register_login_manager(self):
        """Adding login manager for the application."""
        from flask_login import LoginManager

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(self)

        """This sets the callback for reloading a user from the session.
        The function you set should take a user ID (a unicode) and return a user object, or None if the user does not exist."""
        @login_manager.user_loader
        def load_user(id):
            from .modules.user.user_model import User, db
            return db.session.query(User).filter(User.alternative_id == id).first()


    ### INIT FUNCTIONS ###
    def init_mail(self, mail: Mail):
        mail.init_app(self)
        self.mail = mail


    def init_db(self, db: SQLAlchemy):
        """
        Initializing DB connnection.
        Migrating models to DB schema/tables.
        Seeding initial data.
        """
        db.init_app(app=self)
        self.db = db

        # MIGRATING MODELS TO DB SCHEMAS
        if self.config["FLASK_ENV"] == "development":
            from flask_migrate import Migrate
            print("\n\n[MIGRATING THE DATABASE...]")
            migrate = Migrate()
            with self.app_context():
                db.create_all()

                # allow dropping column for sqlite
                if db.engine.url.drivername == 'sqlite':
                    migrate.init_app(self, db, render_as_batch=True)
                else:
                    migrate.init_app(self, db)

            # IMPORTING MODELS IS NEEDED FOR FLASK-MIGRATE TO DETECT CHANGES
            # ...
    

    def init_protections(self, limiter: Limiter, principals: Principal):
        """
        Initializing application's protection/security extensions.
        """
        limiter.init_app(self)
        self.limiter = limiter

        principals.init_app(self)
        self.principals = principals
        self.init_principal_user_provider()


    def init_principal_user_provider(self):
        @self.principals.identity_loader
        def read_identity_from_flask_login():
            from flask_login import current_user

            if current_user.is_authenticated and current_user.activated:
                return Identity(current_user.id)

            # user not logged in
            return AnonymousIdentity()

        @identity_loaded.connect_via(self)
        def on_identity_loaded(sender, identity):
            from flask_login import current_user

            # ensure the logged-in user is activated
            if hasattr(current_user, 'activated') and current_user.activated:
                # Set the identity user object
                identity.user = current_user

                # Add the UserNeed to the identity
                if hasattr(current_user, 'id'):
                    identity.provides.add(UserNeed(current_user.id))

                # Add the RoleNeed to the identity
                if hasattr(current_user, 'role'):
                    identity.provides.add(RoleNeed(current_user.role.code))

    def start_seeding(self):
        """Start seeding initial data"""
        with self.app_context():
            from .seeding import start_seeding
            start_seeding(self.db)
