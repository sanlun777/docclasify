import csv
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import sys
import json
# Prefix of corpus to vectorize; needs to be normalized first
corpusn = sys.argv[1]

# Where to store the result of vectorization
based = f'{corpusn}_vectors'

os.makedirs(based, exist_ok=True)

corpus = []
header = []

try:
    with open(f'{corpusn}_norm.csv', 'r', newline='') as csvf:
        reader = csv.DictReader(csvf, dialect='excel-tab')
        for row in reader:
            json.dumps(row)
            try:
                corpus.append(f'{row['title']} {row['abstract']}')

            except Exception as e:
                 print(f"Error procesando fila: {e}")

    print(f"Se leyeron {len(corpus)} documentos.")

except FileNotFoundError:
    print(f"Error: El archivo de entrada '{input_csv_file}' no fue encontrado.")
    exit()
except Exception as e_read:
    print(f"Ocurrió un error inesperado durante la lectura del CSV: {e_read}")
    exit()

if corpus:
    try:
        for rep in ('freq', 'tf-idf', 'binarized'):
            ngram = (1,1)

            print(f'Generando representación {rep} con NGRAMA {ngram}')
            vectorizer = None
            if(rep == 'freq'):
                vectorizer = CountVectorizer(ngram_range=ngram)
            elif(rep == 'binarized'):
                vectorizer = CountVectorizer(ngram_range=ngram, binary=True)
            elif(rep == 'tf-idf'):
                vectorizer = TfidfVectorizer(ngram_range=ngram)

            X = vectorizer.fit_transform(corpus)
            print(f"  Matriz de Frecuencia generada (dispersa): {X.shape}")
            print(f"  Vocabulario (features): {len(vectorizer.get_feature_names_out())} términos")

            with open(os.path.join(based, f'{rep}_mat.pkl'), 'wb') as mat:
                pickle.dump(X, mat)

            with open(os.path.join(based, f'{rep}_vectzer.pkl'), 'wb') as vec:
                pickle.dump(vectorizer, vec)

    except Exception as e:
        print(f"  ERROR al generar/guardar representación: {e}")

else:
    print("No se encontraron textos en el archivo CSV para procesar.")
