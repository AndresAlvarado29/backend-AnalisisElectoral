import os
import csv
from googleapiclient.discovery import build
from youtube_comment_downloader import YoutubeCommentDownloader
import pandas as pd

# Configura tu API Key de YouTube en las variables de entorno
os.environ["YOUTUBE_API_KEY"] = "A"  # Reemplaza con tu clave de API

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
            videos.append({"title": video_title, "url": video_url})
        
        # Eliminar duplicados en la lista de videos
        videos_unicos = {v["url"]: v for v in videos}.values()
        return list(videos_unicos)

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

def guardar_comentarios_csv(query, comentarios):
    """
    Guarda una lista de comentarios en un archivo CSV.
    """
    filename = f"comentarios_{query.replace(' ', '_')}.csv"
    try:
        # Guardar solo los comentarios (sin video_title)
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["comentario"])  # Encabezado
            for comentario in comentarios:
                writer.writerow([comentario])  # Solo guardar el texto del comentario
        print(f"Comentarios guardados en el archivo: {filename}")
    except Exception as e:
        print(f"Error al guardar comentarios en CSV: {e}")

if __name__ == "__main__":
    # Solicitar término de búsqueda
    termino_busqueda = input("Ingrese el término de búsqueda: ")

    # Buscar videos
    videos = buscar_videos(termino_busqueda)

    if videos:
        print("\nResultados de búsqueda:")
        for video in videos:
            print(f"Título: {video['title']}\nURL: {video['url']}\n")

        # Descargar comentarios de cada video
        todos_comentarios = []
        for video in videos:
            print(f"Descargando comentarios para: {video['title']}")
            comentarios = descargar_comentarios(video["url"].split('=')[-1], max_comentarios=10)
            todos_comentarios.extend(comentarios)

        # Guardar todos los comentarios en un archivo CSV
        guardar_comentarios_csv(termino_busqueda, todos_comentarios)
    else:
        print("No se encontraron videos para el término de búsqueda.")
