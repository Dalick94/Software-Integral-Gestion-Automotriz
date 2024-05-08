import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess
import platform
def open_gestion_clientes():
    subprocess.Popen(['python', 'Clientes.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    root.destroy()
def open_gestion_vehiculos():
    subprocess.Popen(['python', 'vehiculos.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    root.destroy()
def open_almacen():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['python', 'Menuprincipal.py'], creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        else:
            subprocess.run(['Python3', 'Menuprincipal.py'])
            root.destroy()
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir ALMACEN.py.\n{e}')

                     
def setup_main_window(root):
    root.title('Menú Clientes Y Vehiculos')
    root.geometry('800x600')# Ajuste para tamaño estándar de ventana
    root.iconbitmap('./iconos y logo/icono.ico')
    root.configure(bg='white')
    root.state('zoomed')  # Abre la ventana maximizada

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Arial', 30), padding=10, background='#311B92', foreground='white')
    style.configure('Red.TButton', font=('Arial', 30, 'bold'), padding=10, background='red', foreground='white')

    # Cargar y configurar la imagen del logotipo
    logo_image = Image.open('./iconos y logo/logo.png')
    resized_image = logo_image.resize((900, 168), Image.Resampling.LANCZOS)  # Ajusta estos valores según sea necesario
    logo_photo = ImageTk.PhotoImage(resized_image)
    logo_label = tk.Label(root, image=logo_photo, bg='white')
    logo_label.image = logo_photo  # Guardar una referencia!
    logo_label.pack(pady=20)

    # Botones para abrir las gestiones
    ttk.Button(root, text="Gestión de Clientes", command=open_gestion_clientes).pack(pady=20)
    ttk.Button(root, text="Gestión de Vehículos", command=open_gestion_vehiculos).pack(pady=20)

    # Botón de salida
    exit_button = ttk.Button(root, text="Salir", style='Red.TButton', command=open_almacen)
    exit_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


root = tk.Tk()
setup_main_window(root)
root.mainloop()
