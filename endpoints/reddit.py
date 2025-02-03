import requests
import pandas as pd
import time

def buscarComentarios(query):
    # Pedir al usuario el tema a buscar
    query.replace(" ", "+")

    # URL de búsqueda en Reddit
    search_url = f"https://www.reddit.com/search.json?q={query}&limit=10"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Realizar la solicitud y obtener los posts en formato JSON
    response = requests.get(search_url, headers=headers)
    posts = response.json().get("data", {}).get("children", [])

    # Obtener los enlaces de los posts
    post_links = [f"https://www.reddit.com{post['data']['permalink']}" for post in posts]

    # Lista para almacenar los comentarios
    comments_data = []

    # Recorrer cada post y extraer comentarios
    for post_url in post_links:
        json_url = post_url + ".json"  # Obtener los comentarios en formato JSON
        time.sleep(1)  # Evita ser bloqueado por Reddit
        response = requests.get(json_url, headers=headers)
        
        if response.status_code == 200:
            post_data = response.json()
            
            if len(post_data) > 1:
                comments = post_data[1].get("data", {}).get("children", [])
                
                for comment in comments:
                    body = comment["data"].get("body", "").strip()
                    if body and body.lower() != "[removed]" and body.lower() != "[deleted]":  # Evita comentarios eliminados
                        comments_data.append([body])

    # Guardar solo los comentarios en un archivo CSV
    df = pd.DataFrame(comments_data, columns=["Comentario"])
    df.to_csv("comentarios_reddit.csv", index=False, encoding="utf-8")

    print("\n✅ Se han extraído", len(comments_data), "comentarios y guardado en 'comentarios_reddit.csv'.")
