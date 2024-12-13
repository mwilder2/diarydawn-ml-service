from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_model(model_path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        print(f'Loaded model and tokenizer from {model_path}.')
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        raise
    return model, tokenizer

def predict(text, tokenizer, model):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        logits = model(inputs.input_ids, attention_mask=inputs.attention_mask).logits
    predictions = torch.softmax(logits, dim=-1)
    return predictions

def aggregate_predictions(predictions_list):
    # Assuming predictions_list is a list of torch tensors
    averaged_predictions = torch.mean(torch.stack(predictions_list), dim=0)
    return averaged_predictions

def return_disc_predictions(text, model_paths):
    labels = ['dominance', 'influence', 'steadiness', 'compliance']
    predictions_list = []

    for model_path in model_paths:
        model, tokenizer = load_model(model_path)
        predictions = predict(text, tokenizer, model)
        predictions_list.append(predictions)

        # Displaying each classifier's vote
        max_index = predictions.argmax().item()
        print(f"Classifier {model_path} voted for {labels[max_index]} with a score of {predictions[0][max_index].item()}")

    # Aggregate predictions
    averaged_predictions = aggregate_predictions(predictions_list)

    # Optionally, you can include logic here to select the top trait and its average score
    max_index = averaged_predictions.argmax().item()
    winning_trait = labels[max_index]
    winning_score = averaged_predictions[0][max_index].item()

    return averaged_predictions, labels, winning_trait, winning_score