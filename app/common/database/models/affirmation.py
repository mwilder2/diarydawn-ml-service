from app.extensions import db

class Affirmation(db.Model):
    __tablename__ = 'affirmation'

    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    # Adjusting for camelCase foreign key as defined in the database
    # Make sure to quote the column name to preserve case sensitivity
    pageId = db.Column('pageId', db.BigInteger, db.ForeignKey('page.id', ondelete='CASCADE'), unique=True)
    # The relationship can stay the same in terms of Python code, 
    # but ensure the backref in the Page model matches this.
    page = db.relationship('Page', back_populates='affirmation')


    def __init__(self, content):
        self.content = content
        
    def serialize(self):
        """Converts this entity to a dictionary."""
        return {
            'id': self.id,
            'content': self.content
        }
