import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Establecer la cadena de conexión a MySQL
user = 'root'
password = '123456'
host = 'localhost'
database = 'learning_tracker_final'

# Crear el motor de SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}', echo=True)

Base = declarative_base()

class Estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    numero_id = Column(String(255))
    institucion = Column(String(255))
    departamento = Column(String(255))
    correo = Column(String(255))


class Calificacion(Base):
    __tablename__ = 'calificaciones'

    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    id_materia = Column(Integer, ForeignKey('materias.id'))
    total_parcial_final_aprovechamiento = Column(Float)
    cuestionario_examen_final = Column(Float)
    total_parcial_final_examen = Column(Float)
    total_parcial_final = Column(Float)
    total_curso = Column(Float)

    estudiante = relationship("Estudiante", backref="calificaciones")
    materia = relationship("Materia", backref="calificaciones")


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    ultima_descarga = Column(Date)


class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True)
    nombre_materia = Column(String(255))

def obtener_ruta_csv_entrenamiento():
    # Ruta del directorio "entrenamiento"
    carpeta_entrenamiento = 'entrenamiento'

    # Obtener la ruta del primer archivo CSV en el directorio "entrenamiento"
    archivos_csv = [archivo for archivo in os.listdir(carpeta_entrenamiento) if archivo.endswith('.csv')]
    if archivos_csv:
        return os.path.join(carpeta_entrenamiento, archivos_csv[0])
    else:
        return None

def crear_base_datos(nombre_materia):
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Obtener la ruta del archivo CSV
    ruta_csv = obtener_ruta_csv_entrenamiento()

    if ruta_csv:
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(ruta_csv)

        # Crear una sesión de SQLAlchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Crear la instancia de Materia con el nombre ingresado
            materia = Materia(nombre_materia=nombre_materia)

            # Agregar la instancia a la sesión
            session.add(materia)

            # Confirmar los cambios en la base de datos
            session.commit()

            # Obtener el ID de la materia recién creada
            id_materia = materia.id

            # Iterar sobre las filas del DataFrame y crear instancias de Estudiante y Calificacion
            for _, row in df.iterrows():
                estudiante = Estudiante(
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    numero_id=row['Numero_ID'],
                    institucion=row['Institucion'] if pd.notna(row['Institucion']) else None,
                    departamento=row['Departamento'] if pd.notna(row['Departamento']) else None,
                    correo=row['Correo']
                )

                calificacion = Calificacion(
                    total_parcial_final_aprovechamiento=row['Total_Parcial_Final_Aprovechamiento'],
                    cuestionario_examen_final=row['Cuestionario_Examen_Final'],
                    total_parcial_final_examen=row['Total_Parcial_Final_Examen'],
                    total_parcial_final=row['Total_Parcial_Final'],
                    total_curso=row['Total_Curso'],
                    estudiante=estudiante,
                    id_materia=id_materia
                )

                # Agregar las instancias a la sesión
                session.add(estudiante)
                session.add(calificacion)

            # Confirmar los cambios en la base de datos
            session.commit()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos del archivo CSV: {str(e)}")
            session.rollback()

        finally:
            # Cerrar la sesión
            session.close()
    else:
        messagebox.showwarning("Advertencia", "No se encontró ningún archivo CSV en la carpeta 'entrenamiento'")

def seleccionar_archivos():
    # Solicitar el nombre de la materia gráficamente
    nombre_materia = tk.simpledialog.askstring("Nombre de la Materia", "Ingrese el nombre de la materia:")

    if nombre_materia:
        crear_base_datos(nombre_materia)
        messagebox.showinfo("Información", "Procesamiento de archivos completado")
    else:
        messagebox.showwarning("Advertencia", "Debe ingresar un nombre de materia válido")

window = tk.Tk()
window.title("Conversión de archivos XLSX a Base de Datos")
window.geometry("300x150")

lbl_instrucciones = tk.Label(window, text="Proceso de Inserción de datos de entrenamiento:")
lbl_instrucciones.pack(pady=10)

btn_seleccionar_archivos = tk.Button(window, text="Insertar Datos", command=seleccionar_archivos)
btn_seleccionar_archivos.pack(pady=10)

window.mainloop()
