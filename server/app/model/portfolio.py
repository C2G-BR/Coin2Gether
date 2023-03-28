from app import db
from sqlalchemy.ext.associationproxy import association_proxy

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    name = db.Column(db.String(50), default='default', primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    components = association_proxy('components', 'currency')