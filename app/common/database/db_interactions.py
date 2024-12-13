
from flask import abort
from sqlalchemy.orm import joinedload
from app.common.database.models.affirmation import Affirmation
from app.common.database.models.book import Book
from app.common.database.models.dream import Dream
from app.common.database.models.emotion import Emotion
from app.common.database.models.gratitude import Gratitude
from app.common.database.models.journey import Journey
from app.common.database.models.lesson import Lesson
from app.common.database.models.limitless import Limitless
from app.common.database.models.page import Page
from app.common.database.models.result import Result
from app.extensions import db


def get_pages_and_entry_types_by_book_and_user(book_id, user_id):
    # Fetch the book along with its pages in a single query using joinedload
    book = Book.query.options(joinedload(Book.pages)).filter_by(id=book_id, userId=user_id).first()

    if not book:
        # Handle the case where the book is not found
        print(f"Book #{book_id} not found or does not belong to the user #{user_id}")
        return []

    pages_data = []
    for page in book.pages:
        # Base page data
        page_data = {
            'id': page.id,
            'entry_type': page.entry_type,
            'page_number': page.page_number,
            'date': page.date.isoformat(),
            'title': page.title,
            'emotion_name': page.emotion_name,
            'emotion_value': page.emotion_value
        }

        # Dynamically load entry type data based on the type of entry
        entry_type_model = determine_entry_type_model(page.entry_type)
        if entry_type_model:
            entry_type_instance = db.session.query(entry_type_model).filter_by(pageId=page.id).first()
            if entry_type_instance:
                page_data['entry_type_data'] = entry_type_instance.serialize()

        pages_data.append(page_data)

    return pages_data

def determine_entry_type_model(entry_type):
    """Maps the entry type to its corresponding SQLAlchemy model."""
    entry_type_map = {
        'limitless': Limitless,
        'gratitude': Gratitude,
        'emotion': Emotion,
        'affirmation': Affirmation,
        'dream': Dream,
        'journey': Journey,
        'lesson': Lesson
    }
    return entry_type_map.get(entry_type)



def save_ml_results(user_id, book_id, predictions, labels, model_name="OCEAN"):
    print(f"Saving ML results for user {user_id} and book {book_id}")
    # Find the index of the highest prediction score
    max_index = predictions[0].argmax().item()

    # Corresponding label for the highest score
    winning_trait = labels[max_index]

    # Score for the winning trait
    winning_score = predictions[0][max_index].item()

    # Prepare additionalInfo with all scores
    additional_info = {labels[i]: predictions[0][i].item() for i in range(len(labels))}

    # Check if a result already exists for this book and update if so, or create a new one
    existing_result = Result.query.filter_by(bookId=book_id, modelName=model_name).first()
    if existing_result:
        existing_result.modelName = model_name  # or your dynamic model name here
        existing_result.traitName = winning_trait
        existing_result.traitValue = str(winning_score)
        existing_result.additionalInfo = additional_info
    else:
        # Create a new Result object with the winning trait and all scores
        new_result = Result(bookId=book_id, modelName=model_name, traitName=winning_trait,
                            traitValue=str(winning_score), additionalInfo=additional_info)
        db.session.add(new_result)
    
    db.session.commit()


# Saves a row for each trait name and its corresponding value. Not just the winner. 
# def save_ml_results(user_id, book_id, predictions, model_name='OCEAN'):
#     print(f"Saving ML results for user {user_id} and book {book_id}")
#     labels = ['Agreeableness', 'Extraversion', 'Neuroticism', 'Conscientiousness', 'Openness']
    
#     # Convert predictions to a list if it's not already (depends on your return_prediction function implementation)
#     predictions_list = predictions[0].tolist() if not isinstance(predictions, list) else predictions
    
#     for i, label in enumerate(labels):
#         # Here, we're assuming the trait value is the score itself. Modify as needed for your actual data structure.
#         trait_value = str(predictions_list[i])
        
#         # Assuming you want to save the additionalInfo as the scores for all traits
#         # You might want to structure it more cleanly, depending on how you plan to use it later.
#         additional_info = {lbl: predictions_list[j] for j, lbl in enumerate(labels)}
        
#         # Create a new Result object
#         new_result = Result(bookId=book_id, modelName=model_name, traitName=label, traitValue=trait_value, additionalInfo=additional_info)
#         db.session.add(new_result)
        
#     db.session.commit()
