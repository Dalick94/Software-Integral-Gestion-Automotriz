import tkinter as Tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter import Label
from PIL import Image, ImageTk
from tkinter import filedialog
from fpdf import FPDF
import sqlite3
import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import Tk
import tkinter as tk

# Crear ventana
ventana = Tk()
ventana.title("Detalles de Factura")
ventana.geometry("1000x800")
ventana.configure(bg="white")
ventana.iconbitmap("icono.ico")
ventana.state('zoomed')

# Variables Factura
var_factura_id = StringVar()
var_fecha = StringVar()

# Variables Vehiculo
var_matricula = StringVar()
var_marca_vehiculo = StringVar()
var_modelo_vehiculo = StringVar()

# Variables Datos Cliente
var_nombre = StringVar()
var_apellido1 = StringVar()
var_apellido2 = StringVar()
var_tel_contacto1 = StringVar()
var_tel_contacto2 = StringVar()
var_correo = StringVar()
var_dni_nie = StringVar()
var_direccion = StringVar()
var_codigo_postal = StringVar()
var_municipio = StringVar()
var_provincia = StringVar()

# Variables Orden de trabajo Valor
var_orden_de_trabajo = StringVar()
# IVA
var_iva = StringVar()
# Valor Total de Factura
var_valor_total = StringVar()
# Observaciones
var_observaciones = StringVar()

def buscar_cliente():
    # Función para llenar los campos con los datos del cliente seleccionado
    def seleccionar_cliente():
        # Obtener el cliente seleccionado desde el Treeview
        item = tree.focus()
        if item:

            # Obtener los datos del cliente seleccionado
            cliente_seleccionado = tree.item(item, "values")

            # Rellenar los campos con los datos del cliente
            var_nombre.set(cliente_seleccionado[1])
            var_apellido1.set(cliente_seleccionado[2])
            var_apellido2.set(cliente_seleccionado[3])
            var_tel_contacto1.set(cliente_seleccionado[4])
            var_tel_contacto2.set(cliente_seleccionado[5])
            var_correo.set(cliente_seleccionado[6])
            var_dni_nie.set(cliente_seleccionado[7])
            var_direccion.set(cliente_seleccionado[8])
            var_codigo_postal.set(cliente_seleccionado[9])
            var_municipio.set(cliente_seleccionado[10])
            var_provincia.set(cliente_seleccionado[11])

            # Cerrar la ventana de búsqueda de clientes
            ventana_clientes.destroy()
        else:
            mb.showerror("Error", "Selecciona un cliente primero.")

    # Crear ventana para mostrar la lista de clientes
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Seleccionar Cliente")

    # Crear Treeview para mostrar la lista de clientes
    tree = ttk.Treeview(ventana_clientes)
    tree["columns"] = ("DNI/NIE", "Nombre", "Apellido1", "Apellido2")
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)
    tree.heading("DNI/NIE", text="DNI/NIE")
    tree.column("DNI/NIE", width=100)
    tree.heading("Nombre", text="Nombre")
    tree.column("Nombre", width=100)
    tree.heading("Apellido1", text="Apellido1")
    tree.column("Apellido1", width=100)
    tree.heading("Apellido2", text="Apellido2")
    tree.column("Apellido2", width=100)
    tree.grid(row=0, column=0, padx=10, pady=10)

    # Conectar a la base de datos y obtener los clientes
    conn = sqlite3.connect('Clientes.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM clientes")
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert("", "end", text=cliente[0], values=cliente[1:])
    conn.close()

    # Botón para seleccionar el cliente
    boton_seleccionar = tk.Button(ventana_clientes, text="Seleccionar Cliente", command=seleccionar_cliente)
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10)

