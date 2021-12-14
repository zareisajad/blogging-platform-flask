import os
import bleach

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Flask application config
    ------------------------
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = os.path.join('app/static/images')

    ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
        'p','h1','h2','h3','h4','h5', 'div',
        'h6','br','img','font'
    ]
    ALLOWED_ATTRIBUTES = {
        '*': ['style', 'id', 'class'],
        'font': ['color'],
        'a': ['href'],
        'img': ['src', 'alt']
    }