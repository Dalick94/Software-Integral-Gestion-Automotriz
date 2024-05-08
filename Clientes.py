import tkinter as Tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter import Image, Label
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3
import platform
import subprocess
from tkinter import ttk
def mostrar_vehiculos_asociados():
    # Obtener el DNI/NIE del cliente
    dni_cliente = var_dni_nie.get()

    # Limpiar el Treeview
    for record in tree.get_children():
        tree.delete(record)

    # Consultar vehículos asociados al cliente
    conn = sqlite3.connect('Taller.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM vehiculos WHERE dni_cliente=?", (dni_cliente,))
    vehiculos = c.fetchall()
    
    for vehiculo in vehiculos:
        tree.insert("", "end", values=vehiculo[1:5])  # Agregar vehículo al Treeview, omitiendo el id_vehiculo

def open_almacen():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['python', 'menu clientes.py'], creationflags=subprocess.CREATE_NO_WINDOW)
            ventana.destroy()
        else:
            subprocess.run(['Python3', 'menu clientes.py'])
            ventana.destroy()
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir menu clientes.py.\n{e}')

# Función para verificar si los campos obligatorios están completos
def entries():
    campos = {
        'Nombre': var_nombre.get(),
        'Apellido1': var_apellido1.get(),
        'Apellido2': var_apellido2.get(),
        'Telefono1': var_tel_contacto1.get(),
        'DNI_NIE': var_dni_nie.get(),
        'Direccion': var_direccion.get(),
        'Codigo_postal': var_codigo_postal.get(),
        'Municipio': var_municipio.get(),
        'Provincia': var_provincia.get(),
    }

    campos_incompletos = [campo for campo, valor in campos.items() if not valor]

    if campos_incompletos:
        mb.showerror("Campos incompletos", f"Por favor, complete los siguientes campos: {', '.join(campos_incompletos)}")
        return False

    return True

