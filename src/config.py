import os

class DefaultEnvironment(object):
  """
  Defining application configuration variables.
  """

  # site meta
  APP_NAME = "Cổng thông tin Đại Sứ BVU"
  FLASK_ENV=os.environ["FLASK_ENV"]
  FLASK_APP=os.environ["FLASK_APP"]


  # application running stage
  DEBUG = False
  TESTING = False

  # database
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

  # flask login/authentication/protection
  SESSION_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  CSRF_ENABLED = True
  SECRET_KEY = os.environ["SECRET_KEY"]
  RBAC_USE_WHITE = True
  RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'

  # recaptcha
  RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
  RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]

  # mail
  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 465
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.environ["MAIL_USERNAME"]
  MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]


class DevelopmentEnvironment(DefaultEnvironment):
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  DEBUG = True


class ProductionEnvironment(DefaultEnvironment):
  PREFERRED_URL_SCHEME = 'https'
