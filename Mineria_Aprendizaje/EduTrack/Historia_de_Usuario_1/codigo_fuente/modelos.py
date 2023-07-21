from sklearn.ensemble import RandomForestRegressor

def entrenar_modelo(X, y):
    # Crear el modelo de regresión de bosque aleatorio
    modelo = RandomForestRegressor()

    # Entrenar el modelo
    modelo.fit(X, y)

    return modelo

def predecir(modelo, X):
    # Realizar predicciones con el modelo
    y_predicciones = modelo.predict(X)

    # Devolver las predicciones
    return y_predicciones

def evaluar_modelo(modelo, X, y):
    # Evaluar el rendimiento del modelo en los datos de prueba
    puntaje = modelo.score(X, y)

    # Devolver el puntaje de evaluación
    return puntaje
