import csv
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

import sys

corpusn = sys.argv[1]

X = []
y = []

try:
    with open(corpusn, 'r', newline='') as csvf:
        reader = csv.DictReader(csvf, dialect='excel-tab')
        for row in reader:
            try:
                X.append(f'{row['title']} {row['abstract']}')
                y.append(row['section'])
            except Exception as e:
                 print(f"Error procesando fila: {e}")


except FileNotFoundError:
    print(f"Error: El archivo de entrada '{input_csv_file}' no fue encontrado.")
    exit()
except Exception as e_read:
    print(f"Ocurrió un error inesperado durante la lectura del CSV: {e_read}")
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

for rep in (TfidfVectorizer(), CountVectorizer(), CountVectorizer(binary=True)):
    for classifier in (MultinomialNB(), LogisticRegression(max_iter=2048), SVC()):
        print(f'This is a report with the vectorizer {type(rep).__name__} and the classifier {type(classifier).__name__}')
        pipe = Pipeline([('text_representation', rep), ('classifier', classifier)])
        pipe.fit(X_train, y_train)
        print(pipe['text_representation'].get_feature_names_out())
        y_pred = pipe.predict(X_test)
        print(classification_report(y_test, y_pred))

