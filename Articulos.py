from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import date
import os
import  subprocess
# Configuración inicial
def abrir_almacen():
    ventana.destroy()  # Cierra la ventana actual
    subprocess.run(['python', 'Almacen.py'], creationflags=subprocess.CREATE_NO_WINDOW)


conexion = sqlite3.connect("Taller.db")
cursor = conexion.cursor()
conexion.commit()

def validar_campos():
    campos = {
        "Referencia de fabricante": var_referencia_fabricante.get(),
        "Descripción": var_descripcion.get(),
        "Unidades": var_unidades.get(),
        "Precio de compra": var_precio_compra.get(),
        "Precio de venta": var_precio_venta.get(),
        "Albarán": var_albaran.get(),
        "Imagen": var_imagen.get()
    }

    campos_incompletos = [campo for campo, valor in campos.items() if not valor]

    if campos_incompletos:
        mb.showerror("Campos incompletos", f"Por favor, complete los siguientes campos: {', '.join(campos_incompletos)}")
        return False

    if seleccion_familia.get() == "Seleccionar familia":
        mb.showerror("Selección incompleta", "Por favor, seleccione una familia.")
        return False

    if seleccion_vehiculo.get() == "Seleccionar vehículo":
        mb.showerror("Selección incompleta", "Por favor, seleccione un vehículo.")
        return False

    if seleccion_distribuidor.get() == "Seleccionar distribuidor":
        mb.showerror("Selección incompleta", "Por favor, seleccione un distribuidor.")
        return False

    return True

def cargar_contador():
    if os.path.exists('contador_imagenes.txt'):
        with open('contador_imagenes.txt', 'r') as archivo:
            return int(archivo.read().strip())
    return 0

contador_imagenes = cargar_contador()

def guardar_contador(contador):
    with open('contador_imagenes.txt', 'w') as archivo:
        archivo.write(str(contador))
        
def generar_referencia_interna():
    inicial_familia = seleccion_familia.get()[:1].upper()
    inicial_vehiculo = seleccion_vehiculo.get()[:1].upper()
    referencia_interna = f"{inicial_familia}{inicial_vehiculo}{contador_imagenes}"
    
    return referencia_interna

def actualizar_referencia_interna(event=None):
    inicial_familia = seleccion_familia.get()[:1].upper() if seleccion_familia.get() else ""
    inicial_vehiculo = seleccion_vehiculo.get()[:1].upper() if seleccion_vehiculo.get() else ""
    referencia_interna.set(f"{inicial_familia}{inicial_vehiculo}{contador_imagenes+1}")
    
def seleccionar_imagen():
    inicial_familia = seleccion_familia.get()[:1].upper()
    inicial_vehiculo = seleccion_vehiculo.get()[:1].upper()
    global contador_imagenes, img_label
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagenes", "*.png; *.jpg; *.jpeg; *.gif")])
    if ruta_imagen:
        #nombre_imagen = f"imagen_{contador_imagenes + 1}.jpg"
        nombre_imagen = f"{inicial_familia}{inicial_vehiculo}{contador_imagenes+1}.jpg"
        ruta_destino = f"articulos/{nombre_imagen}"
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((350, 350), Image.Resampling.LANCZOS)
        imagen.save(ruta_destino, 'JPEG')
        contador_imagenes += 1
        guardar_contador(contador_imagenes)
        var_imagen.set(ruta_destino)
        miniatura = Image.open(ruta_destino).resize((100, 100), Image.Resampling.LANCZOS)
        miniatura_img = ImageTk.PhotoImage(miniatura)
        img_label.config(image=miniatura_img)
        img_label.image = miniatura_img

def validar_unidades(event=None):
    input_value = var_unidades.get().strip()
    try:
        valor = int(input_value)
        if valor <= 0:
            mb.showerror("Error de validación", "La cantidad de unidades debe ser un número positivo.")
            var_unidades.set('')
            return False
    except ValueError:
        mb.showerror("Error de validación", "La cantidad de unidades debe ser un número entero.")
        var_unidades.set('')
        return False
    return True

def validar_precio(event=None, var=None, nombre_campo=""):
    input_value = var.get().strip() if isinstance(var.get(), str) else str(var.get())
    try:
        precio = float(input_value)
        if precio < 0:
            mb.showerror("Error de validación", f"El {nombre_campo} debe ser un número positivo.")
            var.set('')
            return False
    except ValueError:
        mb.showerror("Error de validación", f"El {nombre_campo} debe ser un valor numérico.")
        var.set('')
        return False
    return True

