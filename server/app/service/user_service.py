from flask import abort
from sqlalchemy import func, text
from .auth_service import get_user_from_token, verify_token, create_token
from .social_media_service import get_platform_by_name
from app.model.user import User
from app.model.social_media_account import SocialMediaAccount
from app.model.social_media_platform import SocialMediaPlatform
from app import bcrypt, db
import dateutil.parser


def get_user_by_id(user_id: int):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        abort(404, 'User Not Found')
    else:
        return user

def get_all_usernames():
    users = User.query.with_entities(User.username).all()
    user_list = []
    for a in users:
        for b in a:
            user_list.append(b)
    return user_list

def get_all_users():
    users = User.query.all()
    return users

def get_user_by_username(username):
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if user == None:
        abort(400, 'User not found')
    return user

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user == None:
        abort(400, 'User not found')
    return user

def follow(token, username):
    user1 = get_user_from_token(token)
    user2 = get_user_by_username(username)
    if user1 is None or user2 is None:
        abort(400, 'User does not exist')
    if user1.is_following(user2):
        abort(400, 'User already following this user')
    # user1.followed.append(user2)
    # db.session.commit()
    connection = db.engine.connect()
    conn = connection.begin()
    statement = text(f"CALL new_follow({user1.user_id}, {user2.user_id});")
    try:
        connection.execute(statement)
        conn.commit()
    except:
        abort(400, 'Error with insert: Follow')
    response_object = {
        'status': 'success',
        'message': 'Successfully followed'
    }
    return response_object, 201

def unfollow(token, username):
    user1 = get_user_from_token(token)
    user2 = get_user_by_username(username)
    if user1 is None or user2 is None:
        abort(400, 'User does not exist')
    if not user1.is_following(user2):
        abort(400, 'User not following this user')
    # user1.followed.remove(user2)
    # db.session.commit()
    connection = db.engine.connect()
    conn = connection.begin()
    statement = text(f"CALL delete_follow({user1.user_id}, {user2.user_id});")
    try:
        connection.execute(statement)
        conn.commit()
    except:
        abort(400, 'Error with insert: Unfollow')
    response_object = {
        'status': 'success',
        'message': 'Successfully unfollowed'
    }
    return response_object, 201

def register(username, email, lastName, firstName, password, birthdate, socialMediaProfiles=None):

    birthdate = dateutil.parser.parse(birthdate)

    if User.query.filter_by(username=username).first() != None or User.query.filter_by(email=email).first() != None:
        abort(400, 'User already exist')
    
    hashed_password = bcrypt.generate_password_hash(password, 10)
    user = User(username=username, email=email, lastName=lastName, firstName=firstName, birthdate=birthdate, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    if socialMediaProfiles is not None:
        for profile in socialMediaProfiles:
            
            platform, account_username = profile["socialMediaPlatform"], profile["username"]
            account = SocialMediaAccount(username=account_username)
            account.platform = get_platform_by_name(platform)
            account.user = user
            user.accounts.append(account)
            db.session.add(account)
            db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully created'
    }
    return response_object, 201

def login(email, password):
    user = get_user_by_email(email)
    password_matched_email = user.password
    if not bcrypt.check_password_hash(password_matched_email, password):
        abort(400, 'Wrong credentials')
    token = create_token(email)
    return token, user.username

def update_user(token, firstName, lastName, birthdate, socialMediaProfiles=None):
    user = get_user_from_token(token)

    birthdate = dateutil.parser.parse(birthdate)
    SocialMediaAccount.query.filter_by(user=user).delete()  
    user.firstName = firstName
    user.lastName = lastName
    user.birthdate = birthdate
    db.session.commit()
    if socialMediaProfiles is not None:
        for profile in socialMediaProfiles:
            
            platform, account_username = profile["socialMediaPlatform"], profile["username"]
            account = SocialMediaAccount(username=account_username)
            account.platform = get_platform_by_name(platform)
            account.user = user
            user.accounts.append(account)
            db.session.add(account)
            db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully updated'
    }
    return response_object, 201