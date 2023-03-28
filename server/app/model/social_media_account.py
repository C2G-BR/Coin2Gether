from app import db

class SocialMediaAccount(db.Model):
    __tablename__ = 'social_media_accounts'
    platform_id = db.Column(db.Integer, db.ForeignKey('social_media_platforms.platform_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    
    user = db.relationship("User", back_populates="accounts")
    platform = db.relationship("SocialMediaPlatform", back_populates="users")

    username = db.Column(db.String, nullable=False)