from app.extensions import db

class Page(db.Model):
    __tablename__ = 'page'

    id = db.Column(db.BigInteger, primary_key=True)
    entry_type = db.Column('entryType', db.String(120), default='limitless', nullable=False) # 'limitless', 'affirmation', 'gratitude', 'emotion', 'dream', 'lesson', 'journey
    page_number = db.Column('pageNumber', db.Integer, default=0, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    title = db.Column(db.String(120), default='', nullable=True)
    emotion_name = db.Column('emotionName', db.String(120), default='', nullable=True)
    emotion_value = db.Column('emotionValue', db.Integer, default=0, nullable=True)
    updated_at = db.Column('updatedAt', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_at = db.Column('createdAt', db.DateTime, default=db.func.current_timestamp())

    # Relationship with Book
    book_id = db.Column('bookId', db.BigInteger, db.ForeignKey('book.id', ondelete='CASCADE'))
    book = db.relationship('Book', back_populates='pages')

    # one-to-one relationships with diary entry types
    limitless = db.relationship('Limitless', back_populates='page', cascade='all, delete-orphan', uselist=False)
    affirmation = db.relationship('Affirmation', back_populates='page', cascade='all, delete-orphan', uselist=False)
    gratitude = db.relationship('Gratitude', back_populates='page', cascade='all, delete-orphan', uselist=False)
    emotion = db.relationship('Emotion', back_populates='page', cascade='all, delete-orphan', uselist=False)
    dream = db.relationship('Dream', back_populates='page', cascade='all, delete-orphan', uselist=False)
    lesson = db.relationship('Lesson', back_populates='page', cascade='all, delete-orphan', uselist=False)
    journey = db.relationship('Journey', back_populates='page', cascade='all, delete-orphan', uselist=False)

    def __init__(self, entry_type, page_number, title='', emotion_name='', emotion_value=0):
        self.entry_type = entry_type
        self.page_number = page_number
        self.title = title
        self.emotion_name = emotion_name
        self.emotion_value = emotion_value

# book = db.relationship('Book', backref=db.backref('pages', lazy=True))
# journey = db.relationship('Journey', back_populates='page', uselist=False, cascade='all, delete-orphan', single_parent=True, foreign_keys=[journey_id])