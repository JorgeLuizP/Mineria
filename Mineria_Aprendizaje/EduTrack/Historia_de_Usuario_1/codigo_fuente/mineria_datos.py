import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
import numpy as np

def obtener_datos():
    # Crear una instancia del motor SQLAlchemy
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost/learning_tracker')

    # Consulta SQL para obtener los datos de los estudiantes
    consulta = "SELECT id, name, age, average_grade, grade FROM students"

    # Obtener los datos de la base de datos en un DataFrame de pandas
    datos = pd.read_sql_query(consulta, engine)

    # Eliminar filas con valores no numéricos en la columna "average_grade"
    datos = datos[pd.to_numeric(datos['average_grade'], errors='coerce').notnull()]

    # Inspeccionar las filas con valores no numéricos en todas las columnas
    filas_no_numericas = datos.loc[~pd.to_numeric(datos['id'], errors='coerce').notnull() |
                                   ~pd.to_numeric(datos['name'], errors='coerce').notnull() |
                                   ~pd.to_numeric(datos['age'], errors='coerce').notnull()]
    if not filas_no_numericas.empty:
        print("Filas con valores no numéricos:")
        print(filas_no_numericas)

    # Hacer una copia de los datos antes de eliminar las columnas
    datos_copia = datos.copy()

    # Eliminar las columnas "id" y "name" del conjunto de características (X)
    X = datos_copia.drop(["id", "name"], axis=1)

    # Separar las características (X) de las etiquetas (y)
    y = X.pop("average_grade").astype(float)  # Convertir los valores a tipo float

    # Obtener las columnas obtenidas
    columnas_obtenidas = ["id", "name", "age", "grade", "average_grade"]

    # Devolver las características, las etiquetas y las columnas obtenidas
    return X, y, columnas_obtenidas


def dividir_datos_entrenamiento_prueba(X, y):
    # Dividir los datos en entrenamiento y prueba
    X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas
