# API Music Preferences App

Este proyecto es una API REST construida con **FastAPI** que permite a los usuarios gestionar sus preferencias musicales. Incluye funcionalidades para interactuar con una base de datos SQLite y conectarse a la API de Spotify.

## Características

### Usuarios
- **Crear usuario**: Añade un nuevo usuario.
- **Consultar usuarios**: Obtiene todos los usuarios.
- **Actualizar usuario**: Modifica los datos de un usuario existente.
- **Eliminar usuario**: Elimina un usuario y sus preferencias asociadas.

### Preferencias musicales
- **Artistas favoritos**:
  - Añadir un artista a la lista de favoritos de un usuario.
  - Eliminar un artista de la lista de favoritos de un usuario.
  - Consultar artistas favoritos de un usuario.
- **Pistas favoritas**:
  - Añadir una pista a la lista de favoritos de un usuario.
  - Eliminar una pista de la lista de favoritos de un usuario.
  - Consultar pistas favoritas de un usuario.

### Conexión con Spotify
- **Buscar artista por nombre**: Recupera datos de Spotify sobre un artista específico.
- **Buscar pista por nombre**: Recupera datos de Spotify sobre una pista específica, con la opción de filtrar por nombre de artista.

## Configuración

### Requisitos previos
- Python 3.8+
- FastAPI
- Uvicorn (para ejecutar el servidor)
- Spotify API Client ID y Client Secret

### Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/DanielCaldes/APIs-REST.git
   cd APIs-REST
   ```

2. Crea y activa el entorno virtual (ejemplo con conda):

   ```bash
   conda create --name nombre_del_entorno python=3.x
   conda activate nombre_del_entorno
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tus credenciales de Spotify en un archivo `.env`:
   ```env
   CLIENT_ID="tu_cliente_id"
   CLIENT_SECRET="tu_cliente_secreto"
   ```

### Ejecución

1. Inicia el servidor de FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

2. Accede a la documentación interactiva de la API en Swagger:
   http://127.0.0.1:8000/docs

## Endpoints


### 1. Crear un usuario

- **Método**: POST /api/create_user
- **Descripción**: Crea un nuevo usuario y lo agrega a la base de datos.
- **Cuerpo de la solicitud** (JSON):
  ```json
  {
    "username": "nombre"
  }
- **Respuesta**:
  ```json
  {
    "id": 1
  }
  ```


### 2. Obtener todos los usuarios

- **Método**: GET /api/users
- **Descripción**: Obtiene una lista de todos los usuarios registrados.
- **Respuesta**:
  ```json  
  [
    {
      "id": 1,
      "username": "nombre"
    },
    {
      "id": 2,
      "username": "otro_nombre"
    }
  ]
  ```


### 3. Actualizar un usuario

- **Método**: PUT /api/update_user/{id}
- **Descripción**: Actualiza la información de un usuario existente.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "username": "nuevo_nombre"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "User updated successfully"
  }
  ```


### 4. Eliminar un usuario

- **Método**: DELETE /api/delete_user/{id}
- **Descripción**: Elimina un usuario de la base de datos por su ID.
- **Respuesta**:
  ```json  
  {
    "message": "User with id {id} deleted successfully."
  }
  ```


### 5. Agregar un artista favorito

- **Método**: POST /api/add_favourite_artist
- **Descripción**: Agrega un artista a los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "user_id": 1,
    "artist_id": "0TnOYISbd1XYRBk9myaseg"
  }
- Respuesta:
  {
    "message": "Insert successful!"
  }
  ```


### 6. Eliminar un artista favorito

- **Método**: DELETE /api/remove_favourite_artist
- **Descripción**: Elimina un artista de los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "user_id": 1,
    "artist_id": "0TnOYISbd1XYRBk9myaseg"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "Artist preference removed!"
  }
  ```


### 7. Obtener artistas favoritos de un usuario

- **Método**: GET /api/get_favourites_artists/{id}
- **Descripción**: Obtiene una lista de los artistas favoritos de un usuario por su ID.
- **Respuesta**:
  ```json  
  [
    {
      "name": "Pitbull",
      "id": "0TnOYISbd1XYRBk9myaseg",
      "uri": "spotify:artist:0TnOYISbd1XYRBk9myaseg"
    }
  ]
  ```


### 8. Agregar una canción favorita

- **Método**: POST /api/add_favourite_track
- **Descripción**: Agrega una canción a los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "user_id": 1,
    "track_id": "11dFghVXANMlKmJXsNCbNl"
  }
- Respuesta:
  {
    "message": "Insert successful!"
  }
  ```


### 9. Eliminar una canción favorita

- **Método**: DELETE /api/remove_favourite_track
- **Descripción**: Elimina una canción de los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "user_id": 1,
    "artist_id": "11dFghVXANMlKmJXsNCbNl"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "Track preference removed!"
  }
  ```


### 10. Obtener canciones favoritas de un usuario

- **Método**: GET /api/get_favourites_tracks/{id}
- **Descripción**: Obtiene una lista de las canciones favoritas de un usuario por su ID.
- **Respuesta**:
  ```json  
  [
    {
      "name": "Pitbull",
      "id": "0TnOYISbd1XYRBk9myaseg",
      "uri": "spotify:artist:0TnOYISbd1XYRBk9myaseg"
    }
  ]
  ```

### 11. Buscar una canción en Spotify

- **Método**: GET /api/spotify_artist/{artist_name}
- **Descripción**: Busca información de un artista en Spotify.
- **Respuesta**:
  ```json  
  {
    "name": "Pitbull",
    "id": "0TnOYISbd1XYRBk9myaseg",
    "uri": "spotify:artist:0TnOYISbd1XYRBk9myaseg"
  }
  ```


## Notas adicionales

- Para interactuar con Spotify, asegúrate de que las credenciales (CLIENT_ID y CLIENT_SECRET) sean válidas.
- El archivo de base de datos `music_app.db` se crea automáticamente en la raíz del proyecto.
- El endpoint `/api/get_favourites_artists/{id}` devuelve información completa sobre los artistas favoritos utilizando la API de Spotify.
