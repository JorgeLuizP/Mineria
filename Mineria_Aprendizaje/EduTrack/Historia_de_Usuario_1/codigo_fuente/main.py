from mineria_datos import obtener_datos, dividir_datos_entrenamiento_prueba
from modelos import entrenar_modelo, predecir

# Obtener los datos
X, y, columnas_obtenidas = obtener_datos()

# Dividir los datos en entrenamiento y prueba
X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas = dividir_datos_entrenamiento_prueba(X, y)

# Entrenar el modelo
modelo = entrenar_modelo(X_entrenamiento, y_entrenamiento)

# Realizar predicciones
y_predicciones = predecir(modelo, X_pruebas)

# Imprimir las predicciones
print("Predicciones:", y_predicciones)
