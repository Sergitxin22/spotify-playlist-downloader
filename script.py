import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp

# Configuración de credenciales de Spotify
DEFAULT_CLIENT_ID = 'tu-client-id'
DEFAULT_CLIENT_SECRET = 'tu-client-secret'
DEFAULT_PLAYLIST_ID = 'tu-playlist-id'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

# Ruta a ffmpeg.exe empaquetado
if getattr(sys, 'frozen', False):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
else:
    ffmpeg_path = r"ruta-absoluta-a-ffmpeg.exe"

# Ruta de la carpeta donde deseas guardar las canciones
DEFAULT_OUTPUT_DIR = "./canciones"

# Asegurarse de que el directorio de salida exista
def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Carpeta creada: {directory}")

# Solicitar al usuario que ingrese el client_id y el client_secret
client_id = input("Ingrese el CLIENT_ID (presione Enter para usar el predeterminado): ")
client_secret = input("Ingrese el CLIENT_SECRET (presione Enter para usar el predeterminado): ")
playlist_id = input(f"Ingrese el ID de la playlist (presione Enter para usar el predeterminado '{DEFAULT_PLAYLIST_ID}'): ")
output_dir = input(f"Ingrese el nombre de la carpeta (presione Enter para usar el predeterminado '{DEFAULT_OUTPUT_DIR}'): ")

# Usar valores predeterminados si el usuario no ingresa nada
if not client_id:
    client_id = DEFAULT_CLIENT_ID
if not client_secret:
    client_secret = DEFAULT_CLIENT_SECRET
if not playlist_id:
    playlist_id = DEFAULT_PLAYLIST_ID
if not output_dir:
    output_dir = DEFAULT_OUTPUT_DIR

# Crear el directorio si no existe
ensure_dir_exists(output_dir)

# Autenticación en Spotify
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))
except spotipy.exceptions.SpotifyException as e:
    print(f"Error de autenticación: {e}")
    sys.exit(1)

# Función para buscar y descargar canciones desde YouTube
def download_song_from_youtube(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, f'{song_name}.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{song_name}"])
            return True
    except Exception as e:
        print(f"Error al descargar {song_name}: {e}")
        return False

# Obtener datos de la playlist con mejor manejo de errores
try:
    playlist = sp.playlist(playlist_id)
    print(f"Playlist encontrada: {playlist['name']} (por {playlist['owner']['display_name']})")
    print(f"Contiene {len(playlist['tracks']['items'])} canciones")
except spotipy.exceptions.SpotifyException as e:
    if "404" in str(e):
        print(f"Error: No se pudo encontrar la playlist con ID '{playlist_id}'.")
        print("Verifique que el ID sea correcto y que la playlist sea pública o que tenga permisos para acceder a ella.")
    else:
        print(f"Error al acceder a la playlist: {e}")
    sys.exit(1)

# Descargar cada canción de la playlist
successful_downloads = 0
failed_downloads = 0

print("\nIniciando descarga de canciones...")
for item in playlist['tracks']['items']:
    try:
        track = item['track']
        if track is None:
            continue
            
        song_name = f"{track['name']} - {track['artists'][0]['name']}"
        # Eliminar caracteres no permitidos en nombres de archivo
        safe_song_name = "".join([c for c in song_name if c.isalpha() or c.isdigit() or c in " -_().[]{}"])
        
        file_path = os.path.join(output_dir, f"{safe_song_name}.mp3")
        if os.path.isfile(file_path):
            print(f"✓ {song_name} ya está descargada.")
            successful_downloads += 1
        else:
            print(f"Descargando: {song_name}")
            if download_song_from_youtube(song_name):
                successful_downloads += 1
            else:
                failed_downloads += 1
    except Exception as e:
        print(f"Error procesando pista: {e}")
        failed_downloads += 1

# Mostrar resumen al finalizar
print("\n--- Resumen de descargas ---")
print(f"Canciones descargadas correctamente: {successful_downloads}")
if failed_downloads > 0:
    print(f"Canciones con error: {failed_downloads}")
print(f"Las canciones se guardaron en: {os.path.abspath(output_dir)}")