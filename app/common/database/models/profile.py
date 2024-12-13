from app.extensions import db
from sqlalchemy.dialects.postgresql import JSON

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    pictureUrl = db.Column('pictureUrl', db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    interests = db.Column(db.ARRAY(db.String), nullable=True)  # Requires PostgreSQL
    website = db.Column(db.String(255), nullable=True)
    socialLinks = db.Column('socialLinks', JSON, nullable=True)  # Stores an object as JSON
    joinedAt = db.Column('joinedAt', db.DateTime, default=db.func.current_timestamp())
    lastActive = db.Column('lastActive', db.DateTime, nullable=True)
    theme = db.Column(db.String(255), nullable=True)

    # Relationship - Adjusting for camelCase foreign key as defined in the database
    userId = db.Column('userId', db.BigInteger, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='profile')

    def __init__(self, name, bio=None, birthdate=None, pictureUrl=None, location=None, interests=None, website=None, socialLinks=None, theme=None):
        self.name = name
        self.bio = bio
        self.birthdate = birthdate
        self.pictureUrl = pictureUrl
        self.location = location
        self.interests = interests
        self.website = website
        self.socialLinks = socialLinks
        self.theme = theme
