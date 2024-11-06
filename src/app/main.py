import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Función para preprocesar el texto
def preprocess_text(text):
    if pd.isna(text):
        return ''
    text = text.lower()  # Convertir a minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar puntuación
    return text

# Cargar los datasets
movie_df = pd.read_csv('D:/SOYHENRY_PI_1/fastapi_project/movie_dataset_cleaned.csv')
cast_df = pd.read_csv('D:/SOYHENRY_PI_1/fastapi_project/cast_dataset.csv')
crew_df = pd.read_csv('D:/SOYHENRY_PI_1/fastapi_project/crew_dataset.csv')

# Definir las columnas de texto relevantes para cada DataFrame
text_columns = {
    'movie_df': ['title', 'overview', 'genres', 'tagline'],
    'cast_df': ['character', 'name'],
    'crew_df': ['department', 'job', 'name']
}

# Preprocesar cada columna de texto en cada DataFrame
for df_name, columns in text_columns.items():
    df = globals()[df_name]  # Obtener el DataFrame por su nombre
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(preprocess_text)

# Función para obtener texto combinado de varias columnas de un DataFrame
def get_combined_text(df, columns):
    all_texts = {}
    for col in columns:
        if col in df.columns:
            text = ' '.join(df[col].dropna().astype(str))
            if text:
                all_texts[col] = text
            else:
                print(f'No text found in column: {col}')
    combined_text = ' '.join(all_texts.values())
    return combined_text

# Lista de palabras a excluir en la nube de palabras
stopwords = set(STOPWORDS).union({'id', 'movie', 'film', 'data', 'name'})  # Puedes agregar más palabras si es necesario

# Función para generar y mostrar la nube de palabras
def generate_wordcloud(text, title, stopwords):
    if text.strip():  # Verificar que el texto no esté vacío
        wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.show()
    else:
        print(f'No se puede generar la nube de palabras para {title} porque el texto está vacío.')

# Generar y mostrar la nube de palabras para cada DataFrame
for df_name, columns in text_columns.items():
    df = globals()[df_name]
    combined_text = get_combined_text(df, columns)
    generate_wordcloud(combined_text, f'Nube de Palabras para {df_name}', stopwords)
