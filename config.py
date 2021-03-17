import os


class Config(object):
    """
    Used to setup flask. Necessary file
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
