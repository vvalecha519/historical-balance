import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*G-KaPdSgVkYp3s6v9y$B&E)H+MbQeTh'
