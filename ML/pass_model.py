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
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression

# pylint: disable=too-many-locals
def train_regression_model(state,
                           training_data='../etl_pipeline/datasets/west-virginia-dataset.csv'):
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

    data = data.replace(to_replace="Failed/Dead", value="Vetoed")
    data = data.replace(to_replace="Failed", value="Vetoed")

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
    x_train, x_test, y_train, y_test = train_test_split(
        text, status, test_size=0.1, random_state=42
    )
    #x_train, _, y_train, _ = train_test_split(text, status, test_size=0.1, random_state=42)

    # Train a logistic regression model on the training set
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # Calculate the error rate using the testing set
    y_pred = model.predict(x_test)
    error_rate = mean_squared_error(y_test, y_pred)
    print(f"Error rate: {error_rate}")
    save_model(model, vectorizer, state)
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

    # Return the predicted likelihood for the new text
    return input_pred

def save_model(clf, vectorizer, state):
    """save_model saves the trained pass model and vectorizer 
    to the specified paths"""
    model_path = 'ML/saved_models/'+ state + '_pass_model.pkl'
    vectorizer_path='ML/saved_models/'+ state + '_pass_vectorizer.pkl'
    with open(model_path, 'wb') as model_file:
        pickle.dump(clf, model_file)

    with open(vectorizer_path, 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

def load_model(state):
    """load_model loads a previously saved pass model and vectorizer
    from the specified paths"""
    model_path = state + '_pass_model.pkl'
    vectorizer_path=state + '_pass_vectorizer.pkl'
    with open(model_path, 'rb') as model_file:
        clf = pickle.load(model_file)

    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    return clf, vectorizer

STATE = "west-virginia"
FILENAME = f"etl_pipeline/datasets/{STATE}-dataset.csv"
if __name__ == "__main__":
    train_regression_model(STATE, training_data=FILENAME)
