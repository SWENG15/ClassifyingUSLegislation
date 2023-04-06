"""
model provides the ML classification for state legislation,
including training the models as well as returning classifications
"""
#pylint: disable=duplicate-code
import sys
import csv
import codecs
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression


def train_model(training_data='../ETL_pipeline/dataset.csv'):
    """train_model trains a Naive Bayes classifier for subject matter based on 
        the path to a dataset given (optionally) in args"""

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

    # Split the data into training and testing sets
    text = data['combined_text']
    subject = data['subject']
    vectorizer = CountVectorizer()
    text = vectorizer.fit_transform(text)
    #test_size determines how much of the data is used to test the model,
    # with the remaining used to train
    #x_train, x_test, y_train, y_test = train_test_split(text, subject, test_size=0.2)
    x_train, _, y_train, _ = train_test_split(text, subject, test_size=0.1)

    # Train a Naive Bayes classifier on the training data
    clf = MultinomialNB()
    clf.fit(x_train, y_train)
    
    save_model(clf, vectorizer, state)
    return clf, vectorizer

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
    #for serialization
    #clf, vectorizer = load_classification_model()

    # Print the predicted subject for the new text
    return input_pred


# pylint: disable=too-many-locals
def train_regression_model(training_data='../ETL_pipeline/datasets/west-virginia-dataset.csv'):
    """
    train_regression_model trains the model to estimate how likely a bill is to pass or fail
    """
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int/10)

    with codecs.open(training_data, 'r', encoding='Latin1') as file:
        reader = csv.reader(file)
        data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

    # Only the bills with the tags 'passed' and 'vetoed'
    # will be considered in the training of the regression algorithm
    bill_tags = ["Passed", "Vetoed"]
    data = data[data.status.isin(bill_tags)]

    # Replace missing values with an empty string
    data['title'] = data['title'].fillna('')
    data['text'] = data['text'].fillna('')
    data['status'] = data['status'].fillna('')

    # Combine text and title columns
    data['combined_text'] = data['text'] + ' ' + data['title']

    # Drop the ID column
    data = data.drop('ID', axis=1)
    # Drop the Subject column
    data = data.drop('subject', axis=1)
    # Drop the text column
    data = data.drop('text', axis=1)
    # Drop the title column
    data = data.drop('title', axis=1)

    # Get one hot encoding of column status
    one_hot = pd.get_dummies(data['status'])
    # Drop column 'status' as it is now encoded
    data = data.drop('status',axis = 1)
    # Join the encoded data
    data = data.join(one_hot)

    # Split the data into training and testing sets
    text = data['combined_text']
    #If the bill has been passed this column will have a 1.
    #If the bill has been vetoed it will have a 0.
    status = data['Passed']
    vectorizer = CountVectorizer()
    text = vectorizer.fit_transform(text)

    #test_size determines how much of the data is used to test the model, remaining used to train
    x_train, x_test, y_train, y_test = train_test_split(text, status, test_size=0.1)
    #x_train, _, y_train, _ = train_test_split(text, status, test_size=0.1)

    # Train a logistic regression model on the training set
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # Calculate the error rate using the testing set
    y_pred = model.predict(x_test)
    error_rate = mean_squared_error(y_test, y_pred)
    print(f"Error rate: {error_rate}")

    #for serialization
    #with open('regression_model.pkl', 'wb') as f:
     #   pickle.dump((model, vectorizer), f)

    return model, vectorizer

def predict_pass(model, vectorizer, text):
    """
    predict_pass predicts the probability of a given bill passing.
    A trained logistic regression model is passed in as well as 
    a vectorizer to get the text into the right format
    The probability of the bill passing is then returned.
    """
    # Take new text and predict the likelihood that it passes
    # the input would go in new text string
    # If the new text string has a problem,
    # namely if the text has a ' in it, it would give an error,
    # so omit that out beefore inputting
    input_test = vectorizer.transform([text])
    #This gets the likelihood of the bill passing - does not just classify whether it will pass/fail
    input_pred = model.predict_proba(input_test)[:, 1]

    #for serialization
    # model, vectorizer = load_regression_model()

    # Return the predicted likelihood for the new text
    return input_pred

def save_model(clf, vectorizer, state):
    """save_model saves the trained classification model and vectorizer 
    to the specified paths"""
    model_path = 'ML/saved_models/'+ state + '_pass_model.pkl'
    vectorizer_path='ML/saved_models/'+ state + '_pass_vectorizer.pkl'
    with open(model_path, 'wb') as model_file:
        pickle.dump(clf, model_file)

    with open(vectorizer_path, 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

def load_model(state,model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
    """load_model loads a previously saved classification model and vectorizer
    from the specified paths"""
    model_path = 'ML/saved_models/'+ state + '_pass_model.pkl'
    vectorizer_path='ML/saved_models/'+ state + '_pass_vectorizer.pkl'
    with open(model_path, 'rb') as model_file:
        clf = pickle.load(model_file)

    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    return clf, vectorizer
