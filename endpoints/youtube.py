import os
import csv
from googleapiclient.discovery import build
from youtube_comment_downloader import YoutubeCommentDownloader

# Configura tu API Key de YouTube en las variables de entorno
os.environ["YOUTUBE_API_KEY"] = "AIzaSyBMGj5Rxu1G1yEp9flEsWx-Irfo0lJP_zo"  # Reemplaza con tu clave de API

def buscar_videos(query, max_results=5):
    """
    Busca videos en YouTube basados en un término de búsqueda y devuelve una lista de videos.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API Key en las variables de entorno. Configura 'YOUTUBE_API_KEY'.")

    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        # Realizar la búsqueda
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results
        )
        response = request.execute()

        # Procesar resultados
        videos = []
        for item in response.get("items", []):
            video_title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({"title": video_title, "url": video_url, "video_id": video_id})
        
        return videos

    except Exception as e:
        print(f"Ocurrió un error al realizar la búsqueda: {e}")
        return []

def descargar_comentarios(video_id, max_comentarios=10):
    """
    Descarga un número limitado de comentarios de un video dado su ID.
    """
    downloader = YoutubeCommentDownloader()
    comments = []

    try:
        for i, comment in enumerate(downloader.get_comments(video_id)):
            comments.append(comment["text"])
            if i + 1 >= max_comentarios:  # Limitar a max_comentarios
                break

        return comments

    except Exception as e:
        print(f"Ocurrió un error al descargar los comentarios del video {video_id}: {e}")
        return []

def obtener_videos_y_comentarios(query, max_results=5, max_comentarios=10):
    """
    Busca videos en YouTube y obtiene comentarios de cada uno.
    Devuelve un JSON con los títulos, URLs y comentarios.
    """
    videos = buscar_videos(query, max_results)

    if not videos:
        return {"error": "No se encontraron videos para la búsqueda."}

    resultados = []
    for video in videos:
        comentarios = descargar_comentarios(video["video_id"], max_comentarios)
        resultados.append({
            "titulo": video["title"],
            "url": video["url"],
            "comentarios": comentarios
        })

    return {"videos": resultados}
