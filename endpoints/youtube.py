import os
from googleapiclient.discovery import build
from youtube_comment_downloader import YoutubeCommentDownloader

# Configura tu API Key de YouTube en las variables de entorno
os.environ["YOUTUBE_API_KEY"] = "AIzaSyBMGj5Rxu1G1yEp9flEsWx-Irfo0lJP_zo"  # Reemplaza con tu clave de API

def buscar_videos(query, max_results=5):
    """
    Busca videos en YouTube y devuelve sus IDs.
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

        # Extraer solo los IDs de los videos
        video_ids = [item["id"]["videoId"] for item in response.get("items", [])]

        return video_ids

    except Exception as e:
        print(f"Ocurrió un error al realizar la búsqueda: {e}")
        return []

def descargar_comentarios(video_id, max_comentarios=10):
    """
    Descarga comentarios de un video dado su ID.
    """
    downloader = YoutubeCommentDownloader()
    comments = []

    try:
        for i, comment in enumerate(downloader.get_comments(video_id)):
            comments.append(comment["text"])
            if i + 1 >= max_comentarios:
                break

        return comments

    except Exception as e:
        print(f"Ocurrió un error al descargar los comentarios del video {video_id}: {e}")
        return []

def obtener_solo_comentarios(query, max_results=5, max_comentarios=10):
    """
    Busca videos en YouTube y obtiene solo los comentarios.
    Devuelve un JSON con una lista de comentarios.
    """
    video_ids = buscar_videos(query, max_results)

    if not video_ids:
        return {"error": "No se encontraron videos para la búsqueda."}

    comentarios_totales = []
    for video_id in video_ids:
        comentarios = descargar_comentarios(video_id, max_comentarios)
        comentarios_totales.extend(comentarios)

    return {"comentarios": comentarios_totales}
