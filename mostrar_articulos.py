import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import messagebox
import datetime
import subprocess
def abrir_almacen():
    ventana.destroy()  # Cierra la ventana actual
    subprocess.run(['python', 'Almacen.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    
def calcular_ir():
    seleccion = tree.selection()
    if seleccion:
        id_seleccionado = tree.item(seleccion)['text']
        
        # Calcular el número de piezas vendidas en la última semana
        fecha_semana_pasada = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        piezas_semana = contar_piezas_vendidas(id_seleccionado, fecha_semana_pasada)
        
        # Calcular el número de piezas vendidas en el último mes
        fecha_mes_pasado = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        piezas_mes = contar_piezas_vendidas(id_seleccionado, fecha_mes_pasado)
        
        # Calcular el número de piezas vendidas en el último año
        fecha_ano_pasado = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        piezas_ano = contar_piezas_vendidas(id_seleccionado, fecha_ano_pasado)
        
        # Calcular el Índice de Rotación (IR)
        ir_semana = piezas_semana / 1
        ir_mes = piezas_mes / 4
        ir_ano = piezas_ano / 52
        
        # Mostrar el IR en una ventana emergente
        mensaje = f"IR última semana: {ir_semana:.2f}\nIR último mes: {ir_mes:.2f}\nIR último año: {ir_ano:.2f}"
        tk.messagebox.showinfo("Índice de Rotación (IR)", mensaje)
    else:
        tk.messagebox.showwarning("Error", "Selecciona un artículo primero")

def contar_piezas_vendidas(id_articulo, fecha):
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT unidades
        FROM articulos
        WHERE id=? AND fecha_alta <= ?
        """, (id_articulo, fecha))
        
        result = cursor.fetchone()
        
        if result:
            unidades = result[0]
            return unidades
        else:
            return 0



def editar_articulo():
    seleccion = tree.selection()
    if seleccion:
        id_seleccionado = tree.item(seleccion)['text']
        
        # Obtener los detalles del artículo seleccionado
        with sqlite3.connect("Taller.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM articulos WHERE id=?", (id_seleccionado,))
            articulo = cursor.fetchone()
        
        if articulo:
            # Crear una nueva ventana para la edición
            ventana_edicion = tk.Toplevel(ventana)
            ventana_edicion.title("Editar Artículo")
            
            # Crear campos de entrada para editar los detalles del artículo
            tk.Label(ventana_edicion, text="Referencia Fabricante:").grid(row=0, column=0, padx=10, pady=5)
            referencia_fabricante_edit = tk.Entry(ventana_edicion)
            referencia_fabricante_edit.insert(0, articulo[1])
            referencia_fabricante_edit.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Referencia Interna:").grid(row=1, column=0, padx=10, pady=5)
            referencia_interna_edit = tk.Entry(ventana_edicion)
            referencia_interna_edit.insert(0, articulo[2])
            referencia_interna_edit.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Descripción:").grid(row=2, column=0, padx=10, pady=5)
            descripcion_edit = tk.Entry(ventana_edicion)
            descripcion_edit.insert(0, articulo[3])
            descripcion_edit.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Unidades:").grid(row=3, column=0, padx=10, pady=5)
            unidades_edit = tk.Entry(ventana_edicion)
            unidades_edit.insert(0, articulo[4])
            unidades_edit.grid(row=3, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Precio Compra:").grid(row=4, column=0, padx=10, pady=5)
            precio_compra_edit = tk.Entry(ventana_edicion)
            precio_compra_edit.insert(0, articulo[5])
            precio_compra_edit.grid(row=4, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Precio Venta:").grid(row=5, column=0, padx=10, pady=5)
            precio_venta_edit = tk.Entry(ventana_edicion)
            precio_venta_edit.insert(0, articulo[6])
            precio_venta_edit.grid(row=5, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Fecha Alta:").grid(row=6, column=0, padx=10, pady=5)
            fecha_alta_edit = tk.Entry(ventana_edicion)
            fecha_alta_edit.insert(0, articulo[7])
            fecha_alta_edit.grid(row=6, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Nombre Distribuidor:").grid(row=7, column=0, padx=10, pady=5)
            nombre_distribuidor_edit = tk.Entry(ventana_edicion)
            nombre_distribuidor_edit.insert(0, articulo[8])
            nombre_distribuidor_edit.grid(row=7, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Albaran:").grid(row=8, column=0, padx=10, pady=5)
            albaran_edit = tk.Entry(ventana_edicion)
            albaran_edit.insert(0, articulo[9])
            albaran_edit.grid(row=8, column=1, padx=10, pady=5)
            
            tk.Label(ventana_edicion, text="Imagen:").grid(row=9, column=0, padx=10, pady=5)
            imagen_edit = tk.Entry(ventana_edicion)
            imagen_edit.insert(0, articulo[10])
            imagen_edit.grid(row=9, column=1, padx=10, pady=5)
            
            tk.Button(ventana_edicion, text="Guardar", command=lambda: guardar_cambios(
                id_seleccionado,
                referencia_fabricante_edit.get(),
                referencia_interna_edit.get(),
                descripcion_edit.get(),
                unidades_edit.get(),
                precio_compra_edit.get(),
                precio_venta_edit.get(),
                fecha_alta_edit.get(),
                nombre_distribuidor_edit.get(),
                albaran_edit.get(),
                imagen_edit.get()
            )).grid(row=10, column=0, columnspan=2, pady=10)
            tk.boton_ok = tk.Button(ventana_edicion, text="ok", command=ventana_edicion.destroy,font=("Arial", 14), bg="red", fg="white")
            tk.boton_ok.grid(row=11, column=0, columnspan=2, pady=10)
        else:
            tk.messagebox.showwarning("Error", "Artículo no encontrado")

    else:
        tk.messagebox.showwarning("Error", "Selecciona un artículo primero")
        
def guardar_cambios(id_articulo, referencia_fabricante, referencia_interna, descripcion, 
                    unidades, precio_compra, precio_venta, fecha_alta, 
                    nombre_distribuidor, albaran, imagen):
    # Actualizar el artículo en la base de datos
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE articulos SET 
        referencia_fabricante=?, referencia_interna=?, descripcion=?, unidades=?, 
        precio_compra=?, precio_venta=?, fecha_alta=?, nombre_distribuidor=?, 
        albaran=?, imagen=?
        WHERE id=?
        """, (referencia_fabricante, referencia_interna, descripcion, unidades, 
              precio_compra, precio_venta, fecha_alta, nombre_distribuidor, 
              albaran, imagen, id_articulo))
        
    conexion.commit()
    
    actualizar_lista_articulos()

def actualizar_lista_articulos():
    # Limpiar el Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Cargar los artículos actualizados
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, referencia_fabricante, descripcion, unidades FROM articulos")
        articulos = cursor.fetchall()
        
        for articulo in articulos:
            tree.insert("", tk.END, text=articulo[0], values=(articulo[1], articulo[2], articulo[3]))
       

def visualizar_media_unidades():
    with sqlite3.connect("Taller.db") as conexion:
        query = """
        SELECT strftime('%Y-%m', fecha_alta) AS mes, AVG(unidades) AS media_unidades
        FROM articulos
        WHERE fecha_alta >= date('now', '-1 year')
        GROUP BY strftime('%Y-%m', fecha_alta)
        """
        df = pd.read_sql_query(query, conexion)
        
    if df.empty:
        tk.messagebox.showwarning("Error", "No hay datos disponibles para visualizar.")
        return
    
    df['mes'] = pd.to_datetime(df['mes'])
    df = df.set_index('mes')
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['media_unidades'], marker='o', linestyle='-')
    plt.title('Número medio de unidades en almacén (Último año)')
    plt.xlabel('Mes')
    plt.ylabel('Media de unidades')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
