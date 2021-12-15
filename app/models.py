from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='posts')
    profile = db.relationship('Profile', backref='profile', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(200), default='images/default.png')
    fname = db.Column(db.String(120))
    lname = db.Column(db.String(120))
    about = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    title = db.Column(db.String(300))
    tags = db.Column(db.String(600))
    content = db.Column(db.String(800))
    author = db.relationship('User', backref='author',overlaps="posts")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

    def __repr__(self):
        return '{}'.format(self.title)