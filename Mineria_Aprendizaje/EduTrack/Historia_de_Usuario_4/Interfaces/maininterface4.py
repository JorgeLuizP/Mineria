import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

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

# Umbral para identificar bajo rendimiento académico
umbral_rendimiento = 6.0

# Creación de la ventana principal
root = tk.Tk()
root.title("Estudiantes con Bajo Rendimiento Académico")
root.geometry("600x400")  # Ajustar el tamaño de la ventana principal

# Creación del árbol de datos
tree = ttk.Treeview(root)
tree["columns"] = ("nombre", "apellido", "edad", "código", "promedio")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("nombre", anchor=tk.CENTER, width=100)
tree.column("apellido", anchor=tk.CENTER, width=100)
tree.column("edad", anchor=tk.CENTER, width=50)
tree.column("código", anchor=tk.CENTER, width=70)
tree.column("promedio", anchor=tk.CENTER, width=70)

tree.heading("#0", text="", anchor=tk.CENTER)
tree.heading("nombre", text="Nombre", anchor=tk.CENTER)
tree.heading("apellido", text="Apellido", anchor=tk.CENTER)
tree.heading("edad", text="Edad", anchor=tk.CENTER)
tree.heading("código", text="Código", anchor=tk.CENTER)
tree.heading("promedio", text="Promedio", anchor=tk.CENTER)

tree.pack(fill="both", expand=True)  # Ajustar el tamaño del árbol de datos

# Función para mostrar los estudiantes en el árbol de datos
def mostrar_estudiantes():
    estudiantes = session.query(Estudiante).all()
    for estudiante in estudiantes:
        rendimiento = "Bajo" if estudiante.promedio < umbral_rendimiento else "Alto"
        tree.insert("", tk.END, text="", values=(estudiante.nombre, estudiante.apellido, estudiante.edad, estudiante.codigo_estudiante, estudiante.promedio, rendimiento))
        if estudiante.promedio < umbral_rendimiento:
            tree.item(tree.get_children()[-1], tags=("bajo_rendimiento",))
    
    tree.tag_configure("bajo_rendimiento", background="red")

# Mostrar los estudiantes al iniciar la aplicación
mostrar_estudiantes()

root.mainloop()
