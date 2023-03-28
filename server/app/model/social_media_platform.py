from app import db

class SocialMediaPlatform(db.Model):
    __tablename__ = 'social_media_platforms'
    platform_id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String, nullable=False)
    platform_specific_link = db.Column(db.String, nullable=False)

    users = db.relationship("SocialMediaAccount", back_populates="platform")

