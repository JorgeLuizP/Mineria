from tkinter import *
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from tkinter import ttk

# Crear la base de datos
engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')
Base = declarative_base()

# Definir las clases de la base de datos
class Estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    edad = Column(Integer)
    codigo_estudiante = Column(String, unique=True)
    promedio = Column(Float)

    calificaciones = relationship("Calificacion", back_populates="estudiante")

class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)

    calificaciones = relationship("Calificacion", back_populates="materia")

class Calificacion(Base):
    __tablename__ = 'calificaciones'

    id = Column(Integer, primary_key=True)
    id_estudiante = Column(Integer, ForeignKey('estudiantes.id'))
    id_materia = Column(Integer, ForeignKey('materias.id'))
    calificacion = Column(Float)

    estudiante = relationship("Estudiante", back_populates="calificaciones")
    materia = relationship("Materia", back_populates="calificaciones")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

def agregar_estudiante():
    # Obtener los valores ingresados en el formulario
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    edad = entry_edad.get()
    codigo_estudiante = entry_codigo_estudiante.get()

    # Validar que se hayan ingresado todos los datos
    if not nombre or not apellido or not edad or not codigo_estudiante:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Crear el motor de la base de datos y la sesión
    engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Verificar si el estudiante ya existe en la base de datos
    estudiante_existente = session.query(Estudiante).filter(Estudiante.codigo_estudiante == codigo_estudiante).first()
    if estudiante_existente:
        messagebox.showerror("Error", "El estudiante ya existe en la base de datos.")
        session.close()
        return

    # Crear una instancia de Estudiante con los datos ingresados
    estudiante = Estudiante(nombre=nombre, apellido=apellido, edad=edad, codigo_estudiante=codigo_estudiante, promedio=0)

    # Agregar el estudiante a la base de datos
    session.add(estudiante)

    # Agregar las calificaciones iniciales con valor cero
    materias = session.query(Materia).all()
    for materia in materias:
        calificacion_nueva = Calificacion(calificacion=0)
        estudiante.calificaciones.append(calificacion_nueva)
        materia.calificaciones.append(calificacion_nueva)
        session.add(calificacion_nueva)

    # Commit para guardar todos los cambios
    session.commit()

    # Cerrar la sesión
    session.close()

    # Limpiar los campos del formulario
    entry_nombre.delete(0, 'end')
    entry_apellido.delete(0, 'end')
    entry_edad.delete(0, 'end')
    entry_codigo_estudiante.delete(0, 'end')

    messagebox.showinfo("Éxito", "Estudiante agregado con éxito.")
    combo_estudiantes['values'] = tuple(f"{estudiante.nombre} {estudiante.apellido}" for estudiante in estudiantes)

def mostrar_estudiantes():
    # Limpiar el Treeview
    treeview_estudiantes.delete(*treeview_estudiantes.get_children())

    # Crear el motor de la base de datos y la sesión
    engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Obtener todos los estudiantes de la base de datos
    estudiantes = session.query(Estudiante).all()

    # Mostrar los estudiantes en el Treeview
    for estudiante in estudiantes:
        promedio = round(estudiante.promedio, 2)
        treeview_estudiantes.insert('', 'end', values=(estudiante.nombre, estudiante.apellido, estudiante.edad, estudiante.codigo_estudiante, promedio))

    # Cerrar la sesión
    session.close()

def agregar_calificacion():
    # Verificar si se ha seleccionado un estudiante en el ComboBox
    if combo_estudiantes.current() != -1:
        # Obtener el estudiante seleccionado del ComboBox
        estudiante_seleccionado = combo_estudiantes.get()
        nombre_estudiante = estudiante_seleccionado

        # Obtener la calificación ingresada
        calificacion = entry_calificacion.get()

        # Validar que se haya ingresado una calificación
        if not calificacion:
            messagebox.showerror("Error", "Por favor, ingrese una calificación.")
            return

        # Verificar si la calificación es válida
        try:
            calificacion = float(calificacion)
        except ValueError:
            messagebox.showerror("Error", "La calificación debe ser un número válido.")
            return

        if calificacion < 0 or calificacion > 10:
            messagebox.showerror("Error", "La calificación debe estar entre 0 y 10.")
            return

        # Obtener el estudiante seleccionado de la base de datos
        engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')
        Session = sessionmaker(bind=engine)
        session = Session()

        estudiante = session.query(Estudiante).filter(
            Estudiante.nombre == nombre_estudiante.split()[0],
            Estudiante.apellido == nombre_estudiante.split()[1]
        ).first()

        # Obtener la materia seleccionada de la base de datos
        materia = session.query(Materia).filter(Materia.nombre == combo_materias.get()).first()

        # Verificar si el estudiante ya tiene una calificación para la materia seleccionada
        calificacion_existente = session.query(Calificacion).filter(
            Calificacion.estudiante == estudiante,
            Calificacion.materia == materia
        ).first()

        if calificacion_existente:
            # Reemplazar la calificación existente por la nueva calificación
            calificacion_existente.calificacion = calificacion
        else:
            # Crear una nueva instancia de Calificacion con la calificación ingresada
            calificacion_nueva = Calificacion(calificacion=calificacion)
            # Asignar la relación entre el estudiante, la materia y la calificación
            estudiante.calificaciones.append(calificacion_nueva)
            materia.calificaciones.append(calificacion_nueva)

        # Actualizar el promedio del estudiante
        calificaciones_estudiante = [float(calificacion.calificacion) for calificacion in estudiante.calificaciones]
        print("Calificaciones del estudiante:", calificaciones_estudiante)

        # Calcular el promedio
        promedio_estudiante = sum(calificaciones_estudiante) / len(calificaciones_estudiante)
        print("Promedio del estudiante:", promedio_estudiante)

        # Actualizar el promedio del estudiante en la base de datos
        estudiante.promedio = promedio_estudiante

        # Actualizar la base de datos
        session.commit()

        # Cerrar la sesión
        session.close()

        # Limpiar el campo de calificación
        entry_calificacion.delete(0, 'end')

        # Actualizar el promedio del estudiante en el ComboBox y en la lista de estudiantes
        actualizar_promedio_estudiante(nombre_estudiante, promedio_estudiante)

        messagebox.showinfo("Éxito", "Calificación agregada correctamente.")
    else:
        messagebox.showerror("Error", "Por favor, seleccione un estudiante.")