def mostrar_vehiculos_asociados():
    def seleccionar_vehiculo():
        # Obtener el vehiculo seleccionado desde el Treeview
        item = tree.focus()
        if item:

            # Obtener los datos del vehiculo seleccionado
            vehiculo_seleccionado = tree.item(item, "values")

            # Rellenar los campos con los datos del vehiculo
            var_matricula.set(vehiculo_seleccionado[1])
            var_marca_vehiculo.set(vehiculo_seleccionado[2])
            var_modelo_vehiculo.set(vehiculo_seleccionado[3])
            
            # Cerrar la ventana de búsqueda de clientes
            ventana.destroy()
        else:
            mb.showerror("Error", "Selecciona un cliente primero.")

    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Vehículos Asociados al Cliente")

    # Crear Treeview
    tree = ttk.Treeview(ventana, columns=("Matrícula", "Marca", "Modelo", "Color"))
    tree.heading("#0", text="ID")
    tree.heading("Matrícula", text="Matrícula")
    tree.heading("Marca", text="Marca")
    tree.heading("Modelo", text="Modelo")
    tree.heading("Color", text="Color")
    tree.grid(row=0, column=0, padx=10, pady=10)

    # Obtener el DNI/NIE del cliente
    dni_cliente = var_dni_nie.get()
    
    # Consultar vehículos asociados al cliente
    conn = sqlite3.connect('Taller.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM vehiculos WHERE dni_cliente=?", (dni_cliente,))
    vehiculos = c.fetchall()
    
    for vehiculo in vehiculos:
        tree.insert("", "end", values=vehiculo[1:5])  # Agregar vehículo al Treeview, omitiendo el id_vehiculo

    conn.close()  # Cerrar la conexión con la base de datos
    boton_seleccionar = tk.Button( ventana, text="Seleccionar Vehiculo", command=seleccionar_vehiculo)
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10)
    ventana.mainloop()  # Agregar el mainloop para que la ventana se muestre

def mostrar_ordenes_trabajo():

    # Función para llenar el widget de orden de trabajo con la descripción del trabajo de la orden de trabajo seleccionada
    def seleccionar_orden_trabajo():

        # Obtener la orden de trabajo seleccionada desde el Treeview
        item = tree.focus()
        if item:

            # Obtener los detalles de la orden de trabajo seleccionada
            orden_seleccionada = tree.item(item, "values")

            # Mostrar la descripción del trabajo en el widget de orden de trabajo
            texto_orden_trabajo.delete(1.0, tk.END)  # Limpiar el contenido actual del widget
            texto_orden_trabajo.insert(tk.END, orden_seleccionada[3])  # Insertar la descripción del trabajo

            # Cerrar la ventana de búsqueda de órdenes de trabajo
            ventana_ordenes_trabajo.destroy()
        else:
            mb.showerror("Error", "Selecciona una orden de trabajo primero.")

    # Crear ventana para mostrar la lista de órdenes de trabajo
    ventana_ordenes_trabajo = tk.Toplevel()
    ventana_ordenes_trabajo.title("Seleccionar Orden de Trabajo")

    # Crear Treeview para mostrar la lista de órdenes de trabajo
    tree = ttk.Treeview(ventana_ordenes_trabajo)
    tree["columns"] = ("ID","DNI Cliente", "Matrícula", "Descripción Trabajo", "Estado Reparación", "Detalles")
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)
    tree.heading("DNI Cliente", text="DNI Cliente")
    tree.column("DNI Cliente", width=100)
    tree.heading("Matrícula", text="Matrícula")
    tree.column("Matrícula", width=100)
    tree.heading("Descripción Trabajo", text="Descripción Trabajo")
    tree.column("Descripción Trabajo", width=200)
    tree.heading("Estado Reparación", text="Estado Reparación")
    tree.column("Estado Reparación", width=150)
    tree.heading("Detalles", text="Detalles")
    tree.column("Detalles", width=300)
    tree.grid(row=0, column=0, padx=10, pady=10)

    # Conectar a la base de datos y obtener las órdenes de trabajo
    conn = sqlite3.connect('Taller.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM OrdenesTrabajo")
    ordenes_trabajo = c.fetchall()
    for orden in ordenes_trabajo:
        tree.insert("", "end", text=orden[0], values=orden[1:])
    conn.close()

    # Botón para seleccionar la orden de trabajo
    boton_seleccionar = tk.Button(ventana_ordenes_trabajo, text="Seleccionar Orden de Trabajo", command=seleccionar_orden_trabajo)
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10)

class FacturaPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Factura', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def obtener_datos_tabla():
    # Aquí obtienes los datos de la tabla que ya están almacenados en la variable datos_tabla
    return datos_tabla 