# Función para dar de alta un cliente
def alta_cliente():
    # Verificar si los campos obligatorios están completos
    if not entries():
        return
    
    # Conectar a la base de datos
    conn = sqlite3.connect('Clientes.db')
    c = conn.cursor()
    
    # Construir la tupla de datos para la inserción
    data = (
        var_nombre.get(),
        var_apellido1.get(),
        var_apellido2.get(),
        var_tel_contacto1.get(),
        var_tel_contacto2.get(),
        var_correo.get(),
        var_dni_nie.get(),
        var_direccion.get(),
        var_codigo_postal.get(),
        var_municipio.get(),
        var_provincia.get(),
        var_comentario.get() if var_comentario.get() else None  # Campo de comentario opcional
    )

    try:
        # Ejecutar la consulta SQL para insertar los datos
        c.execute("""
            INSERT INTO clientes 
            (Nombre, Apellido1, Apellido2, Telefono1, Telefono2, Correo, DNI_NIE, Direccion, Codigo_postal, Municipio, Provincia, Comentario) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Mostrar mensaje de éxito
        mb.showinfo("Alta cliente", "Cliente dado de alta correctamente")

        # Limpiar los campos de la ventana
        clear_entries()

    except Exception as e:
        # En caso de error, mostrar mensaje de error
        mb.showerror("Error", f"No se pudo dar de alta al cliente.\n{e}")

def clear_entries():
    var_nombre.set('')
    var_apellido1.set('')
    var_apellido2.set('')
    var_tel_contacto1.set('')
    var_tel_contacto2.set('')
    var_correo.set('')
    var_dni_nie.set('')
    var_direccion.set('')
    var_codigo_postal.set('')
    var_municipio.set('')
    var_provincia.set('')
    var_comentario.set('')
 # Buscar el Cliente en la BBDD
def buscar_cliente():
    conn = sqlite3.connect('Clientes.db')
    c = conn.cursor()

    # Obtener los datos de las cajas de texto
    
    dni_nie = var_dni_nie.get()

    # Construir la consulta SQL
    consulta = "SELECT * FROM clientes WHERE DNI_NIE=?"
    c.execute(consulta, (dni_nie,))
    cliente = c.fetchone()

    if cliente:
        # Completar los campos de la ventana con los datos del cliente encontrado
        var_nombre.set(cliente[1])
        var_apellido1.set(cliente[2])
        var_apellido2.set(cliente[3])
        var_tel_contacto1.set(cliente[4])
        var_tel_contacto2.set(cliente[5])
        var_correo.set(cliente[6])
        var_dni_nie.set(cliente[7])
        var_direccion.set(cliente[8])
        var_codigo_postal.set(cliente[9])
        var_municipio.set(cliente[10])
        var_provincia.set(cliente[11])
        var_comentario.set(cliente[12])

        mb.showinfo("Cliente encontrado", "Los datos del cliente han sido cargados en los campos.")
    else:
        mb.showerror("Cliente no encontrado", "No se encontró ningún cliente con los datos proporcionados")

    conn.close()

#Modificar Datos del Cliente y Guardar
def modificar_datos():
    # Comprobar si se han ingresado todos los datos necesarios
    if not entries():
        return

    # Obtener el DNI/NIE actual del cliente
    dni_nie_actual = var_dni_nie.get()

    # Conectar a la base de datos
    for db_name in ['Clientes.db', 'Taller.db']:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        data = (
            var_nombre.get(),
            var_apellido1.get(),
            var_apellido2.get(),
            var_tel_contacto1.get(),
            var_tel_contacto2.get(),
            var_correo.get(),
            var_dni_nie.get(),
            var_direccion.get(),
            var_codigo_postal.get(),
            var_municipio.get(),
            var_provincia.get(),
            var_comentario.get(),
            dni_nie_actual
        )
        c.execute("UPDATE clientes SET Nombre=?, Apellido1=?, Apellido2=?, Telefono1=?, Telefono2=?, Correo=?,DNI_NIE=?, Direccion=?, Codigo_postal=?, Municipio=?, Provincia=?, Comentario=? WHERE DNI_NIE=?", data)
        conn.commit()
        conn.close()
    # Mostrar mensaje de éxito
    mb.showinfo("Modificación exitosa", "Los datos del cliente han sido modificados correctamente")

    # Limpiar los campos de la ventana después de la modificación
    clear_entries()
 

def mostrar_vehiculos_asociados():
    dni_cliente = var_dni_nie.get()
    
    if not dni_cliente:
        mb.showwarning("DNI/NIE vacío", "Por favor, ingrese el DNI/NIE del cliente primero.")
        return

    tree_vehiculos.delete(*tree_vehiculos.get_children())  # Limpiar el Treeview
    
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        
        cursor.execute("""
                        SELECT matricula, numero_bastidor, marca, modelo, version, 
                        codigo_motor, planta_motriz, kilometros, etiqueta_medioambiental, 
                        fecha_itv_ok, color_carroceria, comentario_descripcion
                        FROM vehiculos 
                        WHERE dni_cliente=?
                        """, (dni_cliente,))
        
        vehiculos = cursor.fetchall()

        if vehiculos:
            for vehiculo in vehiculos:
                tree_vehiculos.insert("", "end", values=vehiculo)
        else:
            mb.showwarning("Sin vehículos", f"No se encontraron vehículos asociados al cliente con DNI/NIE {dni_cliente}")
    



# Creacion De Ventana
ventana = Tk()
ventana.title("Gestión de Clientes")
ventana.geometry("1100x750")
ventana.state("zoomed")
ventana.configure(bg="white")
ventana.iconbitmap("./iconos y logo/icono.ico")

var_nombre = StringVar()
var_apellido1 = StringVar()
var_apellido2 = StringVar()
var_tel_contacto1 = IntVar()
var_tel_contacto2 = IntVar()
var_correo = StringVar()
var_dni_nie = StringVar()
var_direccion = StringVar()
var_codigo_postal = IntVar()
var_municipio = StringVar()
var_provincia = StringVar()
var_comentario = StringVar()
# Crear Logo
logo_image = Image.open('./iconos y logo/logo.png')
logo_photo = ImageTk.PhotoImage(logo_image.resize((900, 168), Image.Resampling.LANCZOS))
logo_label = Label(ventana, image=logo_photo, bg='white')
logo_label.image = logo_photo
# Modificar la posición del logo dentro del grid
logo_label.grid(row=0, column=0, columnspan=6, pady=20, sticky='nsew')

# Configurar la barra de desplazamiento horizontal

tree_vehiculos = ttk.Treeview(ventana, show="headings")
tree_vehiculos["columns"] = ("Matrícula", "Número de bastidor", "Marca", "Modelo", "Versión", "Código del motor", "Planta motriz", "Kilómetros", "Etiqueta medioambiental", "Fecha ITV OK", "Color de la carrocería", "Comentario/descripción")

for column in tree_vehiculos["columns"]:
    tree_vehiculos.column(column, anchor=W, width=150)
    tree_vehiculos.heading(column, text=column)

scrollbar_horizontal = ttk.Scrollbar(ventana, orient="horizontal", command=tree_vehiculos.xview)
tree_vehiculos.configure(xscrollcommand=scrollbar_horizontal.set)

scrollbar_horizontal.grid(row=10, column=0, columnspan=6, sticky="ew", padx=10, pady=5)
tree_vehiculos.grid(row=9, column=0, columnspan=6, padx=10, pady=10, sticky="ew")

# Marco datos clientes
marco_datos_cliente = Frame(ventana)
marco_datos_cliente.grid(row=1, column=0, columnspan=6, padx=10, pady=10)
marco_datos_cliente.configure(background='white')

# Label Titulo
titulo = Label(marco_datos_cliente, text='DATOS CLIENTE', font=('Arial', 16, 'bold'))
titulo.grid(row=0, column=0, columnspan=6, pady=10)
titulo.configure(background='white', foreground='#311B92')

# Etiquetas y cajas de texto
# Etiqueta Nombre
etiqueta_nombre = Label(marco_datos_cliente, text='Nombre * :', font=('Arial', 12))
etiqueta_nombre.grid(row=1, column=0, pady=5, padx=10, sticky='e')
etiqueta_nombre.configure(background='white', foreground='#311B92')

# Caja de texto Nombre
cajatexto_nombre = Entry(marco_datos_cliente, textvariable=var_nombre)
cajatexto_nombre.grid(row=1, column=1, pady=5, padx=10, sticky='e')
cajatexto_nombre.configure(background='white', foreground='black')

# Etiqueta Apellido 1
etiqueta_apellido1 = Label(marco_datos_cliente, text='Apellido 1 * :', font=('Arial', 12))
etiqueta_apellido1.grid(row=1, column=2, pady=5, padx=10, sticky='e')
etiqueta_apellido1.configure(background='white', foreground='#311B92')

# Caja de texto Apellido 1
cajatexto_apellido1 = Entry(marco_datos_cliente, textvariable=var_apellido1)
cajatexto_apellido1.grid(row=1, column=3, pady=5, padx=10, sticky='ew')
cajatexto_apellido1.configure(background='white', foreground='black')

# Etiqueta Apellido 2
etiqueta_apellido2 = Label(marco_datos_cliente, text='Apellido 2 * :', font=('Arial', 12))
etiqueta_apellido2.grid(row=1, column=4, pady=5, padx=10, sticky='e')
etiqueta_apellido2.configure(background='white', foreground='#311B92')

# Caja de texto Apellido 2
cajatexto_apellido2 = Entry(marco_datos_cliente, textvariable=var_apellido2)
cajatexto_apellido2.grid(row=1, column=5, pady=10, padx=10, sticky='e')
cajatexto_apellido2.configure(background='white', foreground='black')

# Etiqueta Telefono contacto 1
etiqueta_tel_contacto1 = Label(marco_datos_cliente, text='Telefono 1 * :', font=('Arial', 12))
etiqueta_tel_contacto1.grid(row=2, column=0, pady=5, padx=10, sticky='e')
etiqueta_tel_contacto1.configure(background='white', foreground='#311B92')

# Caja de texto Telefono contacto 1
cajatexto_tel_contacto1 = Entry(marco_datos_cliente, textvariable=var_tel_contacto1)
cajatexto_tel_contacto1.grid(row=2, column=1, pady=5, padx=10, sticky='e')
cajatexto_tel_contacto1.configure(background='white', foreground='black')

# Etiqueta Telefono contacto 2
etiqueta_tel_contacto2 = Label(marco_datos_cliente, text='Telefono 2 :', font=('Arial', 12))
etiqueta_tel_contacto2.grid(row=2, column=2, pady=5, padx=10, sticky='e')
etiqueta_tel_contacto2.configure(background='white', foreground='#311B92')

# Caja de texto Telefono contacto 2
cajatexto_tel_contacto2 = Entry(marco_datos_cliente, textvariable=var_tel_contacto2)
cajatexto_tel_contacto2.grid(row=2, column=3, pady=5, padx=10, sticky='ew')
cajatexto_tel_contacto2.configure(background='white', foreground='black')

# Etiqueta Correo Electronico
etiqueta_correo = Label(marco_datos_cliente, text='Email :', font=('Arial', 12))
etiqueta_correo.grid(row=2, column=4, pady=5, padx=10, sticky='e')
etiqueta_correo.configure(background='white', foreground='#311B92')

# Caja de texto Correo Electronico
cajatexto_correo = Entry(marco_datos_cliente, textvariable=var_correo)
cajatexto_correo.grid(row=2, column=5, pady=5, padx=10, sticky='e')
cajatexto_correo.configure(background='white', foreground='black')

# Etiqueta DNI/NIE
etiqueta_dni_nie = Label(marco_datos_cliente, text='DNI/NIE * :', font=('Arial', 12))
etiqueta_dni_nie.grid(row=3, column=0, pady=5, padx=10, sticky='e')
etiqueta_dni_nie.configure(background='white', foreground='#311B92')

# Caja de texto DNI/NIE
cajatexto_dni_nie = Entry(marco_datos_cliente, textvariable=var_dni_nie)
cajatexto_dni_nie.grid(row=3, column=1, pady=5, padx=10, sticky='e')
cajatexto_dni_nie.configure(background='white', foreground='black')

# Etiqueta Buscar Cliente
etiqueta_dni_nie = Label(marco_datos_cliente, text='(Buscar cliente ingrese DNI/NIE)', font=('Arial', 10))
etiqueta_dni_nie.grid(row=3, column=2, pady=5, padx=10, sticky='ew')
etiqueta_dni_nie.configure(background='white', foreground='#311B92')
# Etiqueta Campos Obligatorios
etiqueta_dni_nie = Label(marco_datos_cliente, text='( * Campos Obligatorios,Alta Cliente)', font=('Arial', 10))
etiqueta_dni_nie.grid(row=3, column=3, pady=5, padx=10, sticky='ew')
etiqueta_dni_nie.configure(background='white', foreground='#311B92')

# Etiqueta Direccion
etiqueta_direccion = Label(marco_datos_cliente, text='Direccion * :', font=('Arial', 12))
etiqueta_direccion.grid(row=4, column=0, pady=5, padx=10, sticky='w')
etiqueta_direccion.configure(background='white', foreground='#311B92')

# Caja de texto Direccion
cajatexto_direccion = Entry(marco_datos_cliente, textvariable=var_direccion)
cajatexto_direccion.grid(row=4, column=1, columnspan=5, pady=5, padx=10, sticky='ew')
cajatexto_direccion.configure(background='white', foreground='black')

# Etiqueta Codigo postal
etiqueta_codigo_postal = Label(marco_datos_cliente, text='Codigo Postal * :', font=('Arial', 12))
etiqueta_codigo_postal.grid(row=5, column=0, pady=5, padx=10, sticky='w')
etiqueta_codigo_postal.configure(background='white', foreground='#311B92')

# Caja de text Codigo postal
cajatexto_codigo_postal = Entry(marco_datos_cliente, textvariable=var_codigo_postal)
cajatexto_codigo_postal.grid(row=5, column=1, pady=5, padx=10, sticky='e')
cajatexto_codigo_postal.configure(background='white', foreground='black')

# Etiqueta Municipio
etiqueta_municipio = Label(marco_datos_cliente, text='Municipio * :', font=('Arial', 12))
etiqueta_municipio.grid(row=5, column=2, pady=5, padx=10, sticky='w')
etiqueta_municipio.configure(background='white', foreground='#311B92')

# Caja de texto Municipio
cajatexto_municipio = Entry(marco_datos_cliente, textvariable=var_municipio)
cajatexto_municipio.grid(row=5, column=3, pady=5, padx=10, sticky='e')
cajatexto_municipio.configure(background='white', foreground='black')

# Etiqueta Provincia
etiqueta_provincia = Label(marco_datos_cliente, text='Provincia * :', font=('Arial', 12))
etiqueta_provincia.grid(row=5, column=4, pady=5, padx=10, sticky='w')
etiqueta_provincia.configure(background='white', foreground='#311B92')

# Caja de texto Provincia
cajatexto_provincia = Entry(marco_datos_cliente, textvariable=var_provincia)
cajatexto_provincia.grid(row=5, column=5, pady=5, padx=10, sticky='e')
cajatexto_provincia.configure(background='white', foreground='black')

# Etiqueta Comentario
etiqueta_comentario = Label(marco_datos_cliente, text='Comentario :', font=('Arial', 12))
etiqueta_comentario.grid(row=6, column=0, pady=5, padx=10, sticky='w')
etiqueta_comentario.configure(background='white', foreground='#311B92')

# Caja de texto Comentario
cajatexto_comentario = Entry(marco_datos_cliente, textvariable=var_comentario)
cajatexto_comentario.grid(row=6, column=1, rowspan=2, columnspan=3, pady=5, padx=10, sticky='ew')
cajatexto_comentario.configure(background='white', foreground='black')




# Botones
# Boton Alta cliente
boton_alta_cliente = Button(marco_datos_cliente, text='Alta Cliente', font=('Arial', 14), command=alta_cliente)
boton_alta_cliente.grid(row=8, column=1, pady=5, padx=10)
boton_alta_cliente.configure(background='#311B92', foreground='white')

# Boton Buscar cliente
boton_buscar_cliente = Button(marco_datos_cliente, text='Buscar Cliente', font=('Arial', 14), command=buscar_cliente)
boton_buscar_cliente.grid(row=8, column=2, pady=5, padx=10)
boton_buscar_cliente.configure(background='#311B92', foreground='white')

#Boton mostrar vehiculos asociados al cliente
boton_mostrar_vehiculos_asociados = Button(marco_datos_cliente, text='Mostrar vehículos', font=('Arial', 14), command=mostrar_vehiculos_asociados)
boton_mostrar_vehiculos_asociados.grid(row=8, column=3, pady=5, padx=10)
boton_mostrar_vehiculos_asociados.configure(background='#311B92', foreground='white')


# Boton Modificar Datos
boton_modificar_datos = Button(marco_datos_cliente, text='Modificar Datos', font=('Arial', 14),command=modificar_datos)
boton_modificar_datos.grid(row=8, column=4, pady=5, padx=10)
boton_modificar_datos.configure(background='#311B92', foreground='white')

# Boton Limpiar
boton_limpiar = Button(marco_datos_cliente, text='Limpiar', font=('Arial', 14), command=clear_entries)
boton_limpiar.grid(row=8, column=5, pady=5, padx=10)
boton_limpiar.configure(background='#311B92', foreground='white')



# Boton Salir
boton_salir = Button(ventana, text='Salir', font=('Arial', 14), command=open_almacen)
boton_salir.grid(row=17, column=7, pady=5, padx=10)
boton_salir.configure(background='red', foreground='white')



# Footer
footer = Label(ventana, text='Desarrollado por: MurciaTec', font=('Arial', 10))
footer.grid(row=2, column=0, columnspan=6, pady=(20, 10))
footer.configure(background='white', foreground='#311B92')





# Mostrar ventana
ventana.mainloop()
