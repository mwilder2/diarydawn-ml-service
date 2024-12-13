# ml_command.py
import logging
from app.common.database.db_interactions import get_pages_and_entry_types_by_book_and_user, save_ml_results
from app.ml.voting_systems.disc.disc_system import return_disc_predictions
from app.ml.voting_systems.ocean.ocean_system import return_ocean_predictions
from app.ml.data_preprocessing.preprocessors import concatenate_and_refine_data, preprocess_text
from app.ml.voting_systems.vark.vark_system import return_vark_predictions
from app.pub_sub.publisher import publish_complete_message, publish_public_results_complete_message

def process_ml_for_book(user_id, book_id):
    print(f"Processing ML for user {user_id} and book {book_id}")
    try:
        # Extract and preprocess data (common steps)
        data = get_pages_and_entry_types_by_book_and_user(user_id, book_id)
        preprocessed_data = concatenate_and_refine_data(data)

        # Process each model
        models_to_process = ['OCEAN', 'DISC', 'VARK'] 
        for model in models_to_process:
            if model == 'OCEAN':
                model_paths = get_ocean_model_paths()
                predictions, labels, winning_trait, winning_score = return_ocean_predictions(preprocessed_data, model_paths)
            elif model == 'DISC':
                model_paths = get_disc_model_paths() 
                predictions, labels, winning_trait, winning_score = return_disc_predictions(preprocessed_data, model_paths)
            # elif model == 'VARK':
            #     model_paths = get_vark_model_paths() 
            #     predictions, labels, winning_trait, winning_score = return_vark_predictions(preprocessed_data, model_paths)
            # Save results for the current model
            save_ml_results(user_id, book_id, predictions, labels, model_name=model)  # Assuming save_ml_results can accept a model_name

            # Optionally, log the winning trait and score for debugging or verification
            print(f"{model} results: {winning_trait} with a score of {winning_score}")

        # Prepare and publish completion message
        completion_message = "ML processing completed for all models"
        # publish_complete_message(user_id, book_id)
        print(completion_message)

        return completion_message
    except Exception as e:
        logging.error(f"An error occurred during ML processing for user {user_id} and book {book_id}: {e}")
        # Handle or raise the exception as appropriate for your application's error handling strategy
        
        
def process_text_for_public(text):
    print("Processing public text")
    try:
        preprocessed_text = preprocess_text(text)
        results = {}
        
        # Process each model
        models_to_process = ['OCEAN', 'DISC', 'VARK']
        for model in models_to_process:
            if model == 'OCEAN':
                model_paths = get_ocean_model_paths()
                predictions, labels, winning_trait, winning_score = return_ocean_predictions(preprocessed_text, model_paths)
            elif model == 'DISC':
                model_paths = get_disc_model_paths() 
                predictions, labels, winning_trait, winning_score = return_disc_predictions(preprocessed_text, model_paths)
            elif model == 'VARK':
                model_paths = get_vark_model_paths() 
                predictions, labels, winning_trait, winning_score = return_vark_predictions(preprocessed_text, model_paths)
            
            results[model] = {
                'modelName': model,
                'traitName': winning_trait,
                'traitValue': f"{winning_score:.4f}"  # Format the trait value to 4 decimal places
            }
        
        # Publish results after processing all models
        publish_public_results_complete_message(results)

    except Exception as e:
        print(f"Error processing public text: {e}")
        return {'error': 'Failed to process text'}


def get_ocean_model_paths():
    model_paths = [
        "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_ocean_pos_april_2024_v2",
        "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_ocean_tfidf_april_2024_v2",
        "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_ocean_semantic_april_2024_v1"
    ]
    return model_paths

def get_disc_model_paths():
    model_paths = [
        "/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_fasttext_april_2024_v1",
        "/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_pos_april_2024_v2",
        '/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_semantic_april_2024_v1',
        '/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_tfidf_april_2024_v2',
    ]
    return model_paths

def get_vark_model_paths():
    model_paths = [
        "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_pos_april_2024_v1",
        "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_semantic_april_2024_v1",
        "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_tfidf_april_2024_v2",
        "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_fasttext_april_2024_v1",
    ]
    return model_paths

# def get_model_paths(model_name):
#     if model_name == 'OCEAN':
#         return [
#         "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_model_ocean_pos_april_2024_v1",
#         "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_model_ocean_tfidf_april_2024_v1",
#         "/codebase/app/ml/classifiers/ocean/distilbert_sst_fine_tuned_ocean_semantic_april_2024_v1"
#         ]
#     elif model_name == 'DISC':
#         return [
#         "/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_fasttext_april_2024_v1",
#         "/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_pos_april_2024_v2",
#         '/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_semantic_april_2024_v1',
#         '/codebase/app/ml/classifiers/disc/distilbert-sst-2-finetuned_disc_tfidf_april_2024_v2',
#         ]
#     elif model_name == 'VARK':
#         return [
#         "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_pos_april_2024_v1",
#         "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_semantic_april_2024_v1",
#         "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_tfidf_april_2024_v2",
#         "/codebase/app/ml/classifiers/vark/distilbert_sst_fine_tuned_vark_fasttext_april_2024_v1",
#         ]
#     else:
#         raise ValueError("Unsupported model type")





