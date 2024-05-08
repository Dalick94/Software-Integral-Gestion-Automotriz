import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import messagebox
import datetime
import os
from tkinter import filedialog
import subprocess

def open_menu_clientes():
    subprocess.Popen(['python', 'menu clientes.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    ventana.destroy()


def agregar_vehiculo():
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Vehiculo")
    global foto_vehiculo_add
    
    tk.Label(ventana_agregar, text="matricula:").grid(row=0, column=0, padx=10, pady=5)
    matricula_add = tk.Entry(ventana_agregar)
    matricula_add.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="numero_bastidor:").grid(row=1, column=0, padx=10, pady=5)
    numero_bastidor_add = tk.Entry(ventana_agregar)
    numero_bastidor_add.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="marca:").grid(row=2, column=0, padx=10, pady=5)
    marca_add = tk.Entry(ventana_agregar)
    marca_add.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="modelo:").grid(row=3, column=0, padx=10, pady=5)
    modelo_add = tk.Entry(ventana_agregar)
    modelo_add.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="version:").grid(row=4, column=0, padx=10, pady=5)
    version_add = tk.Entry(ventana_agregar)
    version_add.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="codigo_motor:").grid(row=5, column=0, padx=10, pady=5)
    codigo_motor_add = tk.Entry(ventana_agregar)
    codigo_motor_add.grid(row=5, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="planta motriz:").grid(row=6, column=0, padx=10, pady=5)
    opciones_planta_motriz = ['Gasolina', 'Diésel', 'FULL HYBRID', 'HEV', 'MHEV', 'Eléctrico 100%']
    planta_motriz_var = tk.StringVar()
    planta_motriz_combo = ttk.Combobox(ventana_agregar, textvariable=planta_motriz_var, values=opciones_planta_motriz, state="readonly")
    planta_motriz_combo.grid(row=6, column=1, padx=10, pady=5)
    planta_motriz_combo.current(0) 
    
    tk.Label(ventana_agregar, text="kilometros:").grid(row=7, column=0, padx=10, pady=5)
    kilometros_add = tk.Entry(ventana_agregar)
    kilometros_add.grid(row=7, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="etiqueta_medioambiental:").grid(row=8, column=0, padx=10, pady=5)
    etiqueta_medioambiental_add = tk.Entry(ventana_agregar)
    etiqueta_medioambiental_add.grid(row=8, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="fecha_itv_ok:").grid(row=9, column=0, padx=10, pady=5)
    fecha_itv_ok_add = tk.Entry(ventana_agregar)
    fecha_itv_ok_add.grid(row=9, column=1, padx=10, pady=5)
    
    tk.Label(ventana_agregar, text="color_carroceria :").grid(row=10, column=0, padx=10, pady=5)
    color_carroceria_add = tk.Entry(ventana_agregar)
    color_carroceria_add.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Seleccionar imagen:").grid(row=11, column=0, padx=10, pady=5)
    boton_imagen = tk.Button(ventana_agregar, text="Elegir imagen", command=lambda: seleccionar_imagen(ventana_agregar, numero_bastidor_add))
    boton_imagen.grid(row=11, column=1, padx=10, pady=5)

    # Entry para mostrar la ruta de la imagen seleccionada
    foto_vehiculo_add = tk.Entry(ventana_agregar)
    foto_vehiculo_add.grid(row=11, column=2, padx=10, pady=5)

    tk.Label(ventana_agregar, text="comentario_descripcion :").grid(row=12, column=0, padx=10, pady=5)
    comentario_descripcion_add = tk.Entry(ventana_agregar)
    comentario_descripcion_add.grid(row=12, column=1, padx=10, pady=5)
    #tk.Label(ventana_agregar, text="DNI del cliente:").grid(row=13, column=0, padx=10, pady=5)
    
    
    
    tk.Label(ventana_agregar, text="DNI cliente:").grid(row=13, column=0, padx=10, pady=5)
    dni_add = tk.Entry(ventana_agregar)
    dni_add.grid(row=13, column=1, padx=10, pady=5)
   
    
    tk.Button(ventana_agregar, text="Guardar", command=lambda: guardar_vehiculo(
        ventana_agregar,
        matricula_add.get(),
        numero_bastidor_add.get(),
        marca_add.get(),
        modelo_add.get(),
        version_add.get(),
        codigo_motor_add.get(),
        planta_motriz_var.get(),
        kilometros_add.get(),
        etiqueta_medioambiental_add.get(),
        fecha_itv_ok_add.get(),
        color_carroceria_add.get(),
        foto_vehiculo_add.get(),
        comentario_descripcion_add.get(),
        dni_add.get()
    )).grid(row=14, column=0, columnspan=2, pady=10)

    tk.boton_ok = tk.Button(ventana_agregar, text="Salir", command=ventana_agregar.destroy , font=("Arial", 14), bg="red", fg="white")
    tk.boton_ok.grid(row=15, column=2, columnspan=2, pady=10)