# Actualiza el promedio de un estudiante en el ComboBox y en la lista de estudiantes
def actualizar_promedio_estudiante(nombre_estudiante, promedio):
    # Actualizar el promedio del estudiante en la lista de estudiantes
    for estudiante in estudiantes:
        if estudiante.nombre == nombre_estudiante.split()[0] and estudiante.apellido == nombre_estudiante.split()[1]:
            estudiante.promedio = promedio
            break

    # Actualizar el promedio del estudiante en el ComboBox
    combo_estudiantes['values'] = tuple(f"{estudiante.nombre} {estudiante.apellido}" for estudiante in estudiantes)


# Crear la ventana principal
root = Tk()
root.title("EduTrack")

# Crear un marco para el formulario de agregar estudiante
frame_agregar_estudiante = LabelFrame(root, text="Agregar Estudiante")
frame_agregar_estudiante.pack(padx=10, pady=10)

label_nombre = Label(frame_agregar_estudiante, text="Nombre:")
label_nombre.grid(row=0, column=0)
entry_nombre = Entry(frame_agregar_estudiante)
entry_nombre.grid(row=0, column=1)

label_apellido = Label(frame_agregar_estudiante, text="Apellido:")
label_apellido.grid(row=1, column=0)
entry_apellido = Entry(frame_agregar_estudiante)
entry_apellido.grid(row=1, column=1)

label_edad = Label(frame_agregar_estudiante, text="Edad:")
label_edad.grid(row=2, column=0)
entry_edad = Entry(frame_agregar_estudiante)
entry_edad.grid(row=2, column=1)

label_codigo_estudiante = Label(frame_agregar_estudiante, text="Código Estudiante:")
label_codigo_estudiante.grid(row=3, column=0)
entry_codigo_estudiante = Entry(frame_agregar_estudiante)
entry_codigo_estudiante.grid(row=3, column=1)

btn_agregar_estudiante = Button(frame_agregar_estudiante, text="Agregar", command=agregar_estudiante)
btn_agregar_estudiante.grid(row=4, columnspan=2, pady=5)

# Crear un marco para la lista de estudiantes
frame_lista_estudiantes = LabelFrame(root, text="Lista de Estudiantes")
frame_lista_estudiantes.pack(padx=10, pady=10)

# Crear un Treeview para mostrar los estudiantes
treeview_estudiantes = ttk.Treeview(frame_lista_estudiantes, columns=("nombre", "apellido", "edad", "codigo_estudiante", "promedio"), show="headings")
treeview_estudiantes.column("nombre", width=100)
treeview_estudiantes.column("apellido", width=100)
treeview_estudiantes.column("edad", width=50)
treeview_estudiantes.column("codigo_estudiante", width=100)
treeview_estudiantes.column("promedio", width=70)
treeview_estudiantes.heading("nombre", text="Nombre")
treeview_estudiantes.heading("apellido", text="Apellido")
treeview_estudiantes.heading("edad", text="Edad")
treeview_estudiantes.heading("codigo_estudiante", text="Código Estudiante")
treeview_estudiantes.heading("promedio", text="Promedio")
treeview_estudiantes.pack()

btn_mostrar_estudiantes = Button(frame_lista_estudiantes, text="Mostrar Estudiantes", command=mostrar_estudiantes)
btn_mostrar_estudiantes.pack(pady=5)

# Crear un marco para agregar calificaciones
frame_agregar_calificacion = LabelFrame(root, text="Agregar Calificación")
frame_agregar_calificacion.pack(padx=10, pady=10)

label_estudiante = Label(frame_agregar_calificacion, text="Estudiante:")
label_estudiante.grid(row=0, column=0)

combo_estudiantes = ttk.Combobox(frame_agregar_calificacion, values=[])
combo_estudiantes.grid(row=0, column=1)

label_materia = Label(frame_agregar_calificacion, text="Materia:")
label_materia.grid(row=1, column=0)

combo_materias = ttk.Combobox(frame_agregar_calificacion, values=[])
combo_materias.grid(row=1, column=1)

label_calificacion = Label(frame_agregar_calificacion, text="Calificación:")
label_calificacion.grid(row=2, column=0)

entry_calificacion = Entry(frame_agregar_calificacion)
entry_calificacion.grid(row=2, column=1)

btn_agregar_calificacion = Button(frame_agregar_calificacion, text="Agregar", command=agregar_calificacion)
btn_agregar_calificacion.grid(row=3, columnspan=2, pady=5)

# Obtener los estudiantes y las materias disponibles de la base de datos
engine = create_engine('mysql://root:123456@localhost/learning_tracker_h2')
Session = sessionmaker(bind=engine)
session = Session()
estudiantes = session.query(Estudiante).all()
estudiantes_nombres = [f"{estudiante.nombre} {estudiante.apellido}" for estudiante in estudiantes]
materias = session.query(Materia).all()
materias_nombres = [materia.nombre for materia in materias]
session.close()

# Actualizar los valores de los Combobox
combo_estudiantes['values'] = estudiantes_nombres
combo_materias['values'] = materias_nombres

# Ejecutar la ventana principal
root.mainloop()
