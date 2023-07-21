# mineria_datos.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def obtener_datos():
    # Crear una instancia del motor SQLAlchemy
    engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')

    # Consulta SQL para obtener los datos de los estudiantes, calificaciones y materias
    consulta = """
    SELECT estudiantes.id, estudiantes.nombre, estudiantes.apellido, estudiantes.edad,
           estudiantes.codigo_estudiante, estudiantes.promedio, calificaciones.calificacion,
           materias.nombre AS materia
    FROM estudiantes
    INNER JOIN calificaciones ON estudiantes.id = calificaciones.id_estudiante
    INNER JOIN materias ON calificaciones.id_materia = materias.id
    """

    # Obtener los datos de la base de datos en un DataFrame de pandas
    datos = pd.read_sql_query(consulta, engine)

    # Separar las características (X) de las etiquetas (y)
    X = datos.drop(["promedio", "nombre", "apellido"], axis=1)  # Eliminar las columnas "nombre" y "apellido"
    y = datos["promedio"].astype(float)

    # Codificar la columna "materia" utilizando Label Encoding
    label_encoder = LabelEncoder()
    X["materia"] = label_encoder.fit_transform(X["materia"])

    # Obtener las columnas del DataFrame
    columnas_obtenidas = X.columns.tolist()

    # Devolver las características, las etiquetas y las columnas
    return X, y, columnas_obtenidas

def dividir_datos_entrenamiento_prueba(X, y, test_size=0.2, random_state=42):
    X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_entrenamiento, X_pruebas, y_entrenamiento, y_pruebas
