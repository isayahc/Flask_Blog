"""Data models."""
from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db, login_manager

from datetime import datetime


class User(db.Model, UserMixin):
    '''username, pw_has'''
    __tablename__ = "users"
    id_ = db.Column(
        db.Integer,
        primary_key=True
        )

    name = db.Column(
        db.String(80),
        nullable=False
        )

    email = db.Column(
        db.String(80),
        nullable=False,
        unique=True
        )

    profile_pic = db.Column(
        db.String(180),
        nullable=False,
        unique=True,
        index=False
        )

    user_source = db.Column(
        db.String(180),
        nullable=False,
        unique=True,
        index=False
        )

    post = db.relationship('Post', backref='author', lazy=True)
    

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def get(email: str):
        user = User.query.filter_by(email=email).first()
        return user

    @staticmethod
    def create(name, email, profile_pic, user_source):
        user = User(name=name, email=email, profile_pic=profile_pic, user_source=user_source)
        db.session.add(user)
        db.session.commit()

    def get_id(self):
        return (self.id_)

    def is_authenticated(self):
        return True

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(user_id)
        except:
            return None

class Post(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id_'), nullable=False)

    def __repr__(self):
        return f"<Post ('{self.title},{self.date_posted}')>"

