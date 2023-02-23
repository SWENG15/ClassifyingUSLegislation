import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv
import codecs

# Load the data from a CSV file in Latin1 encoding
with codecs.open('subject_dataset.csv', 'r', encoding='Latin1') as file:
    reader = csv.reader(file)
    data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

# Drop the ID column
data = data.drop('ID', axis=1)
# Drop the Status column
data = data.drop('status', axis=1)

#Check the data description
data.head()

# Replace missing values with an empty string
data['title'] = data['title'].fillna('')
data['text'] = data['text'].fillna('')
data['subject'] = data['subject'].fillna('')

# Combine text and title columns
data['combined_text'] = data['text'] + ' ' + data['title']

# Split the data into training and testing sets
X = data['combined_text']
y = data['subject']
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)
#test_size determines how much of the data is used to test the model, with the remaining used to train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a Naive Bayes classifier on the training data
clf = MultinomialNB()
clf.fit(X_train, y_train)

# Take new text and predict its subject
#the input would go in new text string
#the new text string has a problem, namely if the text has a ' in it, it would give an error, so omit that out beefore inputting
#new_text = 
#input_test = vectorizer.transform([new_text])
#input_pred = clf.predict(input_test)

y_pred = clf.predict(X_test)
score = accuracy_score(y_test, y_pred)
score

# Print the predicted title for the new text
#print(input_pred)
