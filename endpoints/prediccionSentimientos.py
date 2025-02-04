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


# Cargar modelo y tokenizer
MODEL_NAME = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()  # Modo evaluación

# Verificar si hay GPU disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"✅ Usando dispositivo: {device}")

# Ver cuántas etiquetas tiene el modelo
num_labels = model.config.num_labels
print(f"El modelo tiene {num_labels} etiquetas.")

# Diccionario corregido con las 5 etiquetas del modelo
label_map = {
    0: "Muy Negativo",
    1: "Negativo",
    2: "Neutro",
    3: "Positivo",
    4: "Muy Positivo"
}

def predict_sentiment(comment):
    inputs = tokenizer(comment, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Obtener la predicción
    label = torch.argmax(outputs.logits, dim=-1).item()
    
    return label_map[label]  # Solo devolver la etiqueta, no el array de probabilidades
