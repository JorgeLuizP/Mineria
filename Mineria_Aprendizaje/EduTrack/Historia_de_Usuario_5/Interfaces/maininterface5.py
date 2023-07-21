import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import tkinter.messagebox as messagebox

# Conexión a la base de datos
engine = create_engine('mysql+mysqlconnector://root:123456@localhost/learning_tracker_h2')
Session = sessionmaker(bind=engine)
session = Session()

# Definición de la clase Estudiante
Base = declarative_base()

class Estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    edad = Column(Integer)
    codigo_estudiante = Column(String(10))
    promedio = Column(Float)

# Creación de la ventana principal
root = tk.Tk()
root.title("Análisis del Rendimiento Académico")
root.geometry("600x400")

# Funciones para realizar el análisis y mostrar los resultados en visualizaciones

def realizar_analisis(datos_seleccionados, tipo_visualizacion):
    if len(datos_seleccionados) != 2:
        messagebox.showerror("Error", "Debe seleccionar exactamente dos opciones.")
        return

    opciones_validas = {"Estudiante", "Edad", "Promedio"}
    if not set(datos_seleccionados).issubset(opciones_validas):
        print("Opciones inválidas seleccionadas.")
        return

    estudiantes = session.query(Estudiante).all()
    data = {
        "Estudiante": [estudiante.nombre for estudiante in estudiantes],
        "Promedio": [estudiante.promedio for estudiante in estudiantes],
        "Edad": [estudiante.edad for estudiante in estudiantes]
    }
    df = pd.DataFrame(data)

    if "Estudiante" in datos_seleccionados and "Promedio" in datos_seleccionados:
        if tipo_visualizacion == "Gráfico de Barras":
            sns.barplot(x="Estudiante", y="Promedio", data=df)
            plt.xlabel("Estudiante")
            plt.ylabel("Promedio")
            plt.title("Promedio de Calificaciones por Estudiante")
            plt.show()
        elif tipo_visualizacion == "Gráfico de Dispersión":
            sns.scatterplot(x="Estudiante", y="Promedio", data=df)
            plt.xlabel("Estudiante")
            plt.ylabel("Promedio")
            plt.title("Relación entre Estudiante y Promedio de Calificaciones")
            plt.show()
        elif tipo_visualizacion == "Gráfico de Pastel":
            plt.pie(df["Promedio"], labels=df["Estudiante"], autopct='%1.1f%%')
            plt.axis('equal')
            plt.title("Distribución de Promedios por Estudiante")
            plt.show()

    elif "Edad" in datos_seleccionados and "Promedio" in datos_seleccionados:
        if tipo_visualizacion == "Gráfico de Barras":
            sns.barplot(x="Edad", y="Promedio", data=df)
            plt.xlabel("Edad")
            plt.ylabel("Promedio")
            plt.title("Promedio de Calificaciones por Edad")
            plt.show()
        elif tipo_visualizacion == "Gráfico de Dispersión":
            sns.scatterplot(x="Edad", y="Promedio", data=df)
            plt.xlabel("Edad")
            plt.ylabel("Promedio")
            plt.title("Relación entre Edad y Promedio de Calificaciones")
            plt.show()
        elif tipo_visualizacion == "Gráfico de Pastel":
            plt.pie(df["Promedio"], labels=df["Edad"], autopct='%1.1f%%')
            plt.axis('equal')
            plt.title("Distribución de Promedios por Edad")
            plt.show()

    else:
        messagebox.showerror("Error", "Debe seleccionar la opcion promedios.")

# Resto del código de la interfaz de usuario...



# Resto del código...

# Elementos de la interfaz de usuario
datos_seleccionados = []

label = ttk.Label(root, text="Seleccione los datos a analizar:")
label.pack()

def toggle_checkbox(option):
    if option in datos_seleccionados:
        datos_seleccionados.remove(option)
    else:
        datos_seleccionados.append(option)

checkbutton1 = ttk.Checkbutton(root, text="Estudiante", command=lambda: toggle_checkbox("Estudiante"))
checkbutton1.pack()

checkbutton2 = ttk.Checkbutton(root, text="Promedio de Calificaciones", command=lambda: toggle_checkbox("Promedio"))
checkbutton2.pack()

checkbutton3 = ttk.Checkbutton(root, text="Edad", command=lambda: toggle_checkbox("Edad"))
checkbutton3.pack()

label = ttk.Label(root, text="Seleccione el tipo de visualización:")
label.pack()

tipo_visualizacion = tk.StringVar()

radiobutton1 = ttk.Radiobutton(root, text="Gráfico de Barras", variable=tipo_visualizacion, value="Gráfico de Barras")
radiobutton1.pack()

radiobutton2 = ttk.Radiobutton(root, text="Gráfico de Dispersión", variable=tipo_visualizacion, value="Gráfico de Dispersión")
radiobutton2.pack()

radiobutton3 = ttk.Radiobutton(root, text="Gráfico de Pastel", variable=tipo_visualizacion, value="Gráfico de Pastel")
radiobutton3.pack()

button = ttk.Button(root, text="Realizar Análisis", command=lambda: realizar_analisis(datos_seleccionados, tipo_visualizacion.get()))
button.pack()

root.mainloop()