def guardar_en_base_de_datos():
    referencia_interna = generar_referencia_interna()
    
    if not validar_campos():
        return

    if not (validar_unidades() and validar_precio(var=var_precio_compra, nombre_campo="precio de compra") and validar_precio(var=var_precio_venta, nombre_campo="precio de venta")):
        return
    try:
        datos = (var_referencia_fabricante.get(), referencia_interna, var_descripcion.get(), var_unidades.get(),
                 var_precio_compra.get(), var_precio_venta.get(), date.today().strftime('%Y-%m-%d'),
                 seleccion_distribuidor.get(), var_albaran.get(), var_imagen.get())
        cursor.execute('''INSERT INTO articulos (referencia_fabricante, referencia_interna, descripcion, unidades, precio_compra, precio_venta, fecha_alta, nombre_distribuidor, albaran, imagen)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', datos)
        conexion.commit()
        mb.showinfo("Éxito", "Artículo guardado correctamente.")
        reset_campos()
    except Exception as e:
        mb.showerror("Error", "No se pudo guardar el artículo. Error: " + str(e))
def reset_campos():
    for var in [var_referencia_fabricante, var_descripcion, var_unidades, var_precio_compra, var_precio_venta, var_albaran, var_imagen]:
        var.set("")
    seleccion_familia.set("Seleccionar familia")
    seleccion_vehiculo.set("Seleccionar vehículo")
    seleccion_distribuidor.set("Seleccionar distribuidor")
    img_label.image = None

ventana = Tk()
ventana.title("Gestión de Artículos")
ventana.geometry("1000x800")
ventana.configure(bg="white")
ventana.iconbitmap("./iconos y logo/icono.ico")

logo_path = "./iconos y logo/logo.jpg"
logo = Image.open(logo_path)
logo = logo.resize((900, 100), Image.Resampling.LANCZOS)
logo_img = ImageTk.PhotoImage(logo)
logo_label = Label(ventana, image=logo_img, bg="white")
logo_label.pack(pady=10)

frame = LabelFrame(ventana, text="Datos del Artículo", bg="white", fg="#311B92", font=("Arial", 14))
frame.pack(fill="both", expand="yes", padx=20, pady=20)

var_referencia_fabricante = StringVar()
var_descripcion = StringVar()
var_unidades = StringVar()
var_precio_compra = StringVar()
var_precio_venta = StringVar()
var_albaran = StringVar()
var_imagen = StringVar()
referencia_interna = StringVar()

labels = ["Referencia de fabricante", "Descripción", "Unidades", "Precio de compra", "Precio de venta", "Albarán"]
variables = [var_referencia_fabricante, var_descripcion, var_unidades, var_precio_compra, var_precio_venta, var_albaran]
entries = []

for i, (label, var) in enumerate(zip(labels, variables)):
    Label(frame, text=label, bg="white", fg="#311B92", font=("Arial", 14)).grid(row=i, column=0, sticky=W, padx=10, pady=10)
    entry = Entry(frame, textvariable=var, font=("Arial", 14))
    entry.grid(row=i, column=1, sticky=W, padx=10, pady=10)
    entries.append(entry)
    if label == "Unidades":
        entry.bind("<FocusOut>", validar_unidades)
    elif label in ["Precio de compra", "Precio de venta"]:
        entry.bind("<FocusOut>", lambda e, var=var, label=label.lower(): validar_precio(event=e, var=var, nombre_campo=label))

opciones_familia = ["Neumáticos", "Frenos", "Motor", "Amortiguación", "Filtros", "Embrague", "Carrocería", "Suspensión", "Correas", "Aceites", "Escape", "Otras categorías"]
seleccion_familia = ttk.Combobox(frame, values=opciones_familia, state="readonly", font=("Arial", 14))
seleccion_familia.grid(row=0, column=3, padx=10, pady=10)
seleccion_familia.set("Seleccionar familia")

opciones_vehiculo = ["Motocicleta", "Coche", "Furgoneta", "Camión"]
seleccion_vehiculo = ttk.Combobox(frame, values=opciones_vehiculo, state="readonly", font=("Arial", 14))
seleccion_vehiculo.grid(row=1, column=3, padx=10, pady=10)
seleccion_vehiculo.set("Seleccionar vehículo")
Label(frame, text="Referencia Interna:", bg="white", fg="#311B92", font=("Arial", 14)).grid(row=2, column=2, sticky=E, padx=10, pady=10)
Entry(frame, textvariable=referencia_interna, font=("Arial", 12)).grid(row=2, column=3, sticky=W, padx=10, pady=10)
seleccion_familia.bind("<<ComboboxSelected>>", actualizar_referencia_interna)
seleccion_vehiculo.bind("<<ComboboxSelected>>", actualizar_referencia_interna)
actualizar_referencia_interna()
cursor.execute("SELECT DISTINCT nombre FROM distribuidores;")
distribuidores = [x[0] for x in cursor.fetchall()]
seleccion_distribuidor = ttk.Combobox(frame, values=distribuidores, state="readonly", font=("Arial", 14))
seleccion_distribuidor.grid(row=6, column=1, padx=10, pady=10)
seleccion_distribuidor.set("Seleccionar distribuidor")

img_label = Label(frame, bg="white")
img_label.grid(row=7, column=3, padx=10, pady=10)

Button(frame, text="Seleccionar imagen", command=seleccionar_imagen, font=("Arial", 14), bg="#311B92", fg="white").grid(row=7, column=0, padx=10, pady=10)
Entry(frame, textvariable=var_imagen, font=("Arial", 12)).grid(row=7, column=1, sticky=W, padx=10, pady=10)

Button(frame, text="Guardar", command=guardar_en_base_de_datos, font=("Arial", 14), bg="#311B92", fg="white").grid(row=8, column=0, padx=10, pady=10)
Button(frame, text="Salir", command=abrir_almacen, font=("Arial", 14), bg="red", fg="white").grid(row=15, column=3, padx=10, pady=20)

ventana.mainloop()
