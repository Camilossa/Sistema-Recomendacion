import streamlit as st
import pickle
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords

# Descarga de stopwords
nltk.download('stopwords')

# Load data
df = pd.DataFrame()
pkls = Path('./borges/datasets/datasets_pkl').glob('*texts.pkl') 

# Read all pickle files and concatenate into a DataFrame
for pkl in pkls:
    with open(pkl, 'rb') as inp:
        df_ = pickle.load(inp)
    df = pd.concat([df, df_])

df = df.drop_duplicates(subset=[c for c in df.columns if c != 'text_metadata'])
# Reset index to avoid index mismatch issues
df = df.reset_index(drop=True)

# Extract title and author from metadata
df['title'] = df['text_metadata'].apply(lambda x: x['title'])
df['author'] = df['text_metadata'].apply(lambda x: x['author'])

# Prepare stop words
stop = list(stopwords.words('spanish'))

# Create TF-IDF vectorizer
tf = TfidfVectorizer(stop_words=stop)

# Compute features for each item (text)
tfidf_matrix = tf.fit_transform(df['text'])

# Calculate cosine similarities between all documents
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
n = 6

# Dictionary to store results
results = {}
for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-n-2:-1]
    similar_items = [(f"{df['author'][i]} - {df['title'][i]}", round(cosine_similarities[idx][i], 3)) for i in similar_indices]
    results[f"{row['author']} - {row['title']}"] = similar_items[1:]

# Recommendation function
def recomendar(autor, titulo):
    recomendaciones = results.get(f"{autor} - {titulo}", "No se encontraron resultados")
    
    if isinstance(recomendaciones, str):
        return recomendaciones  # Retornar el mensaje de error si no hay resultados
    
    # Formatear los resultados con saltos de línea y redondear los puntajes
    formatted_result = "\n".join([f"{item[0]}: {float(item[1]):.3f}" for item in recomendaciones])
    return formatted_result


# Custom CSS for background image
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


# Streamlit Interface
st.title("Recomendador de Autores y Libros")

# Input fields for author and title without default values
autor = st.text_input("Ingrese el Autor")
titulo = st.text_input("Ingrese el Título")

if st.button("Recomendar"):
    # Call the recommendation function and display the results
    recomendaciones = recomendar(autor, titulo)
    container = st.container()

    # Display recommendations inside the container with a black background
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
