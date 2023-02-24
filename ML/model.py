import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv
import codecs

# Load the data from a CSV file in Latin1 encoding
with codecs.open('../ETL_pipeline/datasets/subject_dataset.csv', 'r', encoding='Latin1') as file:
    reader = csv.reader(file)
    data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

# Drop the ID column
data = data.drop('ID', axis=1)
# Drop the Status column
data = data.drop('status', axis=1)

#Check the data description
print(data.head())

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
new_text = 'A senate RESOLUTION TO RECOGNIZE AND HONOR robert mitchum as one of the greatest motion picture stars of the twentieth century. Whereas, the members of the South Carolina Senate are pleased to recognize the celebrated actor, Robert Mitchum, as one of the greatest motion picture stars of the twentieth century; and Whereas, a native of Bridgeport, Connecticut, Robert Mitchum was born on August 6, 1917, to parents Annie Gunderson and James Mitchum, a native of the town of Lane, in Williamsburg County, South Carolina; and Whereas, during the Great Depression, young Robert Mitchum left home to lessen the financial burden on his family. In 1933, he was arrested for vagrancy and sentenced to thirty days on a chain gang. He escaped the chain gang and made his way to a farm owned by his aunt and uncle, Idell and Alfred Mitchum, in Lane, South Carolina; and Whereas, in the mid-1930s, Robert Mitchum moved to the West Coast, where he began his career in Hollywood as a writer and actor. He started winning roles in cowboy movies in 1943. In 1944, he co-starred with Spencer Tracy in Thirty Seconds Over Tokyo. The following year, he co-starred with Burgess Meredith in The Story of G.I. Joe and was nominated for an Oscar for Best Supporting Actor; and Whereas, after his Oscar nomination, Robert Mitchum career exploded and he became one of the biggest stars of the twentieth century, making over eighty motion pictures until his death in 1997; and Whereas, over the years, Robert Mitchum maintained contact with his Williamsburg family. He invited them to Asheville, North Carolina in 1957 when he filmed Thunder Road. The same year, he was interviewed for a column by Earl Wilson. When Wilson asked him where he was from, Robert Mitchum replied,"Im from Lane, South Carolina and Whereas, three years later, Robert Mitchum was in Savannah making Cape Fear and invited his relatives to visit, and many came. He also hired his cousin, Douglas Mitchum, Idell and Alfreds son, to be his driver during the filming; and Whereas, Robert Mitchum married Dorothy Spencer in 1940, and together they had three children; and Whereas, with a historical marker in the park in Lane and designation of a week-long Robert Mitchum Film Festival, Williamsburg County celebrates this great actor and claims him as truly one of our own; and Whereas, the members of the South Carolina Senate greatly appreciate the dedication and commitment that Robert Mitchum has shown in serving the people and the State of South Carolina. Now, therefore, Be it resolved by the Senate: That the members of the South Carolina Senate, by this resolution, hereby recognize and honor Robert Mitchum as one of the greatest motion picture stars of the twentieth century. Be it further resolved that a copy of this resolution be presented to the family of Robert Mitchum'
input_test = vectorizer.transform([new_text])
input_pred = clf.predict(input_test)

y_pred = clf.predict(X_test)
score = accuracy_score(y_test, y_pred)
print(score)

# Print the predicted subject for the new text
print(input_pred)
