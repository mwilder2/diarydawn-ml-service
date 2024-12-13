from app.extensions import db

class Limitless(db.Model):
    __tablename__ = 'limitless'

    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    # One-to-One relationship with Page
    pageId = db.Column('pageId', db.BigInteger, db.ForeignKey('page.id', ondelete='CASCADE'), unique=True)
    page = db.relationship('Page', back_populates='limitless')

    def __init__(self, content):
        self.content = content

    def serialize(self):
        """Converts this entity to a dictionary."""
        return {
            'id': self.id,
            'content': self.content
        }
