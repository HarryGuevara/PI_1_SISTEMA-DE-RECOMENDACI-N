import pandas as pd
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import requests
from io import StringIO

# URL base de tu repositorio GitHub
BASE_URL = "https://raw.githubusercontent.com/HarryGuevara/my_recommendation_project/main/data/CSV/"

# Función para cargar los CSV desde GitHub con optimización de memoria
def load_csv_from_github(filename: str, usecols=None, sample_frac=1.0) -> pd.DataFrame:
    url = BASE_URL + filename
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error si no se puede cargar el archivo
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data, usecols=usecols)
    if sample_frac < 1.0:  # Reducir filas si se especifica
        df = df.sample(frac=sample_frac, random_state=42)
    return df

# Cargar los datos con optimización
cast_df = load_csv_from_github(
    'cast_desanidado.csv', 
    usecols=['actor_id', 'actor_name', 'movie_id'], 
    sample_frac=0.5  # Carga el 50% de los datos para optimizar
)
crew_df = load_csv_from_github(
    'crew_desanidado.csv', 
    usecols=['crew_id', 'job', 'movie_id', 'director_name'], 
    sample_frac=0.5
)
movie_df = load_csv_from_github(
    'movies_datasetc.csv', 
    usecols=['id', 'title', 'release_date', 'vote_average', 'vote_count', 'revenue', 'budget', 'genre'], 
    sample_frac=0.5
)

# Optimizar tipos de datos
cast_df['actor_id'] = cast_df['actor_id'].astype('int32')
cast_df['movie_id'] = cast_df['movie_id'].astype('int32')
crew_df['crew_id'] = crew_df['crew_id'].astype('int32')
crew_df['movie_id'] = crew_df['movie_id'].astype('int32')
movie_df['id'] = movie_df['id'].astype('int32')
movie_df['vote_count'] = movie_df['vote_count'].astype('int32')
movie_df['revenue'] = movie_df['revenue'].astype('float32')
movie_df['budget'] = movie_df['budget'].astype('float32')

# Inicializar la aplicación FastAPI
app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    mes_df = movie_df[movie_df['release_date'].str.contains(mes, case=False, na=False)]
    return {"mes": mes, "cantidad": len(mes_df)}

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    dia_df = movie_df[movie_df['release_date'].str.contains(dia, case=False, na=False)]
    return {"dia": dia, "cantidad": len(dia_df)}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    pelicula = movie_df[movie_df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"mensaje": "Película no encontrada"}
    return {
        "titulo": pelicula.iloc[0]['title'],
        "año_estreno": pelicula.iloc[0]['release_date'][:4],
        "score": pelicula.iloc[0]['vote_average']
    }

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = movie_df[movie_df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"mensaje": "Película no encontrada"}
    votos = pelicula.iloc[0]['vote_count']
    if votos > 2000:
        return {
            "titulo": pelicula.iloc[0]['title'],
            "cantidad_votos": votos,
            "promedio_voto": pelicula.iloc[0]['vote_average']
        }
    else:
        return {"mensaje": "La película tiene menos de 2000 votos."}

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    actor_df = cast_df[cast_df['actor_name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_df.empty:
        return {"mensaje": "Actor no encontrado"}
    peliculas_actor = actor_df.merge(movie_df, left_on='movie_id', right_on='id')
    exito_promedio = peliculas_actor['revenue'].mean()
    cantidad_peliculas = len(peliculas_actor)
    return {
        "actor": nombre_actor,
        "exito_promedio": exito_promedio,
        "cantidad_peliculas": cantidad_peliculas
    }

@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    director_df = crew_df[crew_df['director_name'].str.contains(nombre_director, case=False, na=False)]
    if director_df.empty:
        return {"mensaje": "Director no encontrado"}
    peliculas_director = director_df.merge(movie_df, left_on='movie_id', right_on='id')
    peliculas_info = peliculas_director[['title', 'release_date', 'revenue', 'budget']]
    peliculas_info['ganancia'] = peliculas_info['revenue'] - peliculas_info['budget']
    exito_promedio = peliculas_info['ganancia'].mean()
    return {
        "director": nombre_director,
        "exito_promedio": exito_promedio,
        "peliculas": peliculas_info.to_dict(orient='records')
    }
