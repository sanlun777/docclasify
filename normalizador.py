import spacy
import pandas as pd
import sys

nlp = spacy.load("en_core_web_trf")

# normalizar el texto
def normalize_text(texto):
    if pd.isnull(texto):
        return ""
    doc = nlp(texto)
    tokens_normalizados = []
    for token in doc:
        if not token.is_stop and token.pos_ not in ['DET', 'ADP', 'CONJ', 'PRON']:
            tokens_normalizados.append(token.lemma_)
    texto_normalizado = " ".join(tokens_normalizados)
    return texto_normalizado

# normalizar un DataFrame en las columnas dadas
def normalizar_columnas(df, columnas_a_normalizar):
    for columna in columnas_a_normalizar:
        if columna in df.columns:
            df[columna] = df[columna].fillna('').apply(normalize_text)
        else:
            print(f"La columna '{columna}' no existe en el archivo CSV.")
    return df

def main():
    corpusn = sys.argv[1]
    df = pd.read_csv(f'{corpusn}.csv', sep='\t')
    normalizar_columnas(df, ('title','abstract'))
    df.to_csv(f'{corpusn}_norm.csv', sep='\t')

if __name__ == "__main__":
    main()

