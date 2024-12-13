from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Dream(db.Model):
    __tablename__ = 'dream'

    id = db.Column(db.BigInteger, primary_key=True)
    symbols = db.Column(ARRAY(db.String), nullable=True)  # Stores an array of strings

    # Adjusting for camelCase foreign key as defined in the database
    # Make sure to quote the column name to preserve case sensitivity
    pageId = db.Column('pageId', db.BigInteger, db.ForeignKey('page.id', ondelete='CASCADE'), unique=True)
    # The relationship can stay the same in terms of Python code, 
    # but ensure the backref in the Page model matches this.
    page = db.relationship('Page', back_populates='dream')

    def __init__(self, symbols=None):
        self.symbols = symbols if symbols is not None else []
        
    def serialize(self):
        """Converts this entity to a dictionary."""
        return {
            'id': self.id,
            'symbols': self.symbols
        }
