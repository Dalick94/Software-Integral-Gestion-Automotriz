import tkinter as tk
from tkinter import messagebox as mb
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess
import sqlite3

def abrir_Menu_Principal():
    root.destroy()  # Cierra la ventana actual
    subprocess.run(['python', 'Menuprincipal.py'], creationflags=subprocess.CREATE_NO_WINDOW)
   
    
# Funciones para abrir otros programas o scripts
def open_distribuidores():
    subprocess.Popen(['python', 'distribuidores.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    root.destroy()
def open_articulos():
    conexion = sqlite3.connect("Taller.db")
    cursor = conexion.cursor()
    distribuidores = cursor.execute('''SELECT * FROM distribuidores''').fetchall()
    conexion.close()
    
    if not distribuidores:
        mb.showerror('Error', 'No existen distribuidores en la BBDD, crea uno primero')
        root.destroy() 
    else:
        root.destroy()
        subprocess.Popen(['python', 'articulos.py'], creationflags=subprocess.CREATE_NO_WINDOW)
        
def open_mostrar_articulos():
    root.destroy()
    subprocess.Popen(['python', 'mostrar_articulos.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    
# Crear la ventana principal
root = tk.Tk()
root.title('GESTION ALMACEN')
root.iconbitmap("./iconos y logo/icono.ico")

# Configurar el fondo de la ventana
root.configure(bg="white")

logo_path = "./iconos y logo/logo.jpg"
logo = Image.open(logo_path)
logo = logo.resize((500, 100), Image.Resampling.LANCZOS)
logo_img = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image=logo_img, bg="white")
logo_label.pack(pady=10)

# Estilo de los botones
button_style = {'font': ('Arial', 14), 'fg': 'white', 'width': 20}

# Botón para abrir distribuidores.py
btn_distribuidores = tk.Button(root, text="Distribuidores", command=open_distribuidores, bg="#311B92", **button_style)
btn_distribuidores.pack(pady=10)

# Botón para abrir articulos.py
btn_articulos = tk.Button(root, text="Introducir artículo", command=open_articulos, bg="#311B92", **button_style)
btn_articulos.pack(pady=10)

# Botón para mostrar artículos
btn_mostrar = tk.Button(root, text="Mostrar Artículos", command=open_mostrar_articulos, bg="#311B92", **button_style)
btn_mostrar.pack(pady=10)

# Botón para salir de la aplicación
btn_exit = tk.Button(root, text="Salir", command=abrir_Menu_Principal, bg="red", font=("Arial", 14), width=20, fg='white')
btn_exit.pack(side=tk.BOTTOM, anchor=tk.SE, pady=10)

root.geometry('600x600')
root.eval('tk::PlaceWindow . center')

root.mainloop()
