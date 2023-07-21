import tkinter as tk
from tkinter import ttk
import subprocess
import os
import subprocess

def ingresar_calificaciones():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo maininterface2.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'Historia_de_Usuario_2', 'Interfaces', 'maininterface2.py')

    # Lógica para ingresar calificaciones
    subprocess.Popen(['python', file_path])

def generar_informes():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo maininterface3.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'Historia_de_Usuario_3', 'Interfaces', 'maininterface3.py')

    # Lógica para generar informes
    subprocess.Popen(['python', file_path])

def identificar_bajo_rendimiento():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo maininterface4.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'Historia_de_Usuario_4', 'Interfaces', 'maininterface4.py')

    # Lógica para identificar bajo rendimiento
    subprocess.Popen(['python', file_path])

def analisis_visualizacion_datos():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo maininterface5.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'Historia_de_Usuario_5', 'Interfaces', 'maininterface5.py')

    # Lógica para análisis y visualización de datos
    subprocess.Popen(['python', file_path])

def conversion_archivos():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo convertir.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'convertir.py')

    # Lógica para conversión de archivos
    subprocess.Popen(['python', file_path])

def insercion_datos():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo base.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'base.py')

    # Lógica para insercion de datos
    subprocess.Popen(['python', file_path])

def mineria_datos():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo Aprendizaje.py utilizando la ruta relativa
    file_path = os.path.join(current_dir, 'Aprendizaje.py')

    # Lógica para minería de datos
    subprocess.Popen(['python', file_path])

# Crear la ventana principal
window = tk.Tk()
window.title("Sistema de Gestión Académica")

# Crear el controlador de pestañas
tab_control = ttk.Notebook(window)

# Pestaña "Ingresar Calificaciones"
tab_ingresar_calificaciones = ttk.Frame(tab_control)
tab_control.add(tab_ingresar_calificaciones, text='Ingresar Calificaciones')

# Pestaña "Generar Informes"
tab_generar_informes = ttk.Frame(tab_control)
tab_control.add(tab_generar_informes, text='Generar Informes')

# Pestaña "Estudiantes con Bajo Rendimiento"
tab_bajo_rendimiento = ttk.Frame(tab_control)
tab_control.add(tab_bajo_rendimiento, text='Estudiantes con Bajo Rendimiento')

# Pestaña "Análisis y Visualización"
tab_analisis_visualizacion = ttk.Frame(tab_control)
tab_control.add(tab_analisis_visualizacion, text='Análisis y Visualización')

# Pestaña "Conversión de  Archivos"
tab_analisis_visualizacion = ttk.Frame(tab_control)
tab_control.add(tab_analisis_visualizacion, text='Conversión de  Archivos')

# Pestaña "Inserción de  Datos"
tab_analisis_visualizacion = ttk.Frame(tab_control)
tab_control.add(tab_analisis_visualizacion, text='Inserción de  Datos')

# Pestaña "Minería de Datos"
tab_analisis_visualizacion = ttk.Frame(tab_control)
tab_control.add(tab_analisis_visualizacion, text='Minería de Datos')

# Posicionar y mostrar el controlador de pestañas
tab_control.pack(expand=1, fill='both')

# Asignar funciones a cada pestaña
tab_control.bind("<<NotebookTabChanged>>", lambda event: {
    0: ingresar_calificaciones,
    1: generar_informes,
    2: identificar_bajo_rendimiento,
    3: analisis_visualizacion_datos,
    4: conversion_archivos,
    5: insercion_datos,
    6: mineria_datos
}[tab_control.index(tab_control.select())]())

# Ejecutar la ventana principal
window.mainloop()
