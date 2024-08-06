# Spotify Playlist Downloader

Este script permite descargar canciones de una playlist de Spotify en formato MP3 utilizando `spotipy` para interactuar con la API de Spotify y `yt_dlp` para descargar las canciones desde YouTube.

## Requisitos

- Python 3.x
- `spotipy` (instalar con `pip install spotipy`)
- `yt_dlp` (instalar con `pip install yt-dlp`)
- `ffmpeg` (descargar desde [aquí](https://ffmpeg.org/download.html))

## Instalación

1. Clona este repositorio o descarga el archivo fuente.

2. Instala las dependencias necesarias ejecutando:
   ```sh
   pip install spotipy yt-dlp
   ```
3. Descarga ffmpeg desde [aquí](https://ffmpeg.org/download.html) y coloca ffmpeg.exe en una ubicación accesible. Anota la ruta completa a ffmpeg.exe.

## Uso

1. Abre el archivo del script y configura tus credenciales de Spotify:
   ```py
   DEFAULT_CLIENT_ID = 'tu-client-id'
   DEFAULT_CLIENT_SECRET = 'tu-client-secret'
   DEFAULT_PLAYLIST_ID = 'tu-playlist-id'
   ```
2. Proporciona la ruta a `ffmpeg.exe`:
   ```py
   ffmpeg_path = "ruta-absoluta-a-ffmpeg.exe"
   ```
3. Ejecuta el script:
   ```sh
   python script.py
   ```
4. Ingresa tus credenciales de Spotify y el ID de la playlist cuando se te solicite. Puedes presionar Enter para usar los valores predeterminados.
5. Las canciones se descargarán en la carpeta especificada (por defecto, `./canciones`).

## Notas
- Si el script se empaqueta con una herramienta como PyInstaller, `ffmpeg.exe` se debe incluir en el paquete, y el script debe ajustarse para localizar `ffmpeg.exe` en el directorio empaquetado.
  Ejecuta el siguiente código:
  ```sh
  pip install pyinstaller
  pyinstaller --onefile --add-binary "ruta-absoluta-a-ffmpeg.exe;." script.py
  ```
- Asegúrate de tener permisos de lectura en la playlist de Spotify que deseas descargar.
- Las canciones se buscarán y descargarán desde YouTube, por lo que puede haber variaciones en la calidad y precisión de los resultados.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
