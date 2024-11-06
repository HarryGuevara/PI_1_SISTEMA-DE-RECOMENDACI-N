
markdown
 FastAPI Movie Data API

Esta es una API construida con FastAPI que proporciona información sobre películas, actores, directores y sus estadísticas. La API está conectada a un conjunto de datos que incluye información sobre las películas, sus cast y crew, permitiendo consultas específicas como el número de películas estrenadas en un mes, el score de una película, y más.

 Requisitos

Para ejecutar esta API, asegúrate de tener instalado lo siguiente:

Python 3.7+
FastAPI
Uvicorn
Pandas
Pydantic

Puedes instalar las dependencias ejecutando:

bash
pip install fastapi uvicorn pandas pydantic


 Archivos de Datos

La API utiliza tres archivos CSV que contienen información de películas, actores y directores:

1. cast_cleaned.csv: Información sobre los actores y las películas en las que han participado.
2. crew_cleaned.csv: Información sobre los directores y los miembros del equipo de cada película.
3. df_movie_progress.csv: Datos de las películas, incluyendo título, fecha de estreno, votos, ingresos y presupuesto.

Estos archivos deben estar ubicados en las siguientes rutas (o personalizarse según tu entorno):

- cast_df: C:/path/to/cast_cleaned.csv
- crew_df: C:/path/to/crew_cleaned.csv
- movie_df: C:/path/to/df_movie_progress.csv

 Endpoints

1. /cantidad_filmaciones_mes/{mes}
Descripción: Devuelve el número de películas estrenadas en un mes específico.

Método: GET

Parámetro:
- mes (str): El mes para consultar las películas estrenadas.

Ejemplo:
bash
GET /cantidad_filmaciones_mes/enero


Respuesta:
json
{
  "mes": "enero",
  "cantidad": 10
}


2. /cantidad_filmaciones_dia/{dia}
Descripción: Devuelve la cantidad de películas estrenadas en un día específico.

Método: GET

Parámetro:
- dia (str): El día para consultar las películas estrenadas.

Ejemplo:
bash
GET /cantidad_filmaciones_dia/2024-01-01


Respuesta:
json
{
  "dia": "2024-01-01",
  "cantidad": 2
}


3. /score_titulo/{titulo_de_la_filmacion}
Descripción: Retorna el título, año de estreno y score de la película especificada.

Método: GET

Parámetro:
- titulo_de_la_filmacion (str): El título de la película para obtener la información.

Ejemplo:
bash
GET /score_titulo/Inception


Respuesta:
json
{
  "titulo": "Inception",
  "año_estreno": "2010",
  "score": 8.8
}


4. /votos_titulo/{titulo_de_la_filmacion}
Descripción: Devuelve el título, cantidad de votos y promedio de votación si supera los 2000 votos. Si no, muestra un mensaje de aviso.

Método: GET

Parámetro:
- titulo_de_la_filmacion (str): El título de la película.

Ejemplo:
bash
GET /votos_titulo/Inception


Respuesta:
json
{
  "titulo": "Inception",
  "cantidad_votos": 3000,
  "promedio_voto": 8.8
}


5. /get_actor/{nombre_actor}
Descripción: Devuelve el éxito promedio del actor basado en el retorno promedio y la cantidad de películas en las que ha participado.

Método: GET

Parámetro:
- nombre_actor (str): El nombre del actor.

Ejemplo:
bash
GET /get_actor/Leonardo DiCaprio


Respuesta:
json
{
  "actor": "Leonardo DiCaprio",
  "exito_promedio": 200000000,
  "cantidad_peliculas": 10
}


6. /get_director/{nombre_director}
Descripción: Devuelve el éxito del director junto con información sobre cada película que ha dirigido (nombre, fecha de lanzamiento, retorno, costo, ganancia).

Método: GET

Parámetro:
- nombre_director (str): El nombre del director.

Ejemplo:
bash
GET /get_director/Christopher Nolan


Respuesta:
json
{
  "director": "Christopher Nolan",
  "exito_promedio": 250000000,
  "peliculas": [
    {
      "title": "Inception",
      "release_date": "2010-07-16",
      "revenue": 829895144,
      "budget": 160000000,
      "ganancia": 669895144
    },
    {
      "title": "Interstellar",
      "release_date": "2014-11-07",
      "revenue": 677471339,
      "budget": 165000000,
      "ganancia": 512471339
    }
  ]
}


 Iniciar el servidor

Para iniciar el servidor FastAPI, corre el siguiente comando:

bash
uvicorn main:app --reload


Esto iniciará el servidor en http://127.0.0.1:8000.

 Pruebas

Puedes probar los endpoints utilizando herramientas como Postman o curl. Asegúrate de tener los datos correctamente cargados en las rutas especificadas para que la API funcione correctamente.

Ejemplo con curl:

bash
curl -X 'GET' 'http://127.0.0.1:8000/cantidad_filmaciones_mes/enero' -H 'accept: application/json'


 Contribuciones

Si deseas contribuir al proyecto, siéntete libre de hacer un fork del repositorio y enviar un pull request.

 Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.


Explicación del archivo README.md:

1. Requisitos: Instrucciones para instalar las dependencias necesarias para correr la API.
2. Archivos de Datos: Detalles sobre los archivos CSV que utiliza la API.
3. Endpoints: Descripción de cada endpoint, cómo se utilizan y ejemplos de respuesta.
4. Iniciar el servidor: Cómo iniciar el servidor FastAPI.
5. Pruebas: Métodos para probar los endpoints usando herramientas como curl o Postman.
6. Contribuciones y Licencia: Sección para cualquier contribución y la licencia del proyecto.

Este README.md proporcionará a cualquier usuario la información necesaria para entender, instalar y probar la API de manera efectiva.