from tkinter import Tk, Label, Entry, Button, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    average_grade = Column(Float)

def agregar_estudiante():
    nombre = entry_nombre.get()
    edad = int(entry_edad.get())
    grado = int(entry_grado.get())
    promedio = float(entry_promedio.get())

    # Validar el grado y promedio
    if not (1 <= grado <= 10) or not (1 <= promedio <= 100):
        messagebox.showerror("Error", "Grado y promedio deben estar entre 1 y 10.")
        return

    # Crear el motor de la base de datos y la sesión
    engine = create_engine('mysql://root:123456@localhost/learning_tracker')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear una instancia de Student con los datos del estudiante
    estudiante = Student(name=nombre, age=edad, grade=grado, average_grade=promedio)

    # Agregar el estudiante a la base de datos
    session.add(estudiante)
    session.commit()

    # Cerrar la sesión
    session.close()

    # Limpiar los campos después de agregar el estudiante
    entry_nombre.delete(0, 'end')
    entry_edad.delete(0, 'end')
    entry_grado.delete(0, 'end')
    entry_promedio.delete(0, 'end')

    messagebox.showinfo("Éxito", "Estudiante agregado con éxito.")

root = Tk()
root.title("Agregar Estudiante")
root.geometry("400x250")  # Establecer el tamaño inicial de la ventana

label_nombre = Label(root, text="Nombre:")
label_nombre.pack()
entry_nombre = Entry(root)
entry_nombre.pack()

label_edad = Label(root, text="Edad:")
label_edad.pack()
entry_edad = Entry(root)
entry_edad.pack()

label_grado = Label(root, text="Grado:")
label_grado.pack()
entry_grado = Entry(root)
entry_grado.pack()

label_promedio = Label(root, text="Promedio:")
label_promedio.pack()
entry_promedio = Entry(root)
entry_promedio.pack()

button_agregar = Button(root, text="Agregar estudiante", command=agregar_estudiante)
button_agregar.pack()

root.mainloop()
