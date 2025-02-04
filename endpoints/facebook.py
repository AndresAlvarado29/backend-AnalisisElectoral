from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Configuración de Selenium en Linux
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecuta en segundo plano
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--no-sandbox")  # Recomendado para evitar problemas de permisos en Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # Evita errores en entornos limitados como contenedores Docker

# Inicializar WebDriver sin Service
driver = webdriver.Chrome(options=chrome_options)

def login_facebook(email, password):
    driver.get("https://www.facebook.com")
    time.sleep(3)
    
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
    time.sleep(5)  # Espera que cargue la página principal

def buscar_publicaciones(palabra_clave):
    driver.get(f"https://www.facebook.com/search/posts?q={palabra_clave}")
    time.sleep(5)
    
    enlaces_publicaciones = []
    publicaciones = driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/')]")
    
    for publicacion in publicaciones[:5]:  # Extrae solo los primeros 5 enlaces
        link = publicacion.get_attribute("href")
        if link and link not in enlaces_publicaciones:
            enlaces_publicaciones.append(link)
    
    return enlaces_publicaciones

def extraer_comentarios(url):
    driver.get(url)
    time.sleep(10)  # Espera para cargar comentarios
    
    comentarios = []
    elementos_comentarios = driver.find_elements(By.XPATH, "//div[@aria-label='Comentario']")
    
    for comentario in elementos_comentarios:
        texto = comentario.text.strip()
        if texto:
            comentarios.append(texto)
    
    return comentarios

def obtener_comentarios_facebook(palabra_clave):
    email = "tu_email"
    password = "tu_contraseña"

    login_facebook(email, password)
    links = buscar_publicaciones(palabra_clave)

    todos_comentarios = []
    for link in links:
        comentarios = extraer_comentarios(link)
        todos_comentarios.extend(comentarios)

    return todos_comentarios
