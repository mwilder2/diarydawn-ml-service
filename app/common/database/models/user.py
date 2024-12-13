from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    createdAt = db.Column('createdAt', db.DateTime, default=db.func.current_timestamp())
    updatedAt = db.Column('updatedAt', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    books = db.relationship('Book', back_populates='user', lazy=True, cascade='all, delete-orphan')
    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')

    def __init__(self, email, password):
        self.email = email
        self.password = password
