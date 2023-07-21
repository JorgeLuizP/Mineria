import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import re
import shutil

# Función para convertir un archivo XLSX a CSV
def convertir_xlsx_a_csv(file_path, output_folder):
    try:
        # Leer el archivo XLSX en un DataFrame
        df = pd.read_excel(file_path)

        # Obtener el nombre base del archivo
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Crear la ruta de salida para el archivo CSV
        csv_file_path = os.path.join(output_folder, f"{file_name}.csv")

        # Guardar el DataFrame en formato CSV
        df.to_csv(csv_file_path, index=False)

        return csv_file_path
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir el archivo XLSX a CSV: {str(e)}")
        return None

def mapear_columnas(df):
    try:
        nuevo_esquema = {
            "Nombre": "Nombre",
            "Apellido(s)": "Apellido",
            "Número de ID": "Numero_ID",
            "Institución": "Institucion",
            "Departamento": "Departamento",
            "Dirección de correo": "Correo",
            "Total Parcial Final Aprovechamiento (Real)": "Total_Parcial_Final_Aprovechamiento",
            "Cuestionario:Examen Parcial Final (Real)": "Cuestionario_Examen_Final",
            "Total PF Examen (Real)": "Total_Parcial_Final_Examen",
            "Total Parcial Final (Real)": "Total_Parcial_Final",
            "Total del curso (Real)": "Total_Curso",
            "Última descarga de este curso": "ultima_descarga"
        }

        # Eliminar caracteres especiales y espacios en los nombres de columna
        nuevo_esquema = {k: re.sub(r"[^\w\s]+", "", v) for k, v in nuevo_esquema.items()}

        # Renombrar las columnas del DataFrame
        df.rename(columns=lambda x: buscar_correspondencia(x, nuevo_esquema), inplace=True)

        # Eliminar las columnas que no coinciden con el mapeo
        columnas_a_mantener = set(nuevo_esquema.values())
        columnas_actuales = set(df.columns)
        columnas_a_eliminar = columnas_actuales - columnas_a_mantener
        df.drop(columns=columnas_a_eliminar, inplace=True)

        # Reemplazar el signo "-" por 0 en las columnas que contienen valores numéricos
        df.replace("-", 0, regex=True, inplace=True)

        return df

    except Exception as e:
        messagebox.showerror("Error", f"Error al mapear las columnas: {str(e)}")
        return None
    
# Función para buscar la correspondencia de nombre de columna ignorando mayúsculas y espacios en blanco
def buscar_correspondencia(columna, nuevo_esquema):
    for key in nuevo_esquema.keys():
        if re.sub(r"\s+", "", columna.lower()) == re.sub(r"\s+", "", key.lower()):
            return nuevo_esquema[key]
    return columna

# Función para procesar un archivo XLSX y realizar el mapeo
def procesar_archivo_xlsx(file_path, output_folder):
    try:
        # Convertir el archivo XLSX a CSV
        csv_file_path = convertir_xlsx_a_csv(file_path, output_folder)

        if csv_file_path is not None:
            # Leer el archivo CSV en un DataFrame
            df = pd.read_csv(csv_file_path)

            # Mapear las columnas y mejorar el CSV
            df = mapear_columnas(df)

            # Guardar el DataFrame actualizado en el mismo archivo CSV
            df.to_csv(csv_file_path, index=False)

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el archivo CSV: {str(e)}")

# Función para procesar los archivos XLSX y realizar el mapeo
def procesar_archivos_xlsx(file_paths):
    # Obtener la ruta del directorio actual
    current_directory = os.getcwd()

    # Carpeta de salida para los archivos CSV convertidos
    output_folder = os.path.join(current_directory, "calificaciones")

    # Carpeta de salida para el primer archivo CSV
    entrenamiento_folder = os.path.join(current_directory, "entrenamiento")

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer los archivos XLSX
    for i, file_path in enumerate(file_paths):
        # Procesar el archivo XLSX y realizar el mapeo
        procesar_archivo_xlsx(file_path, output_folder)

        # Mover el primer archivo CSV al directorio "entrenamiento"
        if i == 0:
            if not os.path.exists(entrenamiento_folder):
                os.makedirs(entrenamiento_folder)
            shutil.move(
                os.path.join(output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}.csv"),
                os.path.join(entrenamiento_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}.csv")
            )

    # Mostrar mensaje de finalización
    messagebox.showinfo("Información", "Procesamiento de archivos completado")


# Función para manejar el evento de selección de archivos
def seleccionar_archivos():
    file_paths = filedialog.askopenfilenames(title="Seleccionar archivos XLSX", filetypes=(("Archivos XLSX", "*.xlsx"),))

    if file_paths:
        # Procesar los archivos XLSX y realizar el mapeo
        procesar_archivos_xlsx(file_paths)

# Crear la ventana principal de la interfaz gráfica
window = tk.Tk()
window.title("Conversión de archivos XLSX a CSV")
window.geometry("300x150")

# Etiqueta de instrucción
lbl_instrucciones = tk.Label(window, text="Seleccione los archivos XLSX:")
lbl_instrucciones.pack(pady=10)

# Botón de selección de archivos
btn_seleccionar_archivos = tk.Button(window, text="Seleccionar archivos", command=seleccionar_archivos)
btn_seleccionar_archivos.pack(pady=10)

# Ejecutar el bucle principal de la interfaz gráfica
window.mainloop()
