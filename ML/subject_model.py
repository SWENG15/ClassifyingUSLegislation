"""
model provides the ML classification for state legislation,
including training the models as well as returning classifications
"""
#pylint: disable=duplicate-code
import sys
import csv
import codecs
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(training_data='../ETL_pipeline/dataset.csv'):
    """train_model trains a Naive Bayes classifier for subject matter based on 
        the path to a dataset given (optionally) in args"""
    data = prepare_data(training_data)
    
    # Split the data into training and testing sets
    text = data['combined_text']
    subject = data['subject']
    vectorizer = CountVectorizer()
    text = vectorizer.fit_transform(text)
    #test_size determines how much of the data is used to test the model,
    # with the remaining used to train
    x_train, _, y_train, _ = train_test_split(text, subject, test_size=0.005)

    # Train a Naive Bayes classifier on the training data
    clf = MultinomialNB()
    clf.fit(x_train, y_train)

    #y_pred = clf.predict(x_test)
    #score = accuracy_score(y_test, y_pred)
    #print(score)

    return clf, vectorizer

def prepare_data(training_data):
    """
    prepare_data takes in the path to the training data, 
    then modifies it as necessary 
    before returning the data in the correct form
    """
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
    # Drop the Status column
    data = data.drop('status', axis=1)

    #Check the data description
    #print(data.head())

    # Replace missing values with an empty string
    data['title'] = data['title'].fillna('')
    data['text'] = data['text'].fillna('')
    data['subject'] = data['subject'].fillna('')

    # Combine text and title columns
    data['combined_text'] = data['text'] + ' ' + data['title']

    return data

def predict_subject(clf, vectorizer, text):
    """
    predict_subject predicts the subject of a bill given
    its text and a trained classification model 
    (and the vectorizer necessary to get the text into the correct format)
    """
    # Take new text and predict its subject
    # the input would go in new text string
    # If the new text string has a problem,
    # namely if the text has a ' in it, it would give an error,
    # so omit that out beefore inputting
    input_test = vectorizer.transform([text])
    input_pred = clf.predict(input_test)

    # Print the predicted subject for the new text
    return input_pred

def train_model_accuracy(training_data):
    """
    train_model_accuracy trains the model, 
    but instead of returning the model, it returns the accuracy
    """
    data = prepare_data(training_data)

    print("Length of data: ",len(data))
    
    # Split the data into training and testing sets
    text = data['combined_text']
    subject = data['subject']
    vectorizer = CountVectorizer()
    text = vectorizer.fit_transform(text)

    #test_size determines how much of the data is used to test the model,
    # with the remaining used to train
    x_train, x_test, y_train, y_test = train_test_split(text, subject, test_size=0.005)

    # Train a Naive Bayes classifier on the training data
    clf = MultinomialNB()
    clf.fit(x_train, y_train)

    # Find the accuracy of the model
    y_pred = clf.predict(x_test)
    return accuracy_score(y_test, y_pred)
