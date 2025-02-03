from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Ruta del modelo entrenado
model_path = "./modeloIA/modelo_sentimiento"

# Cargar el tokenizador y el modelo
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Mover el modelo a la GPU si está disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predecir_sentimiento(texto):
    # Tokenizar el texto
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Mover los tensores a la GPU si está disponible
    inputs = {key: val.to(device) for key, val in inputs.items()}

    # Hacer la predicción
    with torch.no_grad():
        outputs = model(**inputs)

    # Obtener la clase con mayor probabilidad
    logits = outputs.logits
    prediccion = torch.argmax(logits, dim=-1).item()

    # Mapeo de etiquetas (ajustar según las clases usadas en tu entrenamiento)
    etiquetas = {0: "Negativo", 1: "Neutro", 2: "Positivo"}
    
    return etiquetas[prediccion]

# Ejemplo de prueba
#texto_prueba = "Me encanta este candidato, sus ideas son muy innovadoras."
#resultado = predecir_sentimiento(texto_prueba)
#print(f"Sentimiento: {resultado}")
