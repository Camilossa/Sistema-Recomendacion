import streamlit as st
import pickle
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode  # Librería para eliminar tildes y acentos

# Descarga de stopwords
nltk.download('stopwords')

# Cargar los datos
df = pd.DataFrame()
pkls = Path('./borges').glob('*texts.pkl') 

# Leer todos los archivos pickle y concatenarlos en un DataFrame
for pkl in pkls:
    with open(pkl, 'rb') as inp:
        df_ = pickle.load(inp)
    df = pd.concat([df, df_])

df = df.drop_duplicates(subset=[c for c in df.columns if c != 'text_metadata'])
# Reiniciar el índice para evitar problemas de desajuste
df = df.reset_index(drop=True)

# Extraer título y autor de los metadatos
df['title'] = df['text_metadata'].apply(lambda x: x['title'])
df['author'] = df['text_metadata'].apply(lambda x: x['author'])

# Preparar las stopwords
stop = list(stopwords.words('spanish'))

# Crear el vectorizador TF-IDF
tf = TfidfVectorizer(stop_words=stop)

# Calcular las características para cada elemento (texto)
tfidf_matrix = tf.fit_transform(df['text'])

# Calcular las similitudes coseno entre todos los documentos
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
n = 6  # Número de recomendaciones a mostrar

# Diccionario para almacenar resultados con claves normalizadas (minúsculas y sin acentos)
results = {}
for idx, row in df.iterrows():
    # Normalizar la clave convirtiéndola a minúsculas y eliminando acentos
    key = unidecode(f"{row['author'].lower()} - {row['title'].lower()}")
    similar_indices = cosine_similarities[idx].argsort()[:-n-2:-1]
    similar_items = [(f"{df['author'][i]} - {df['title'][i]}", round(cosine_similarities[idx][i], 3)) for i in similar_indices]
    results[key] = similar_items[1:]

# Función de recomendación con coincidencia insensible a mayúsculas y acentos
def recomendar(autor, titulo):
    # Normalizar la entrada convirtiéndola a minúsculas y eliminando acentos
    key = unidecode(f"{autor.lower()} - {titulo.lower()}")
    recomendaciones = results.get(key, "No se encontraron resultados")
    
    if isinstance(recomendaciones, str):
        return recomendaciones  # Retornar el mensaje de error si no hay resultados
    
    # Formatear los resultados con saltos de línea y redondear los puntajes
    formatted_result = "\n".join([f"{item[0]}: {float(item[1]):.3f}" for item in recomendaciones])
    return formatted_result


# CSS personalizado para la imagen de fondo
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://pics.craiyon.com/2023-06-15/5c14db2bf0ec41fd87bb61cc936e7be9.webp");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Interfaz en Streamlit
st.title("Recomendador de Autores y Libros")

# Campos de entrada para autor y título sin valores predeterminados
autor = st.text_input("Ingrese el Autor")
titulo = st.text_input("Ingrese el Título")

if st.button("Recomendar"):
    # Llamar a la función de recomendación y mostrar los resultados
    recomendaciones = recomendar(autor, titulo)
    container = st.container()

    # Mostrar recomendaciones dentro del contenedor con fondo negro
    with container:
        st.markdown(
            """
            <div style='background-color:black;color:white;padding:10px;border-radius:5px;'>
                <h3>Recomendaciones</h3>
                <p>{}</p>
            </div>
            """.format(recomendaciones.replace('\n', '<br>')),
            unsafe_allow_html=True
        )
