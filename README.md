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

### Usuarios
- **POST /api/create_user**: Crea un usuario nuevo.
- **GET /api/users**: Recupera la lista de usuarios.
- **PUT /api/update_user/{id}**: Actualiza los datos de un usuario.
- **DELETE /api/delete_user/{id}**: Elimina un usuario.

### Preferencias de artistas
- **POST /api/add_favourite_artist**: Añade un artista favorito.
- **DELETE /api/remove_favourite_artist**: Elimina un artista favorito.
- **GET /api/get_favourites_artists/{id}**: Consulta los artistas favoritos de un usuario.

### Preferencias de pistas
- **POST /api/add_favourite_track**: Añade una pista favorita.
- **DELETE /api/remove_favourite_track**: Elimina una pista favorita.
- **GET /api/get_favourites_tracks/{id}**: Consulta las pistas favoritas de un usuario.

### Spotify
- **GET /api/spotify_artist/{artist_name}**: Busca un artista por nombre en Spotify.
- **GET /api/spotify_track/{track_name}**: Busca una pista por nombre en Spotify (opcionalmente, filtra por artista).

## Notas adicionales

- Para interactuar con Spotify, asegúrate de que las credenciales (CLIENT_ID y CLIENT_SECRET) sean válidas.
- El archivo de base de datos `music_app.db` se crea automáticamente en la raíz del proyecto.
- El endpoint `/api/get_favourites_artists/{id}` devuelve información completa sobre los artistas favoritos utilizando la API de Spotify.
