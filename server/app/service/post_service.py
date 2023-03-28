from .auth_service import get_user_from_token, verify_token, create_token
from app.model.user import User, followers
from app.model.post import Post
from app import db
from .user_service import get_user_by_username
from flask import abort
from sqlalchemy import desc, text

def get_all_posts():
    last_posts = text("SELECT * FROM last_10_posts;")
    with db.engine.connect() as connection:
        result = db.engine.execute(last_posts)
        posts = []
        for row in result:
            post = get_post_by_id(post_id=row[0])
            posts.append(post)
    return posts

def get_followed_posts(token):
    user = get_user_from_token(token)
    return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == user.user_id).order_by(
                    Post.date.desc()).all()
    
def get_post_by_id(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        abort(404, 'Post Not Found')
    else:
        return post

def get_posts_by_username(username):
    user = get_user_by_username(username)
    return Post.query.filter_by(user=user).all()

def new_post(token, data):
    user = get_user_from_token(token)
    title       = data["title"]
    description = data["content"]
    post = Post(title = title, description = description, user = user)
    db.session.add(post)
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully created post'
    }
    return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit(data)