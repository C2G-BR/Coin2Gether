from app.model.social_media_account import SocialMediaAccount
from app.model.social_media_platform import SocialMediaPlatform
from flask import abort

def get_platform_by_name(platform):
    platform = SocialMediaPlatform.query.filter_by(platform_name=platform).first()
    if not platform:
        abort(404, 'Platform Not Found')
    return platform