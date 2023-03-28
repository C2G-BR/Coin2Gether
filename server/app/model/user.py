from app import db
from sqlalchemy import desc, Index
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.user_id'))
) # User_follower_id folgt user_followed_id

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    lastName = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.today()) 
    trades = association_proxy('trades', ['debit_currency', 'credit_currency'])
    portfolio = db.relationship('Portfolio', uselist=False, foreign_keys='Portfolio.user_id', cascade='all, delete-orphan', backref=db.backref('users', lazy=True), lazy=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    accounts = db.relationship("SocialMediaAccount", back_populates="user")

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == user_id),
        secondaryjoin=(followers.c.followed_id == user_id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def is_following(self, user2):
        return self.followed.filter(
            followers.c.followed_id == user2.user_id).count() > 0
Index('user_username_idx', User.username.desc())