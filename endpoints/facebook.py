import csv
import os
import pandas as pd
from apify_client import ApifyClient

# API Key de Apify (debe colocarse en variables de entorno por seguridad)
API_KEY_POSTS = os.getenv("APIFY_API_KEY", "apify_a")
API_KEY_COMMENTS = API_KEY_POSTS  # Se usa la misma API Key para comentarios

# Inicializar el cliente de Apify
client_posts = ApifyClient(API_KEY_POSTS)
client_comments = ApifyClient(API_KEY_COMMENTS)

# Nombre del archivo donde se guardarán todos los comentarios
ARCHIVO_CSV = "facebook_comentarios.csv"

def buscar_posts(nombre):
    """
    Busca publicaciones en Facebook relacionadas con un término dado.
    Devuelve una lista de enlaces de los posts encontrados.
    """
    print(f"\n🔍 Buscando posts en Facebook sobre: {nombre}...\n")

    # Configurar búsqueda de posts
    run_input = {
        "searchQuery": nombre,
        "maxPosts": 3,  # Número de posts a buscar
    }

    # Ejecutar el actor de Apify para buscar posts
    run = client_posts.actor("4YfcIWyRtJHJ5Ha3a").call(run_input=run_input)

    # Lista para almacenar los enlaces de posts encontrados
    links = []

    print("📌 Posts encontrados:")
    for item in client_posts.dataset(run["defaultDatasetId"]).iterate_items():
        link = item.get("link")
        if link:
            links.append(link)
            print(link)  # Mostrar los enlaces encontrados

    if not links:
        print("\n❌ No se encontraron posts.")
        return None

    return links

def extraer_comentarios(links):
    """
    Extrae comentarios de una lista de enlaces de posts.
    Devuelve una lista de comentarios junto con sus enlaces.
    """
    comentarios_totales = []

    for link in links:
        print(f"\n💬 Extrayendo comentarios del post: {link}\n")

        # Configuración del actor para extraer comentarios
        run_input = {
            "startUrls": [{"url": link}],
            "resultsLimit": 10,  # Limitar la cantidad de comentarios a extraer
        }

        # Ejecutar el actor de Apify para extraer comentarios
        run = client_comments.actor("apify/facebook-comments-scraper").call(run_input=run_input)

        # Lista para almacenar los comentarios extraídos de este post
        for item in client_comments.dataset(run["defaultDatasetId"]).iterate_items():
            if "text" in item:
                comentarios_totales.append({"post": link, "comentario": item.get("text", "")})

    return comentarios_totales

def guardar_comentarios_csv(comentarios):
    """
    Guarda todos los comentarios extraídos en un único archivo CSV.
    """
    df_final = pd.DataFrame(comentarios)

    if os.path.exists(ARCHIVO_CSV):
        df_existente = pd.read_csv(ARCHIVO_CSV, encoding="utf-8-sig")
        df_final = pd.concat([df_existente, df_final], ignore_index=True)

    df_final.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8-sig")
    print(f"\n✅ Todos los comentarios han sido guardados en '{ARCHIVO_CSV}'.\n")

def obtener_comentarios_facebook(query):
    """
    Orquesta la búsqueda de posts y la extracción de comentarios.
    """
    links = buscar_posts(query)
    if not links:
        return {"error": "No se encontraron publicaciones en Facebook."}

    comentarios = extraer_comentarios(links)

    if comentarios:
        guardar_comentarios_csv(comentarios)
    else:
        print("\n❌ No se encontraron comentarios en los posts.")

    return {"comentarios": comentarios}