def seleccionar_imagen(ventana_padre, numero_bastidor_widget):
    filename = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    
    if filename:
        try:
            # Abrir la imagen con PIL
            imagen = Image.open(filename)
            
            # Redimensionar la imagen a 350x350
            imagen = imagen.resize((350, 350), Image.LANCZOS)
            
            # Guardar la imagen en la carpeta "imagenes" con el nombre del número de bastidor en formato JPG
            nombre_archivo = numero_bastidor_widget.get() + ".jpg"
            ruta_guardar = os.path.join("vehiculos", nombre_archivo)
            imagen.save(ruta_guardar, "JPEG")
            
            # Actualizar la ruta de la imagen en el Entry correspondiente
            foto_vehiculo_add.delete(0, tk.END)
            foto_vehiculo_add.insert(0, ruta_guardar)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen: {e}")
    
    # Asegúrate de que la ventana principal recupere el enfoque
    ventana_padre.focus_set()


def mostrar_imagen(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((350, 350), Image.LANCZOS)
        foto = ImageTk.PhotoImage(imagen)
        
        ventana_imagen = tk.Toplevel(ventana)
        ventana_imagen.title("Imagen del Vehículo")
        
        etiqueta_imagen = tk.Label(ventana_imagen, image=foto)
        etiqueta_imagen.image = foto
        etiqueta_imagen.pack(padx=20, pady=20)
    except Exception as e:
        tk.messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")

def guardar_vehiculo(ventana_agregar, matricula, numero_bastidor, marca, modelo, version, codigo_motor, planta_motriz, kilometros, etiqueta_medioambiental, fecha_itv_ok, color_carroceria, foto_vehiculo, comentario_descripcion, dni_cliente):
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO vehiculos (
            matricula, 
            numero_bastidor,
            marca,
            modelo,
            version,
            codigo_motor,
            planta_motriz,
            kilometros,
            etiqueta_medioambiental,
            fecha_itv_ok,
            color_carroceria,
            foto_vehiculo,
            comentario_descripcion,
            dni_cliente
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            matricula,
            numero_bastidor,
            marca,
            modelo,
            version,
            codigo_motor,
            planta_motriz,
            kilometros,
            etiqueta_medioambiental,
            fecha_itv_ok,
            color_carroceria,
            foto_vehiculo,
            comentario_descripcion,
            dni_cliente
        ))

       

    conexion.commit()
    
    actualizar_lista_vehiculos()
    


