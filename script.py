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
    ffmpeg_path = "ruta-absoluta-a-ffmpeg.exe"

# Ruta de la carpeta donde deseas guardar las canciones
DEFAULT_OUTPUT_DIR = "./canciones"

# Solicitar al usuario que ingrese el client_id y el client_secret
client_id = input("Ingrese el CLIENT_ID (presione Enter para usar el predeterminado)")
client_secret = input("Ingrese el CLIENT_SECRET (presione Enter para usar el predeterminado)")
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

# Autenticación en Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

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
    except Exception as e:
        print(f"Error al descargar {song_name}: {e}")

# Obtener datos de la playlist
playlist = sp.playlist(playlist_id)

# Descargar cada canción de la playlist
for item in playlist['tracks']['items']:
    track = item['track']
    song_name = f"{track['name']} - {track['artists'][0]['name']}"
    file_path = os.path.join(output_dir, f"{song_name}.mp3")
    if os.path.isfile(file_path):
        print(f"{song_name} ya está descargada.")
    else:
        print(f"Descargando: {song_name}")
        download_song_from_youtube(song_name)