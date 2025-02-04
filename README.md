### 🔹 Candidatos
| Método  | Endpoint                            | Descripción                     |
|---------|-------------------------------------|---------------------------------|
| **POST**   | `/candidatos`                        | Crear un nuevo candidato.        |
| **GET**    | `/candidatos`                        | Obtener la lista de candidatos.  |
| **GET**    | `/candidatos/<int:id>`              | Obtener un candidato por ID.     |
| **GET**    | `/candidatos/nombre/<string:nombre>` | Obtener un candidato por nombre. |
| **DELETE** | `/candidatos/<int:id>`              | Eliminar un candidato por ID.    |

---

### 🔹 Redes Sociales
| Método  | Endpoint                                    | Descripción                      |
|---------|---------------------------------------------|----------------------------------|
| **POST**   | `/redes_sociales`                            | Crear una nueva red social.      |
| **GET**    | `/redes_sociales`                            | Obtener la lista de redes sociales. |
| **GET**    | `/redes_sociales/<int:id>`                  | Obtener una red social por ID.   |
| **GET**    | `/redes_sociales/nombre/<string:nombre>`    | Obtener una red social por nombre. |

---

### 🔹 Consultas
| Método  | Endpoint                   | Descripción                     |
|---------|----------------------------|---------------------------------|
| **POST**   | `/consultas`                  | Crear una nueva consulta.       |
| **GET**    | `/consultas`                  | Obtener la lista de consultas.  |
| **DELETE** | `/consultas/<int:id>`         | Eliminar una consulta por ID.   |

---

### 🔹 Búsqueda de Comentarios en Redes Sociales
| Método  | Endpoint                            | Descripción                                      |
|---------|-------------------------------------|--------------------------------------------------|
| **POST**   | `/api/facebook_comments`          | Buscar publicaciones en Facebook y extraer comentarios. |
| **GET**    | `/api/buscar_reddit?query=<palabra_clave>` | Buscar comentarios en Reddit.  |
| **GET**    | `/api/buscar_youtube?query=<palabra_clave>` | Buscar videos en YouTube y extraer comentarios. |

---

### 🔹 Predicción de Sentimientos
| Método  | Endpoint                             | Descripción                                       |
|---------|--------------------------------------|---------------------------------------------------|
| **POST**   | `/api/predecir_sentimiento`        | Analiza el sentimiento de un conjunto de comentarios. |
| **POST**   | `/api/predecir_sentimiento2`       | Analiza sentimientos con una clasificación más detallada. |

