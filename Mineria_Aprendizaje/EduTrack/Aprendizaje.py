import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import mysql.connector
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import mysql.connector
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import numpy as np

# Función para cargar los datos desde un archivo CSV
def cargar_datos():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            df.fillna(0, inplace=True)
            messagebox.showinfo("Información", "Datos cargados exitosamente")
            return df
        except Exception as e:
            messagebox.showerror("Error", str(e))
    return None

# Función para insertar datos en la tabla calificaciones
def insertar_datos():
    df = cargar_datos()
    if df is not None:
        try:
            # Configuración de la conexión a la base de datos
            config = {
                'user': 'root',
                'password': '123456',
                'host': 'localhost',
                'database': 'learning_tracker_final'
            }

            # Establecer la conexión
            connection = mysql.connector.connect(**config)

            # Crear el cursor
            cursor = connection.cursor()

            # Eliminar columnas no deseadas del DataFrame
            df.drop(['Nombre', 'Apellido', 'Numero_ID', 'Institucion', 'Departamento', 'Correo', 'ultima_descarga'], axis=1, inplace=True)

            # Convertir los valores de tipo numpy.int32 a float
            df = df.astype({'Total_Parcial_Final_Aprovechamiento': float, 'Cuestionario_Examen_Final': float, 'Total_Parcial_Final_Examen': float, 'Total_Parcial_Final': float, 'Total_Curso': float})

            # Insertar cada fila de datos en la tabla calificaciones
            for _, row in df.iterrows():
                values = tuple(row.values)
                column_names = ', '.join(row.index)  # Obtener los nombres de las columnas en el DataFrame
                placeholders = ', '.join(['%s'] * len(row))  # Crear los marcadores de posición para los valores
                query = f"INSERT INTO calificaciones ({column_names}) VALUES ({placeholders})"
                cursor.execute(query, values)

            # Confirmar los cambios en la base de datos
            connection.commit()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            connection.close()

            messagebox.showinfo("Información", "Datos insertados exitosamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))



# Función para realizar predicciones utilizando el modelo de minería de datos
def realizar_predicciones():
    try:
        # Configuración de la conexión a la base de datos
        config = {
            'user': 'root',
            'password': '123456',
            'host': 'localhost',
            'database': 'learning_tracker_final'
        }

        # Establecer la conexión
        connection = mysql.connector.connect(**config)

        # Crear el cursor
        cursor = connection.cursor()

        # Consulta SQL para obtener los datos de la tabla calificaciones
        query = "SELECT * FROM calificaciones"

        # Leer los datos de la base de datos en un DataFrame
        df = pd.read_sql(query, connection)

        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        connection.close()

        # Verificar si la columna 'total_curso' está presente
        if 'total_curso' in df.columns:
            # Eliminar columnas no deseadas
            columns_to_drop = ['Nombre', 'Apellido', 'Numero_ID', 'Institucion', 'Departamento', 'Correo', 'ultima_descarga']
            existing_columns = df.columns.tolist()
            columns_to_drop = [col for col in columns_to_drop if col in existing_columns]
            df.drop(columns_to_drop, axis=1, inplace=True)

            # Imputar los valores faltantes con la media
            df.fillna(df.mean(), inplace=True)

            # Dividir los datos en características (X) y etiquetas (y)
            X = df.drop('total_curso', axis=1)
            y = df['total_curso']

            # Dividir los datos en conjuntos de entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Crear y entrenar el modelo de regresión de árbol de decisión
            model = DecisionTreeRegressor()
            model.fit(X_train, y_train)

            # Realizar predicciones en el conjunto de prueba
            y_pred = model.predict(X_test)

            # Mostrar Mensaje de las predicciones realizadas
            prediction_message = f"Valores de las predicciones: {', '.join(map(str, y_pred))}"
            messagebox.showinfo("Predicciones", prediction_message)

            # Calcular el error cuadrático medio
            mse = mean_squared_error(y_test, y_pred)

            # Mostrar el error cuadrático medio
            messagebox.showinfo("Error Cuadrático Medio", f"El error cuadrático medio es: {mse}")

            # Obtener los índices de los registros insertados correspondientes al conjunto de prueba
            last_inserted_indices = X_test.index.tolist()

            # Crear una lista vacía para almacenar los valores de MSE
            mse_values = []

            # Realizar predicciones y calcular el MSE en cada iteración
            for i, index in enumerate(last_inserted_indices):
                if index <= len(df):
                    # Dividir los datos en características (X) y etiquetas (y) actualizados
                    X = df.drop('total_curso', axis=1)
                    y = df['total_curso']

                    # Dividir los datos en conjuntos de entrenamiento y prueba actualizados
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                    # Crear y entrenar el modelo de regresión de árbol de decisión actualizado
                    model = DecisionTreeRegressor()
                    model.fit(X_train, y_train)

                    # Realizar predicciones en el conjunto de prueba actualizado
                    y_pred = model.predict(X_test)

                    # Calcular el error cuadrático medio actualizado
                    mse = mean_squared_error(y_test, y_pred)

                    # Agregar el valor de MSE a la lista
                    mse_values.append(mse)

            # Graficar el MSE en función de las iteraciones
            iterations = np.arange(1, len(mse_values) + 1)
            plt.plot(iterations, mse_values, marker='o')
            plt.xlabel('Iteraciones')
            plt.ylabel('MSE')
            plt.title('Error Cuadrático Medio')
            plt.grid(True)
            plt.show()

        else:
            messagebox.showerror("Error", "La columna 'total_curso' no está presente en los datos.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# Crear la ventana principal
window = tk.Tk()

# Configurar la ventana principal
window.title("Sistema de Gestión de Calificaciones")
window.geometry("400x200")

insertar_button = tk.Button(window, text="Insertar Datos", command=insertar_datos)
insertar_button.pack(pady=10)

predecir_button = tk.Button(window, text="Realizar Predicciones", command=realizar_predicciones)
predecir_button.pack(pady=10)

# Iniciar el bucle principal de la aplicación
window.mainloop()
