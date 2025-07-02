# Install required packages (run these lines in your environment if not already installed)
# !pip install spacy pandas boto3
# !python -m spacy download en_core_web_sm

import pandas as pd
import spacy
import boto3
from botocore.exceptions import NoCredentialsError

# Load spaCy's English model for Named Entity Recognition
nlp = spacy.load('en_core_web_sm')

def extract_names_from_text(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

def read_file_and_extract_names(file_path):
    names = []
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        for col in df.select_dtypes(include=['object']).columns:
            for text in df[col].dropna():
                names.extend(extract_names_from_text(str(text)))
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            names = extract_names_from_text(text)
    return list(set(names))  # Remove duplicates

def write_names_to_file(names, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for name in names:
            f.write(name + '\n')

def upload_file_to_s3(file_name, bucket, s3_file_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_name, bucket, s3_file_name)
        print(f"File uploaded successfully to s3://{bucket}/{s3_file_name}")
        return True
    except FileNotFoundError:
        print("The file was not found.")
        return False
    except NoCredentialsError:
        print("AWS credentials not available.")
        return False

# Example usage:
# file_path = 'your_input_file.txt'  # or .csv
# output_file = 'extracted_names.txt'
# s3_bucket = 'your-s3-bucket-name'
# s3_key = 'folder/extracted_names.txt'

# names = read_file_and_extract_names(file_path)
# write_names_to_file(names, output_file)
# upload_file_to_s3(output_file, s3_bucket, s3_key)