def editar_vehiculo():
    seleccion = tree.selection()
    if seleccion:
        id_seleccionado = tree.item(seleccion)['text']
        
        # Obtener los detalles del vehículo seleccionado
        with sqlite3.connect("Taller.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo=?", (id_seleccionado,))
            vehiculo = cursor.fetchone()
        
      
        
        if vehiculo:
            # Crear una nueva ventana para la edición
            ventana_edicion = tk.Toplevel(ventana)
            ventana_edicion.title("Editar Vehiculo")
            
            # Crear campos de entrada para editar los detalles del vehículo
            tk.Label(ventana_edicion, text="matricula:").grid(row=0, column=0, padx=10, pady=5)
            matricula_edit = tk.Entry(ventana_edicion)
            matricula_edit.insert(0, vehiculo[1])
            matricula_edit.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="numero_bastidor:").grid(row=1, column=0, padx=10, pady=5)
            numero_bastidor_edit = tk.Entry(ventana_edicion)
            numero_bastidor_edit.insert(0, vehiculo[2])
            numero_bastidor_edit.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(ventana_edicion, text="marca:").grid(row=2, column=0, padx=10, pady=5)
            marca_edit = tk.Entry(ventana_edicion)
            marca_edit.insert(0, vehiculo[3])
            marca_edit.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="modelo:").grid(row=3, column=0, padx=10, pady=5)
            modelo_edit = tk.Entry(ventana_edicion)
            modelo_edit.insert(0, vehiculo[4])
            modelo_edit.grid(row=3, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="version:").grid(row=4, column=0, padx=10, pady=5)
            version_edit = tk.Entry(ventana_edicion)
            version_edit.insert(0, vehiculo[5])
            version_edit.grid(row=4, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="codigo_motor:").grid(row=5, column=0, padx=10, pady=5)
            codigo_motor_edit = tk.Entry(ventana_edicion)
            codigo_motor_edit.insert(0, vehiculo[6])
            codigo_motor_edit.grid(row=5, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text=" planta motriz:").grid(row=6, column=0, padx=10, pady=5)
            planta_motriz_edit = tk.Entry(ventana_edicion)
            planta_motriz_edit.insert(0, vehiculo[7])
            planta_motriz_edit.grid(row=6, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="kilometros:").grid(row=7, column=0, padx=10, pady=5)
            kilometros_edit = tk.Entry(ventana_edicion)
            kilometros_edit.insert(0, vehiculo[8])
            kilometros_edit.grid(row=7, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="etiqueta_medioambiental:").grid(row=8, column=0, padx=10, pady=5)
            etiqueta_medioambiental_edit = tk.Entry(ventana_edicion)
            etiqueta_medioambiental_edit.insert(0, vehiculo[9])
            etiqueta_medioambiental_edit.grid(row=8, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="fecha_itv_ok:").grid(row=9, column=0, padx=10, pady=5)
            fecha_itv_ok_edit = tk.Entry(ventana_edicion)
            fecha_itv_ok_edit.insert(0, vehiculo[10])
            fecha_itv_ok_edit.grid(row=9, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="color_carroceria :").grid(row=10, column=0, padx=10, pady=5)
            color_carroceria_edit = tk.Entry(ventana_edicion)
            color_carroceria_edit.insert(0, vehiculo[11])
            color_carroceria_edit.grid(row=10, column=1, padx=10, pady=5)

            tk.Label(ventana_edicion, text="foto_vehiculo :").grid(row=11, column=0, padx=10, pady=5)
            foto_vehiculo_edit = tk.Entry(ventana_edicion)
            foto_vehiculo_edit.insert(0, vehiculo[12])
            foto_vehiculo_edit.grid(row=11, column=1, padx=10, pady=5)

            tk.Label(ventana_edicion, text="comentario_descripcion :").grid(row=12, column=0, padx=10, pady=5)
            comentario_descripcion_edit = tk.Entry(ventana_edicion)
            comentario_descripcion_edit.insert(0, vehiculo[13])
            comentario_descripcion_edit.grid(row=12, column=1, padx=10, pady=5)
            tk.Label(ventana_edicion, text="DNI cliente:").grid(row=13, column=0, padx=10, pady=5)
            dni_edit = tk.Entry(ventana_edicion)
            dni_edit.insert(0, vehiculo[14])
            dni_edit.grid(row=13, column=1, padx=10, pady=5)

            tk.Button(ventana_edicion, text="Guardar", command=lambda: guardar_cambios(
                id_seleccionado,
                matricula_edit.get(),
                numero_bastidor_edit.get(),
                marca_edit.get(),
                modelo_edit.get(),
                version_edit.get(),
                codigo_motor_edit.get(),
                planta_motriz_edit.get(),
                kilometros_edit.get(),
                etiqueta_medioambiental_edit.get(),
                fecha_itv_ok_edit.get(),
                color_carroceria_edit.get(),
                foto_vehiculo_edit.get(),
                comentario_descripcion_edit.get(),
                dni_edit.get()
                
                
            )).grid(row=14, column=0, columnspan=2, pady=10)
            tk.boton_ok = tk.Button(ventana_edicion, text="ok", command=ventana_edicion.destroy,font=("Arial", 14), bg="red", fg="white")
            tk.boton_ok.grid(row=15, column=0, columnspan=2, pady=10)
        else:
            tk.messagebox.showwarning("Error", "vehiculo no encontrado")

    else:
        tk.messagebox.showwarning("Error", "Selecciona un vehiculo primero")
        
