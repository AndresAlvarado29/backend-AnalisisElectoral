import os
from apify_client import ApifyClient

# API Key de Apify (debe colocarse en variables de entorno por seguridad)
API_KEY_POSTS = os.getenv("APIFY_API_KEY", "apify_api_Ji1r9d7CypLVf9bORjfZMt9DUnDdvP0Hek8W")
API_KEY_COMMENTS = API_KEY_POSTS  # Se usa la misma API Key para comentarios

# Inicializar el cliente de Apify
client_posts = ApifyClient(API_KEY_POSTS)
client_comments = ApifyClient(API_KEY_COMMENTS)

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

    # Extraer los enlaces de los posts
    links = [item.get("link") for item in client_posts.dataset(run["defaultDatasetId"]).iterate_items() if item.get("link")]

    if not links:
        print("\n❌ No se encontraron posts.")
        return None

    return links

def extraer_comentarios(links):
    """
    Extrae comentarios de una lista de enlaces de posts.
    Devuelve solo los comentarios en una lista.
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

        # Extraer solo los comentarios sin información adicional
        for item in client_comments.dataset(run["defaultDatasetId"]).iterate_items():
            if "text" in item:
                comentarios_totales.append(item.get("text", ""))

    return comentarios_totales

def obtener_solo_comentarios_facebook(query):
    """
    Orquesta la búsqueda de posts y la extracción de solo los comentarios.
    Devuelve un JSON con una lista de comentarios.
    """
    links = buscar_posts(query)
    if not links:
        return {"error": "No se encontraron publicaciones en Facebook."}

    comentarios = extraer_comentarios(links)

    if not comentarios:
        return {"message": "No se encontraron comentarios en los posts de Facebook."}

    return {"comentarios": comentarios}
