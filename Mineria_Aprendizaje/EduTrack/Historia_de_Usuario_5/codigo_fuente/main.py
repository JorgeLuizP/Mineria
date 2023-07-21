# main.py
from mineria_datos import obtener_datos, dividir_datos_entrenamiento_prueba
from modelos import entrenar_modelo, predecir, evaluar_modelo

# Obtener los datos
X, y, _ = obtener_datos()

# Dividir los datos en conjuntos de entrenamiento y prueba
X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas = dividir_datos_entrenamiento_prueba(X, y)

# Entrenar el modelo
modelo = entrenar_modelo(X_entrenamiento, y_entrenamiento)

# Realizar predicciones en los datos de prueba
y_predicciones = predecir(modelo, X_pruebas)

# Evaluar el modelo
puntaje = evaluar_modelo(modelo, X_pruebas, y_pruebas)

print("Predicciones:", y_predicciones)
print("Puntaje de evaluación:", puntaje)
