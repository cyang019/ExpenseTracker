import os


class Config(object):
  """Base configuration"""
  user = os.environ.get("POSTGRES_USER", None)
  password = os.environ.get("POSTGRES_PASSWORD", None)
  hostname = os.environ.get("POSTGRES_HOSTNAME", None)
  port = os.environ.get("POSTGRES_PORT", None)
  database = os.environ.get("APPLICATION_DB", None)

  SQLALCHEMY_DATABASE_URI = (
      f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
  """Production configuration"""
  pass


class DevelopmentConfig(Config):
  """Development configuration"""
  pass


class TestingConfig(Config):
  """Testing configuration"""
  TESTING = True
