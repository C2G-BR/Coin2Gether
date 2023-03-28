from sqlalchemy import desc, Index
from app import db
from datetime import datetime
from .user import User

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.today())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
Index('post_date_idx', Post.date.desc())