def generar_factura():

    #Campos factura id y fecha
    factura_id = {"Factura ID": var_factura_id.get()}
    fecha = {"Fecha": var_fecha.get()}

    # Campos datos Cliente
    nombre_cliente = {
        "Nombre": var_nombre.get(),
        "Apellido1": var_apellido1.get(),
        "Apellido2": var_apellido2.get()
    }
    contacto_cliente = {
        "Teléfono 1": var_tel_contacto1.get(),
        "Teléfono 2": var_tel_contacto2.get(),
        "Email": var_correo.get()
    }
    dni_nie_cliente = {"DNI/NIE": var_dni_nie.get()}
    calle_cliente = {"Dirección": var_direccion.get()}
    direccion_cliente = {
        "Código Postal": var_codigo_postal.get(),
        "Municipio": var_municipio.get(),
        "Provincia": var_provincia.get()
    }

    # Campos datos vehiculo 
    datos_vehiculo = {
        "Matricula": var_matricula.get(),
        "Marca": var_marca_vehiculo.get(),
        "Modelo": var_modelo_vehiculo.get()
    }
    
    datos_tabla=obtener_datos_tabla()
    
    # Obtiene la orden de trabajo del Text Widget
    orden_trabajo = texto_orden_trabajo.get("1.0", "end-1c")
    
    coste_total = var_coste_total.get()

    # Genera la factura PDF con los datos proporcionados
    generar_factura_pdf(factura_id,fecha,nombre_cliente, contacto_cliente, dni_nie_cliente,
                        calle_cliente, direccion_cliente, datos_vehiculo, orden_trabajo,datos_tabla,coste_total)
    mb.showinfo("Factura generada", "La factura ha sido generada y guardada correctamente.")