def mostrar_articulo():
    seleccionado = tree.selection()
    if seleccionado:
        item = tree.item(seleccionado)
        id_articulo = item['text']
        
        with sqlite3.connect("Taller.db") as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("SELECT * FROM articulos WHERE id=?", (id_articulo,))
            articulo = cursor.fetchone()
        
        ventana_articulo = tk.Toplevel(ventana)
        ventana_articulo.title(f"Artículo: {articulo[2]}")
        
        # Mostrar la imagen
        try:
            imagen = Image.open(articulo[-1])
            imagen = imagen.resize((350, 350), Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            
            etiqueta_imagen = tk.Label(ventana_articulo, image=foto)
            etiqueta_imagen.image = foto
            etiqueta_imagen.pack(padx=20, pady=20)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
        
        # Mostrar detalles del artículo
        detalles = f"""
        Referencia fabricante: {articulo[1]}
        Referencia interna : {articulo[2]}
        Descripción: {articulo[3]}
        Unidades: {articulo[4]}
        Precio de compra: {articulo[5]}
        Precio de venta: {articulo[6]}
        Fecha: {articulo[7]}
        Distribuidor: {articulo[8]}
        Albaran: {articulo[9]}
        """
        
        etiqueta_detalles = tk.Label(ventana_articulo, text=detalles, justify=tk.LEFT,font=("Arial", 20), bg="#311B92", fg="white")
        etiqueta_detalles.pack(padx=20, pady=20)
        boton_ok = tk.Button(ventana_articulo, text="ok", command=ventana_articulo.destroy,font=("Arial", 14), bg="red", fg="white")
        boton_ok.pack( padx=20, pady=20)

def buscar_articulos():
    palabra_clave = entrada_busqueda.get()
    
    with sqlite3.connect("Taller.db") as conexion:
        cursor = conexion.cursor()
        
        if palabra_clave:
            cursor.execute("SELECT id, referencia_fabricante, descripcion,unidades FROM articulos WHERE referencia_fabricante LIKE ? OR descripcion LIKE ?", 
                           (f"%{palabra_clave}%", f"%{palabra_clave}%"))
        else:
            cursor.execute("SELECT id, referencia_fabricante, descripcion,unidades FROM articulos")
            
        # Limpiar el Treeview antes de añadir los nuevos resultados
        for item in tree.get_children():
            tree.delete(item)
        
        articulos = cursor.fetchall()
        
        for articulo in articulos:
            tree.insert("", tk.END, text=articulo[0], values=(articulo[1], articulo[2],articulo[3]))
def eliminar_articulo():
    seleccion = tree.selection()
    if seleccion:
        id_seleccionado = tree.item(seleccion)['text']
        
        # Comprobar si hay unidades en el almacén
        with sqlite3.connect("Taller.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT unidades FROM articulos WHERE id=?", (id_seleccionado,))
            unidades = cursor.fetchone()[0]
        
        if unidades > 0:
            tk.messagebox.showwarning("Error", "No se puede eliminar el artículo porque hay unidades en el almacén.")
            return
        
     
            
            if cursor.fetchone():
                tk.messagebox.showwarning("Error", "No se puede eliminar el artículo porque tiene una ORDEN DE TRABAJO con fecha de uso superior a 30 días desde su entrada en almacén.")
                return
        
        # Confirmar la eliminación del artículo
        respuesta = tk.messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este artículo?")
        
        if respuesta:
            with sqlite3.connect("Taller.db") as conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM articulos WHERE id=?", (id_seleccionado,))
            
            conexion.commit()
            actualizar_lista_articulos()
    else:
        tk.messagebox.showwarning("Error", "Selecciona un artículo primero")

# Crear ventana principal
ventana= tk.Tk()
ventana.title("Seleccionar Artículo")
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

etiqueta_busqueda = tk.Label(frame_busqueda, text="Introduzca ref fabricante o la descripción:",bg="white", fg="#311B92", font=("Arial", 14))
etiqueta_busqueda.pack(side=tk.LEFT, padx=10)

entrada_busqueda = tk.Entry(frame_busqueda, width=30,bg="white", fg="#311B92", font=("Arial", 14))
entrada_busqueda.pack(side=tk.LEFT, padx=10)

boton_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar_articulos)
boton_buscar.pack(side=tk.LEFT, padx=10)

