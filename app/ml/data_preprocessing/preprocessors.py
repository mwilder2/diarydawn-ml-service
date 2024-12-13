import re

def concatenate_entry_content(pages):
    concatenated_content = ""
    for page in pages:
        # Check if 'entry_type_data' exists and if 'content' exists within it
        if 'entry_type_data' in page and 'content' in page['entry_type_data']:
            content = page['entry_type_data']['content']
            concatenated_content += " " + content  # Add a space between contents for readability
    return concatenated_content.strip()  # Remove any leading or trailing whitespace


def remove_control_characters(s):
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)

def preprocess_text(text):
    text = text.strip()
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = text.lower()  # Lowercase
    text = re.sub('\s+', ' ', text)  # Replace multiple whitespaces with a single space
    text = re.sub('[^A-Za-z0-9\s]+', ' ', text)  # Remove special characters, keep only alphanumeric and spaces
    return text
  
def concatenate_and_refine_data(data):
  
    # Step 1: Concatenate content from all pages
    concatenated_content = concatenate_entry_content(data)
    
    # Step 2: Remove control characters
    refined_content = remove_control_characters(concatenated_content)
    
    # Step 3: Preprocess text
    preprocessed_text = preprocess_text(refined_content)
    
    return preprocessed_text