def generar_factura_pdf(factura_id,fecha,nombre_cliente, contacto_cliente, dni_nie_cliente,
                        calle_cliente, direccion_cliente, datos_vehiculo, orden_trabajo,datos_tabla,coste_total):
    factura = FacturaPDF()
    factura.add_page()
    
    # Información del taller
    factura.set_font('Arial', 'B', 16)
    factura.cell(0, 10, 'Taller Quirino Vallejera', 0, 1, 'C')
    factura.set_font('Arial', '', 12)
    factura.cell(0, 10, 'Dirección: C. Levante, 9, BAJO, CP:34004 ,Palencia', 0, 1, 'C')
    factura.cell(0, 10, 'Teléfono: 979 72 31 91', 0, 1, 'C')
    y=5
    x=20

    #Añadir Factura ID y Fecha....??
    factura.set_font('Arial', 'B', 10)
    factura.cell(x, y, 'Factura ID:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 20, y, factura_id["Factura ID"], 0, 0)
    factura.set_font('Arial', 'B', 10)
    factura.cell(x , y, 'Fecha:',0,0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 5, y, fecha["Fecha"], 0, 0)
    
    # Espacio entre información del taller y datos del cliente
    factura.ln(10)
    # Escribir datos del cliente
    
    factura.set_font('Arial', 'B', 12)
    factura.cell(0, 10, 'DATOS DEL CLIENTE', 0, 1, 'C')
    factura.set_font('Arial', '', 10)
    
    # Coordenadas iniciales
    x = 20
    y = 10
    
    # Escribir nombre del cliente
    # Escribir nombre del cliente
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x, y, 'Nombre:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, nombre_cliente["Nombre"], 0, 0)

    # Escribir apellidos del cliente
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 2, y, 'Apellido1:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 2, y, nombre_cliente["Apellido1"], 0, 0)
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 2, y, 'Apellido2:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 2, y, nombre_cliente["Apellido2"], 0, 0)

# Ajustar la posición Y para la próxima fila de datos
    y += 5
    factura.ln(5)

    x = 25
    # Escribir datos de contacto del cliente
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 10
    factura.cell(x, y, 'Teléfono 1:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, contacto_cliente["Teléfono 1"], 0, 0)
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 1, y, 'Teléfono 2:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 3, y, contacto_cliente["Teléfono 2"], 0, 0)
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 5, y, 'Email:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(1 , y, contacto_cliente["Email"], 0, 0)

# Ajustar la posición Y para la próxima fila de datos
    y += 5
    factura.ln(5)
# Escribir DNI/NIE del cliente
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x, y, 'DNI/NIE:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 20, y, dni_nie_cliente["DNI/NIE"], 0, 0)

# Ajustar la posición Y para la próxima fila de datos
    y += 5
    factura.ln(5)
# Escribir dirección del cliente
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x, y, 'Dirección:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, calle_cliente["Dirección"], 0, 0)

# Ajustar la posición Y para la próxima fila de datos
    y += 5
    factura.ln(5)
# Escribir datos de la dirección del cliente
    x = 30
    factura.set_font('Arial', 'B', 10)
    factura.cell(x, y, 'Código Postal:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 10, y, direccion_cliente["Código Postal"], 0, 0)
    x=20
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 5, y, 'Municipio:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 10, y, direccion_cliente["Municipio"], 0, 0)
    factura.set_font('Arial', 'B', 10)
    factura.cell(x + 5, y, 'Provincia:', 0, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(x + 10, y, direccion_cliente["Provincia"], 0, 0)
    factura.ln(15)
    y = 100
    # Escribir datos del vehículo
    factura.set_font('Arial', 'B', 12)
    factura.cell(0, 20, 'DATOS DE VEHÍCULO', 0, 1, 'C')
    factura.set_font('Arial', '', 10)
    #factura.ln(10)
    x = 20
 #Datos Vehiculo
    y = 10
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x, y, 'Matricula:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, datos_vehiculo["Matricula"], 0, 0)
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x + 5 , y, 'Marca:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, datos_vehiculo["Marca"], 0, 0)
    factura.set_font('Arial', 'B', 10)  # Establece la fuente Arial, negrita, tamaño 12
    factura.cell(x + 5 , y, 'Modelo:', 0, 0)
    factura.set_font('Arial', '', 12)  # Restablece la fuente Arial, tamaño 12 (sin negrita)
    factura.cell(x + 5, y, datos_vehiculo["Modelo"], 0, 0)

    # Espacio entre datos del vehículo y orden de trabajo
    factura.ln(10)
    # Escribir orden de trabajo
    factura.set_font('Arial', 'B', 12)
    factura.cell(0, 10, 'Trabajo realizado', 0, 1, 'C')
    factura.set_font('Arial', '', 10)
    factura.multi_cell(0, 10, orden_trabajo)

    # Dibujar la tabla
    if datos_tabla:
    # Espacio entre orden de trabajo y datos de la tabla
        factura.ln(5)
    
    # Título de la tabla
        factura.set_font('Arial', 'B', 12)
        factura.cell(200, 10, 'Datos de la tabla', ln=True, align='C')
        factura.set_font('Arial', '', 12)
    
    # Cabecera de la tabla
        for col in header:
        # Si la columna es "Concepto", expande su ancho a 60 para ocupar dos columnas
            if col == "Concepto":
                factura.cell(50, 10, col, border=1)
            else:
                factura.cell(25, 10, col, border=1)
        factura.ln()
    
    # Datos de la tabla

        for fila in datos_tabla:
            for i, valor in enumerate(fila):
            # Si es la tercera columna (Concepto), usar el ancho específico
                if i == 2:
                    factura.set_font('Arial', '', 10)
                    factura.cell(50,10, str(valor), border=1)
                else:
                    factura.set_font('Arial', '', 10)
                    factura.cell(25, 10, str(valor), border=1)
            factura.ln()
    
    #posicion inicial
    factura.ln(5)
    x = 20
    y = 10
    # Escribir el coste total con IVA al final de la factura
    factura.set_font('Arial', 'B', 10)
    factura.cell(50, y, 'Coste Total con 21% IVA:', 1, 0)
    factura.set_font('Arial', '', 12)
    factura.cell(20, y, coste_total, 1, 1)
    
    factura.ln(10)
    
    #Firma cliente
    factura.set_font('Arial', 'B', 10)
    factura.cell(100, 10, 'Firma Cliente', 1, 0)
    
    #Firma y sello  Empresa
    factura.set_font('Arial', 'B', 10)
    factura.cell(100, 10, 'Firma y Sello Empresa', 1, 1)
   
    # Guardar factura como PDF
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
    if nombre_archivo:
        factura.output(nombre_archivo)

#VENTANA TKINTER
# Crear Logo
logo_image = Image.open('./iconos y logo/logo.png')
logo_photo = ImageTk.PhotoImage(logo_image.resize((900, 168), Image.Resampling.LANCZOS))
logo_label = Label(ventana, image=logo_photo, bg='white')
logo_label.image = logo_photo
logo_label.grid(pady=20)

# Datos taller
datos_taller = Label(ventana, text=' Taller QUIRINO VALLEJERA   Dirección: C. Levante, 9, BAJO, CP:34004 ,Palencia ,Teléfono: 979 72 31 91  ', font=('Arial', 12, 'bold'))
datos_taller.grid(row=1, column=0, columnspan=6, pady=10)

# Marco de ID Factura...
marco_id_factura = Frame(ventana)
marco_id_factura.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
marco_id_factura.configure(background='white')

# Titulo Factura
titulo = Label(marco_id_factura, text='Detalles de la factura', font=('Arial', 16, 'bold'))
titulo.grid(row=2, column=0, columnspan=6, pady=10)
titulo.configure(background='white', foreground='#311B92')

# Factura Etiquetas Cajas de texto
etiqueta_id_factura = Label(marco_id_factura, text='Factura ID :', font=('Arial', 12))
etiqueta_id_factura.grid(row=3, column=0, pady=5, padx=10, sticky='w')
etiqueta_id_factura.configure(background='white', foreground='#311B92')
cajatexto_id_factura = Entry(marco_id_factura, textvariable=var_factura_id)
cajatexto_id_factura.grid(row=3, column=1, pady=5, padx=10, sticky='e')
cajatexto_id_factura.configure(background='white', foreground='black')

# Fecha
etiqueta_id_factura = Label(marco_id_factura, text='Fecha :', font=('Arial', 12))
etiqueta_id_factura.grid(row=3, column=2, pady=5, padx=10, sticky='w')
etiqueta_id_factura.configure(background='white', foreground='#311B92')
cajatexto_id_factura = Entry(marco_id_factura, textvariable=var_fecha)
cajatexto_id_factura.grid(row=3, column=3, pady=5, padx=10, sticky='e')
cajatexto_id_factura.configure(background='white', foreground='black')

# Marco datos clientes
marco_datos_cliente = Frame(ventana)
marco_datos_cliente.grid(row=3, column=0, columnspan=6, padx=10, pady=10)
marco_datos_cliente.configure(background='white')

# Label Titulo
titulo = Label(marco_datos_cliente, text='DATOS CLIENTE', font=('Arial', 16, 'bold'))
titulo.grid(row=0, column=0, columnspan=6, pady=10)
titulo.configure(background='white', foreground='#311B92')

# Etiquetas y cajas de texto
# Etiqueta Nombre
etiqueta_nombre = Label(marco_datos_cliente, text='Nombre:', font=('Arial', 12))
etiqueta_nombre.grid(row=1, column=0, pady=5, padx=10, sticky='w')
etiqueta_nombre.configure(background='white', foreground='#311B92')
cajatexto_nombre = Entry(marco_datos_cliente, textvariable=var_nombre)
cajatexto_nombre.grid(row=1, column=1, pady=5, padx=10, sticky='e')
cajatexto_nombre.configure(background='white', foreground='black')

# Etiqueta Apellido 1
etiqueta_apellido1 = Label(marco_datos_cliente, text='Apellido 1 :', font=('Arial', 12))
etiqueta_apellido1.grid(row=1, column=2, pady=5, padx=10, sticky='w')
etiqueta_apellido1.configure(background='white', foreground='#311B92')
cajatexto_apellido1 = Entry(marco_datos_cliente, textvariable=var_apellido1)
cajatexto_apellido1.grid(row=1, column=3, pady=5, padx=10, sticky='e')
cajatexto_apellido1.configure(background='white', foreground='black')

# Etiqueta Apellido 2
etiqueta_apellido2 = Label(marco_datos_cliente, text='Apellido 2 :', font=('Arial', 12))
etiqueta_apellido2.grid(row=1, column=4, pady=5, padx=10, sticky='w')
etiqueta_apellido2.configure(background='white', foreground='#311B92')
cajatexto_apellido2 = Entry(marco_datos_cliente, textvariable=var_apellido2)
cajatexto_apellido2.grid(row=1, column=5, pady=5, padx=10, sticky='e')
cajatexto_apellido2.configure(background='white', foreground='black')

# Etiqueta Telefono contacto 1
etiqueta_tel_contacto1 = Label(marco_datos_cliente, text='Telefono 1 :', font=('Arial', 12))
etiqueta_tel_contacto1.grid(row=2, column=0, pady=5, padx=10, sticky='w')
etiqueta_tel_contacto1.configure(background='white', foreground='#311B92')
cajatexto_tel_contacto1 = Entry(marco_datos_cliente, textvariable=var_tel_contacto1)
cajatexto_tel_contacto1.grid(row=2, column=1, pady=5, padx=10, sticky='e')
cajatexto_tel_contacto1.configure(background='white', foreground='black')

# Etiqueta Telefono contacto 2
etiqueta_tel_contacto2 = Label(marco_datos_cliente, text='Telefono 2 :', font=('Arial', 12))
etiqueta_tel_contacto2.grid(row=2, column=2, pady=5, padx=10, sticky='w')
etiqueta_tel_contacto2.configure(background='white', foreground='#311B92')
cajatexto_tel_contacto2 = Entry(marco_datos_cliente, textvariable=var_tel_contacto2)
cajatexto_tel_contacto2.grid(row=2, column=3, pady=5, padx=10, sticky='e')
cajatexto_tel_contacto2.configure(background='white', foreground='black')

# Etiqueta Correo Electronico
etiqueta_correo = Label(marco_datos_cliente, text='Email :', font=('Arial', 12))
etiqueta_correo.grid(row=2, column=4, pady=5, padx=10, sticky='w')
etiqueta_correo.configure(background='white', foreground='#311B92')
cajatexto_correo = Entry(marco_datos_cliente, textvariable=var_correo)
cajatexto_correo.grid(row=2, column=5, pady=5, padx=10, sticky='e')
cajatexto_correo.configure(background='white', foreground='black')

# Etiqueta DNI/NIE
etiqueta_dni_nie = Label(marco_datos_cliente, text='DNI/NIE :', font=('Arial', 12))
etiqueta_dni_nie.grid(row=3, column=0, pady=5, padx=10, sticky='w')
etiqueta_dni_nie.configure(background='white', foreground='#311B92')
cajatexto_dni_nie = Entry(marco_datos_cliente, textvariable=var_dni_nie)
cajatexto_dni_nie.grid(row=3, column=1, pady=5, padx=10, sticky='e')
cajatexto_dni_nie.configure(background='white', foreground='black')

# Etiqueta Direccion
etiqueta_direccion = Label(marco_datos_cliente, text='Direccion :', font=('Arial', 12))
etiqueta_direccion.grid(row=4, column=0, pady=5, padx=10, sticky='w')
etiqueta_direccion.configure(background='white', foreground='#311B92')
cajatexto_direccion = Entry(marco_datos_cliente, textvariable=var_direccion)
cajatexto_direccion.grid(row=4, column=1, columnspan=5, pady=5, padx=10, sticky='ew')
cajatexto_direccion.configure(background='white', foreground='black')

# Etiqueta Codigo postal
etiqueta_codigo_postal = Label(marco_datos_cliente, text='Codigo Postal :', font=('Arial', 12))
etiqueta_codigo_postal.grid(row=5, column=0, pady=5, padx=10, sticky='w')
etiqueta_codigo_postal.configure(background='white', foreground='#311B92')
cajatexto_codigo_postal = Entry(marco_datos_cliente, textvariable=var_codigo_postal)
cajatexto_codigo_postal.grid(row=5, column=1, pady=5, padx=10, sticky='e')
cajatexto_codigo_postal.configure(background='white', foreground='black')

# Etiqueta Municipio
etiqueta_municipio = Label(marco_datos_cliente, text='Municipio :', font=('Arial', 12))
etiqueta_municipio.grid(row=5, column=2, pady=5, padx=10, sticky='w')
etiqueta_municipio.configure(background='white', foreground='#311B92')
cajatexto_municipio = Entry(marco_datos_cliente, textvariable=var_municipio)
cajatexto_municipio.grid(row=5, column=3, pady=5, padx=10, sticky='e')
cajatexto_municipio.configure(background='white', foreground='black')

# Etiqueta Provincia
etiqueta_provincia = Label(marco_datos_cliente, text='Provincia :', font=('Arial', 12))
etiqueta_provincia.grid(row=5, column=4, pady=5, padx=10, sticky='w')
etiqueta_provincia.configure(background='white', foreground='#311B92')
cajatexto_provincia = Entry(marco_datos_cliente, textvariable=var_provincia)
cajatexto_provincia.grid(row=5, column=5, pady=5, padx=10, sticky='e')
cajatexto_provincia.configure(background='white', foreground='black')

# Datos Vehiculo ##################
# Marco Vehiculos
marco_datos_vehiculo = Frame(ventana)
marco_datos_vehiculo.grid(row=6, column=0, columnspan=6, padx=10, pady=10)
marco_datos_vehiculo.configure(background='white')

# Label Titulo
titulo = Label(marco_datos_vehiculo, text='Datos vehiculo', font=('Arial', 16, 'bold'))
titulo.grid(row=0, column=0,columnspan=6, pady=10)
titulo.configure(background='white', foreground='#311B92')

# Etiquetas y cajas de texto
# Etiqueta Matricula
etiqueta_matricula = Label(marco_datos_vehiculo, text='Matricula:', font=('Arial', 12))
etiqueta_matricula.grid(row=7, column=0, pady=5, padx=5, sticky='e')
etiqueta_matricula.configure(background='white', foreground='#311B92')
cajatexto_matricula = Entry(marco_datos_vehiculo, textvariable=var_matricula)
cajatexto_matricula.grid(row=7, column=1, pady=5, padx=5, sticky='e')
cajatexto_matricula.configure(background='white', foreground='black')

# Etiqueta marca vehiculo
etiqueta_matricula = Label(marco_datos_vehiculo, text='Marca vehiculo:', font=('Arial', 12))
etiqueta_matricula.grid(row=7, column=2, pady=5, padx=5, sticky='e')
etiqueta_matricula.configure(background='white', foreground='#311B92')
cajatexto_matricula = Entry(marco_datos_vehiculo, textvariable=var_marca_vehiculo)
cajatexto_matricula.grid(row=7, column=3, pady=5, padx=5, sticky='e')
cajatexto_matricula.configure(background='white', foreground='black')

# Etiqueta Modelo vehiculo
etiqueta_matricula = Label(marco_datos_vehiculo, text='Modelo vehiculo :', font=('Arial', 12))
etiqueta_matricula.grid(row=7, column=4, pady=5, padx=5, sticky='e')
etiqueta_matricula.configure(background='white', foreground='#311B92')
cajatexto_matricula = Entry(marco_datos_vehiculo, textvariable=var_modelo_vehiculo)
cajatexto_matricula.grid(row=7, column=5, pady=5, padx=5, sticky='e')
cajatexto_matricula.configure(background='white', foreground='black')

#Crear Orden De Trabajo
marco_orden_trabajos=Frame(ventana)
marco_orden_trabajos.grid(row=8,column=0,columnspan=6,padx=10,pady=10)
marco_orden_trabajos.configure(background='white')

# Label Titulo
titulo = Label(marco_orden_trabajos, text='Trabajos relizados', font=('Arial', 16, 'bold'))
titulo.grid(row=8, column=0,columnspan=6, pady=10)
titulo.configure(background='white', foreground='#311B92')

def crear_widget_orden_trabajo():
    texto_orden_trabajo = tk.Text(marco_orden_trabajos, height=3, width=100)
    texto_orden_trabajo.grid(row=9, column=0, columnspan=6, padx=10, pady=10)
    return texto_orden_trabajo

texto_orden_trabajo = crear_widget_orden_trabajo()

#CREAR TABLA 

#Estructura de la tabla
def crear_tabla(frame, header, datos_tabla):
    # Crea las etiquetas para el encabezado
    for i, col in enumerate(header):
        if col == "Concepto":
            etiqueta = tk.Label(frame, text=col, borderwidth=2, relief="solid", width=30)
        else:
            etiqueta = tk.Label(frame, text=col, borderwidth=2, relief="solid", width=10)
        etiqueta.grid(row=0, column=i, sticky="nsew")

    # Crea las etiquetas para los datos de la tabla
    for i, fila in enumerate(datos_tabla):
        for j, valor in enumerate(fila):
            etiqueta = tk.Label(frame, text=valor, borderwidth=1, relief="solid", width=10)
            etiqueta.grid(row=i+1, column=j, sticky="nsew")

def actualizar_tabla(nueva_fila, datos_tabla):
    datos_tabla.append(nueva_fila)
    crear_tabla(frame_tabla, header, datos_tabla)

def agregar_datos_ventana():
    ventana = tk.Toplevel()
    ventana.title("Agregar Datos")
    
    ventana.campos = []

    for i, col in enumerate(header):
        tk.Label(ventana, text=col).grid(row=0, column=i)
        campo = tk.Entry(ventana)
        campo.grid(row=1, column=i)
        ventana.campos.append(campo)

    def agregar_fila():
        nueva_fila = [campo.get() for campo in ventana.campos]
        cantidad = float(nueva_fila[1])
        precio = float(nueva_fila[3])
        descuento = float(nueva_fila[4])
        total = cantidad * precio * (1 - descuento / 100)
        nueva_fila[5] = total
        actualizar_tabla(nueva_fila, datos_tabla)
        ventana.destroy()

    boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_fila)
    boton_agregar.grid(row=2, columnspan=len(header), sticky="ew")

def abrir_ventana_agregar():
    agregar_datos_ventana()

#Crear frame para la tabla
frame_tabla = tk.Frame(ventana)
frame_tabla.grid(row=12, column=0,padx=10,pady=10, sticky='ew')
  # Coloca el frame en la fila 0 y columna 0 de la ventana

header = ['Referencia', 'Cantidad', 'Concepto', 'Precio', 'Descuento', 'Total']
datos_tabla = []

# Crear la tabla en el frame
crear_tabla(frame_tabla, header, datos_tabla)

import csv
def guardar_csv(frame, header,datos_tabla):
    # Obtener la ubicación y nombre del archivo CSV
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])

    if nombre_archivo:
        try:
            with open(nombre_archivo, 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir los encabezados de columna
                writer.writerow(header)
                # Escribir los datos de la tabla en el archivo CSV
                writer.writerows(datos_tabla)
            mb.showinfo("Guardado exitoso", "Los datos se han guardado correctamente en el archivo CSV.")
        except Exception as e:
            mb.showerror("Error al guardar", f"No se pudo guardar el archivo CSV.\nError: {str(e)}")
    else:
        mb.showinfo("Operación cancelada", "La operación de guardado ha sido cancelada.")
    
#Total FACTURA
def mostrar_ventana_costo_total():
    global datos_tabla  # Declarar datos_tabla como global

    # Definir la función para calcular el costo total con IVA
    def calcular_costo_total():
        total_factura = 0

        # Sumar el total de cada fila
        for fila in datos_tabla:
            total_factura += fila[5]  # Considerando que la columna 5 contiene el total de cada fila

        # Agregar el 21% de IVA
        total_con_iva = total_factura * 1.21

        return total_con_iva

    # Crear ventana
    ventana_costo_total = tk.Toplevel()
    ventana_costo_total.title("Costo Total con IVA")
    ventana_costo_total.geometry("300x300")

    # Calcular el costo total con IVA
    costo_total_iva = calcular_costo_total()

    # Mostrar el costo total con IVA
    etiqueta_costo_total_iva = tk.Label(ventana_costo_total, text=f"Costo Total con IVA: {costo_total_iva}")
    etiqueta_costo_total_iva.grid(row=0, column=0, padx=10, pady=10)

    # Botón para guardar el costo total con IVA en una variable
    def guardar_costo_total():
        # Guardar el costo total con IVA en una variable global
        global var_coste_total
        var_coste_total.set(costo_total_iva)
        ventana_costo_total.destroy()

    boton_guardar = tk.Button(ventana_costo_total, text="Guardar Costo Total", command=guardar_costo_total)
    boton_guardar.grid(row=1, column=0,padx=10,pady=10)

var_coste_total=StringVar()

# Marco Botones
marco_botones = Frame(ventana)
marco_botones.grid(row=10, column=0, columnspan=7, padx=10, pady=10)
marco_botones.configure(background='white')

#Boton buscar Ciente
boton_buscar_cliente=tk.Button(marco_botones, text='Buscar Cliente',command=buscar_cliente)
boton_buscar_cliente.grid(row=10, column=1,pady=10)

# Botón para guardar en PDF
boton_guardar_pdf = tk.Button(marco_botones, text="Guardar en PDF", command=generar_factura)
boton_guardar_pdf.grid(row=10, column=0, pady=10)

# Botón para guardar en PDF
boton_guardar_csv = tk.Button(marco_botones, text="Guardar CSV", command=lambda: guardar_csv(frame_tabla,header,datos_tabla))
boton_guardar_csv.grid(row=10, column=2)

# Botón para agregar datos
boton_agregar = tk.Button(marco_botones, text="Agregar datos tabla", command=abrir_ventana_agregar)
boton_agregar.grid(row=10, column=3)

boton_agregar_ordenes=tk.Button(marco_botones,text='Añadir trabajos',command=mostrar_ordenes_trabajo)
boton_agregar_ordenes.grid(row=10, column=4)

boton_buscar_vehiculos=tk.Button(marco_botones,text='Buscar vehiculos',command=mostrar_vehiculos_asociados)
boton_buscar_vehiculos.grid(row=10,column=5)

#Boton coste total
boton_total=tk.Button(marco_botones, text='Total Factura', command=mostrar_ventana_costo_total)
boton_total.grid(row=10, column=7, padx=10, pady=10)

def salir():
    ventana.destroy()

boton_salir = tk.Button(ventana, text="Salir", command=salir, bg="red", fg="white", font=("Arial", 12, "bold"))
boton_salir.place(relx=0.9, rely=0.9, anchor="se")

ventana.mainloop()
