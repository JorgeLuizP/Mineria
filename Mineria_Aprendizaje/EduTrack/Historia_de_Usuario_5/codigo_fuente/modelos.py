# modelos.py
from sklearn.tree import DecisionTreeRegressor

def entrenar_modelo(X, y):
    # Crear el modelo de regresión
    modelo = DecisionTreeRegressor()

    # Entrenar el modelo
    modelo.fit(X, y)

    # Devolver el modelo entrenado
    return modelo

def predecir(modelo, X):
    # Realizar predicciones con el modelo
    y_predicciones = modelo.predict(X)

    # Devolver las predicciones
    return y_predicciones

def evaluar_modelo(modelo, X, y):
    # Calcular el puntaje de evaluación del modelo
    puntaje = modelo.score(X, y)

    # Devolver el puntaje de evaluación
    return puntaje