# Crear Treeview para mostrar la lista de artículos
tree = ttk.Treeview(ventana, columns=("Referencia Fabricante", "Descripción", "Unidades"))
tree.heading("#0", text="ID")
tree.heading("Referencia Fabricante", text="Referencia Fabricante")
tree.heading("Descripción", text="Descripción")
tree.heading("Unidades", text="Unidades")
tree.pack(padx=20, pady=20)

# Cargar los artículos al iniciar la aplicación
with sqlite3.connect("Taller.db") as conexion:
    cursor = conexion.cursor()
    
    cursor.execute("SELECT id, referencia_fabricante, descripcion, unidades FROM articulos")
    articulos = cursor.fetchall()
    
    for articulo in articulos:
        tree.insert("", tk.END, text=articulo[0], values=(articulo[1], articulo[2], articulo[3]))


boton_mostrar = tk.Button(ventana, text="Mostrar Artículo", command=mostrar_articulo,font=("Arial", 14), bg="#311B92", fg="white")
boton_mostrar.pack(side=tk.LEFT, padx=20, pady=20)

boton_visualizar = tk.Button(ventana, text="Visualizar Media Unidades", command=visualizar_media_unidades,font=("Arial", 14), bg="#311B92", fg="white")
boton_visualizar.pack(side=tk.LEFT, padx=20, pady=20)

boton_editar = tk.Button(ventana, text="Editar Artículo", command=editar_articulo,font=("Arial", 14), bg="#311B92", fg="white")
boton_editar.pack(side=tk.LEFT, padx=20, pady=20)

boton_eliminar = tk.Button(ventana, text="Eliminar Artículo", command=eliminar_articulo,font=("Arial", 14), bg="#311B92", fg="white")
boton_eliminar.pack(side=tk.LEFT, padx=20, pady=20)

boton_ir = tk.Button(ventana, text="Calcular IR", command=calcular_ir,font=("Arial", 14), bg="#311B92", fg="white")
boton_ir.pack(side=tk.LEFT, padx=20, pady=20)

boton_salir = tk.Button(ventana, text="Salir", command=abrir_almacen,font=("Arial", 14), bg="red", fg="white")
boton_salir.pack(side=tk.LEFT, padx=20, pady=20)


ventana.mainloop()
