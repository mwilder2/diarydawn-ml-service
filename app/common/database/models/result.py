from app.extensions import db

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.BigInteger, primary_key=True)
    # Adjusting for camelCase foreign key as defined in the database
    bookId = db.Column('bookId', db.BigInteger, db.ForeignKey('book.id', ondelete='CASCADE'))
    modelName = db.Column('modelName', db.String(120), nullable=False)
    traitName = db.Column('traitName', db.String(120), nullable=False)
    traitValue = db.Column('traitValue', db.String(120), nullable=False)
    # Additional information column (optional), can be used to store confidence scores, etc., as JSON
    additionalInfo = db.Column('additionalInfo', db.JSON, nullable=True)

    book = db.relationship('Book', back_populates='result')

    def __init__(self, bookId, modelName, traitName, traitValue, additionalInfo=None):
        self.bookId = bookId
        self.modelName = modelName
        self.traitName = traitName
        self.traitValue = traitValue
        self.additionalInfo = additionalInfo