def guardar_cambios(id_vehiculo, matricula, numero_bastidor, marca, modelo, version, codigo_motor, planta_motriz, kilometros, etiqueta_medioambiental, fecha_itv_ok, color_carroceria, foto_vehiculo, comentario_descripcion, dni_cliente):
    
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE vehiculos SET 
        matricula=?, numero_bastidor=?, marca=?, modelo=?, 
        version=?, codigo_motor=?, planta_motriz=?, kilometros=?, 
        etiqueta_medioambiental=?, fecha_itv_ok=?, color_carroceria=?,
        foto_vehiculo=?,comentario_descripcion=?, dni_cliente=?
        WHERE id_vehiculo=?
        """, (matricula, numero_bastidor, marca, modelo, version, codigo_motor, planta_motriz, kilometros, etiqueta_medioambiental, fecha_itv_ok, color_carroceria, foto_vehiculo, comentario_descripcion, dni_cliente, id_vehiculo))
        
    conexion.commit()
    
    actualizar_lista_vehiculos()
    

def actualizar_lista_vehiculos():
    # Limpiar el Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Cargar los vehículos actualizados
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM vehiculos")
        vehiculos = cursor.fetchall()
        
        for vehiculo in vehiculos:
            tree.insert("", tk.END, text=vehiculo[0], values=(vehiculo[1], vehiculo[2], vehiculo[3],
                                                              vehiculo[4], vehiculo[5], vehiculo[6], vehiculo[7],
                                                              vehiculo[8], vehiculo[9], vehiculo[10], vehiculo[11],
                                                              vehiculo[12],vehiculo[13],vehiculo[14]))
def mostrar_vehiculos():
    seleccionado = tree.selection()
    if seleccionado:
        item = tree.item(seleccionado)
        id_vehiculo = item['text']
        
        with sqlite3.connect("Taller.db") as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("""
            SELECT * 
            FROM vehiculos v  
            WHERE v.id_vehiculo=?
            """, (id_vehiculo,))
            
            vehiculo = cursor.fetchone()
        
        ventana_vehiculo = tk.Toplevel(ventana)
        ventana_vehiculo.title(f"Vehículo: {vehiculo[3]}")
        
        # Mostrar la imagen
        try:
            imagen = Image.open(vehiculo[12])
            imagen = imagen.resize((350, 350), Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            
            etiqueta_imagen = tk.Label(ventana_vehiculo, image=foto)
            etiqueta_imagen.image = foto
            etiqueta_imagen.pack(padx=20, pady=20)
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")
        
        # Mostrar detalles del vehículo y el DNI del cliente
        detalles = f"""
        Matrícula: {vehiculo[1]}
        Número de bastidor: {vehiculo[2]}
        Marca: {vehiculo[3]}
        Modelo: {vehiculo[4]}
        Versión: {vehiculo[5]}
        Código del motor: {vehiculo[6]}
        Planta motriz: {vehiculo[7]}
        Kilómetros: {vehiculo[8]}
        Etiqueta medioambiental: {vehiculo[9]}
        Fecha ITV OK: {vehiculo[10]}
        Color de la carrocería: {vehiculo[11]}
        Comentario/descripción: {vehiculo[13]}
        DNI/NIE del cliente: {vehiculo[14]}
        """
        
        etiqueta_detalles = tk.Label(ventana_vehiculo, text=detalles, justify=tk.LEFT, font=("Arial", 20), bg="#311B92", fg="white")
        etiqueta_detalles.pack(padx=20, pady=20)
        
        boton_ok = tk.Button(ventana_vehiculo, text="OK", command=ventana_vehiculo.destroy, font=("Arial", 14), bg="red", fg="white")
        boton_ok.pack(padx=20, pady=20)
    else:
        tk.messagebox.showwarning("Error", "Selecciona un vehiculo primero")



def buscar_vehiculo():
    palabra_clave = entrada_busqueda.get()
    
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        
        if palabra_clave:
            cursor.execute("SELECT * FROM vehiculos WHERE matricula LIKE ? OR marca LIKE ?", 
                           (f"%{palabra_clave}%", f"%{palabra_clave}%"))
        else:
            cursor.execute("SELECT * FROM vehiculos")
            
        # Limpiar el Treeview antes de añadir los nuevos resultados
        for item in tree.get_children():
            tree.delete(item)
        
        vehiculos = cursor.fetchall()
        
        for vehiculo in vehiculos:
          tree.insert("", tk.END, text=vehiculo[0], values=( vehiculo[1], vehiculo[2], vehiculo[3],
                                                          vehiculo[4], vehiculo[5], vehiculo[6], vehiculo[7],
                                                          vehiculo[8], vehiculo[9], vehiculo[10], vehiculo[11],
                                                          vehiculo[12],vehiculo[13],vehiculo[14]))

def eliminar_Vehiculo():
    seleccion = tree.selection()
    if seleccion:
        id_seleccionado = tree.item(seleccion)['text']
        
               # Confirmar la eliminación del artículo
        respuesta = tk.messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este vehiculo?")
        
        if respuesta:
            with sqlite3.connect("Taller.db") as conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo=?", (id_seleccionado,))
            
            conexion.commit()
            actualizar_lista_vehiculos()
    else:
        tk.messagebox.showwarning("Error", "Selecciona un vehiculo primero")

# Crear ventana principal
ventana= tk.Tk()
ventana.title("Vehiculos")
ventana.geometry("1100x800")
ventana.configure(bg="white")
ventana.iconbitmap("./iconos y logo/icono.ico")
logo_path = "./iconos y logo/logo.png"
logo = Image.open(logo_path)
logo = logo.resize((900, 100), Image.Resampling.LANCZOS)
logo_img = ImageTk.PhotoImage(logo)
logo_label = tk.Label(ventana, image=logo_img, bg="white", fg="#311B92", font=("Arial", 14))
logo_label.pack(pady=10)

# Campo de búsqueda
frame_busqueda = tk.Frame(ventana,bg="white")
frame_busqueda.pack(pady=20)

etiqueta_busqueda = tk.Label(frame_busqueda, text="Introduzca matricula del vehiculo:",bg="white", fg="#311B92", font=("Arial", 14))
etiqueta_busqueda.pack(side=tk.LEFT, padx=10)

entrada_busqueda = tk.Entry(frame_busqueda, width=30,bg="white", fg="#311B92", font=("Arial", 14))
entrada_busqueda.pack(side=tk.LEFT, padx=10)

boton_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar_vehiculo)
boton_buscar.pack(side=tk.LEFT, padx=10)

tree = ttk.Treeview(ventana, columns=("matricula", "numero_bastidor", "marca", "modelo", "version", 
                                      "codigo_motor", "planta_motriz", "kilometros", "etiqueta_medioambiental", 
                                      "fecha_itv_ok", "color_carroceria","foto_vehiculo", "comentario_descripcion","dni_cliente"))



tree.heading("matricula", text="Matricula")
tree.heading("numero_bastidor", text="Numero Bastidor")
tree.heading("marca", text="Marca")
tree.heading("modelo", text="Modelo")
tree.heading("version", text="Version")
tree.heading("codigo_motor", text="Codigo Motor")
tree.heading("planta_motriz", text="Planta Motriz")
tree.heading("kilometros", text="Kilometros")
tree.heading("etiqueta_medioambiental", text="Etiqueta Medioambiental")
tree.heading("fecha_itv_ok", text="Fecha ITV OK")
tree.heading("color_carroceria", text="Color Carroceria")
tree.heading("foto_vehiculo", text="foto_vehiculo")
tree.heading("comentario_descripcion", text="comentario_descripcion")
tree.heading("dni_cliente", text="DNI Cliente")
tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Configurar la barra de desplazamiento horizontal
scrollbar_horizontal = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=scrollbar_horizontal.set)

# Ubicar la barra de desplazamiento en el Treeview
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

# Cargar los vehículos en el Treeview
with sqlite3.connect("Taller.db") as conexion:
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM vehiculos")
    vehiculos = cursor.fetchall()
    
    for vehiculo in vehiculos:
        tree.insert("", tk.END, text=vehiculo[0], values=( vehiculo[1], vehiculo[2], vehiculo[3],
                                                          vehiculo[4], vehiculo[5], vehiculo[6], vehiculo[7],
                                                          vehiculo[8], vehiculo[9], vehiculo[10], vehiculo[11],
                                                          vehiculo[12],vehiculo[13],vehiculo[14]))
boton_agregar = tk.Button(ventana, text="Agregar Vehiculo", command=agregar_vehiculo, font=("Arial", 14), bg="#311B92", fg="white")
boton_agregar.pack(side=tk.LEFT, padx=20, pady=20)

boton_mostrar = tk.Button(ventana, text="Mostrar Vehiculo", command=mostrar_vehiculos,font=("Arial", 14), bg="#311B92", fg="white")
boton_mostrar.pack(side=tk.LEFT, padx=20, pady=20)

boton_editar = tk.Button(ventana, text="Editar Vehiculo", command=editar_vehiculo,font=("Arial", 14), bg="#311B92", fg="white")
boton_editar.pack(side=tk.LEFT, padx=20, pady=20)

boton_eliminar = tk.Button(ventana, text="Eliminar Vehiculo", command=eliminar_Vehiculo,font=("Arial", 14), bg="#311B92", fg="white")
boton_eliminar.pack(side=tk.LEFT, padx=20, pady=20)

boton_salir = tk.Button(ventana, text="Salir", command=open_menu_clientes,font=("Arial", 14), bg="red", fg="white")
boton_salir.pack(side=tk.LEFT, padx=20, pady=20)

ventana.mainloop()
