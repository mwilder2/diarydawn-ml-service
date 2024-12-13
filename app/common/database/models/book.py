from app.extensions import db

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.BigInteger, primary_key=True)
    # Adjusting for camelCase foreign key as defined in the database
    userId = db.Column('userId', db.BigInteger, db.ForeignKey('user.id', ondelete='CASCADE'))
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)
    createdAt = db.Column('createdAt', db.DateTime, default=db.func.current_timestamp())
    updatedAt = db.Column('updatedAt', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    # Ensure the back_populates arguments in related models (User, Page, Result) match these relationship names
    user = db.relationship('User', back_populates='books')
    pages = db.relationship('Page', back_populates='book', lazy=True, cascade='all, delete-orphan')
    result = db.relationship('Result', back_populates='book', uselist=False)

    def __init__(self, userId, title, description=None):
        self.userId = userId
        self.title = title
        self.description = description

    # user = db.relationship('User', backref=db.backref('books', lazy=True))
    # pages = db.relationship('Page', backref='book', lazy=True, cascade='all, delete-orphan', passive_deletes=True)

