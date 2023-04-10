"""The purpose of this algorithm is to enable our user to find and
and read bills that are similar to the bill they are currently viewing.
The user simply enters the bill for which they wish to find similar
bills for and the program will return a specific number of bills that
are similar to the one they entered (the default is set to 10)."""
import sys
import csv
import codecs
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#pylint: disable=duplicate-code

def train_similarity_model(state, training_data='etl_pipeline/datasets/west-virginia-dataset.csv'):
    """train_similarity_model is using Python's Scikit-learn library to preprocess 
    and vectorize text data from our dataset and calculate the cosine similarity
    between the vectors of the bills in the file"""

    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int/10)

    # Load the data from a CSV file in Latin1 encoding
    with codecs.open(training_data, 'r', encoding='Latin1') as file:
        reader = csv.reader(file)
        data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

    # Drop the ID column
    data = data.drop('ID', axis=1)

    # Fill missing text values with empty strings
    # data['text'] = data['text'].fillna('')

    # Vectorize text
    vectorizer = TfidfVectorizer()
    vectorized_text = vectorizer.fit_transform(data.loc[:, 'text'])

    # Return trained model
    save_model(vectorizer, vectorized_text, data, state)
    return vectorizer, vectorized_text, data

def predict_similar_bills(bill, trained_model, num_of_similar_bills=10):
    """print_similar_bills takes a single bill text, the trained model
    including vectorizer, vectorized_text, and data,
    and a number of similar bills to return, and prints the most 
    similar bills based on the cosine similarity scores"""

    # Extract trained model components
    vectorizer, vectorized_text, data = trained_model

    # Transform input bill text using the trained vectorizer
    bill_vectorized = vectorizer.transform([bill])

    # Calculate cosine similarity scores between the input bill and all other bills in the dataset
    similarity_scores = cosine_similarity(bill_vectorized, vectorized_text)

    # Get most similar bills
    similar_bills = data.iloc[similarity_scores.argsort()[0][-num_of_similar_bills:], :]

    # Return results
    return similar_bills

def save_model(vectorizer, vectorized_text, data, state):
    """save_model saves the trained similarity model and vectorized data
    to the specified path"""
    vectorizer_path = 'ML/saved_models/'+ state + '_similarity_vectorizer.pkl'
    vectorized_text_path = 'ML/saved_models/'+ state + '_similarity_vectorized_data.pkl'
    data_path = 'ML/saved_models/'+ state + '_similarity_data.pkl'
    with open(vectorizer_path, 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
    with open(vectorized_text_path, 'wb') as vectorized_text_file:
        pickle.dump(vectorized_text, vectorized_text_file)
    with open(data_path, 'wb') as data_file:
        pickle.dump(data, data_file)

def load_model(state):
    """load_model loads a previously saved similarity 
    model from the specified paths"""
    vectorizer_path = state + '_similarity_vectorizer.pkl'
    vectorized_text_path = state + '_similarity_vectorized_data.pkl'
    data_path =  state + '_similarity_data.pkl'
    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    with open(vectorized_text_path, 'rb') as vectorized_text_file:
        vectorized_text = pickle.load(vectorized_text_file)
    with open(data_path, 'rb') as data_file:
        data = pickle.load(data_file)
    return vectorizer, vectorized_text, data

STATE = "idaho"
FILENAME = f"etl_pipeline/datasets/{STATE}-dataset.csv"
if __name__ == '__main__':
    # Train the model
    train_model = train_similarity_model(STATE, training_data=FILENAME)

    # Find similar bills for an input bill
    #INPUT_BILL = "An act to promote sustainability in public transportation"
    #print(predict_similar_bills(INPUT_BILL, train_model, num_of_similar_bills=5))
