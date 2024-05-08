import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, Label
from tkinter import messagebox as mb
import subprocess
import platform

# Crear la ventana principal
root = tk.Tk()
root.title('Menú Principal')
root.iconbitmap('./iconos y logo/icono.ico')
root.geometry('950x600')  # Ajustar el tamaño para dar más espacio a los botones
root.configure(bg="white")

# Configurar estilo para ttk widgets
style = ttk.Style()
style.theme_use('default')
style.configure('TButton', font=('Arial', 14), padding=10, background='#311B92', foreground='white')
style.configure('Red.TButton', font=('Arial', 14, 'bold'), padding=10, background='red', foreground='white')
style.configure('TLabelframe', background='white', bordercolor='white', relief='flat')
style.configure('TLabelframe.Label', background='white', foreground='black')

# Frame Logo Empresa
frame_logo = ttk.LabelFrame(root, text="", labelanchor='n', style='TLabelframe')
frame_logo.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
frame_logo.grid_propagate(False)

# Imagen Logo Empresa
imagen_nombre = PhotoImage(file='./iconos y logo/logo.png')
lbl_icono = Label(frame_logo, image=imagen_nombre, bg="white")
lbl_icono.pack(padx=10, pady=10)

# Frame para los botones
frame = ttk.LabelFrame(root, text="", labelanchor='n', style='TLabelframe')
frame.grid(row=1, column=0, padx=20, pady=20, sticky='ew')

# Funciones para abrir otros programas o scripts
def open_almacen():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['python', 'ALMACEN.py'], creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        else:
            subprocess.run(['python3', 'ALMACEN.py'])
            root.destroy()
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir ALMACEN.py.\n{e}')

def open_clientes():
    try:
        if platform.system() == 'Windows':
            root.destroy()
            subprocess.run(['python', 'menu clientes.py'], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(['python3', 'menu clientes.py'])
            root.destroy()
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir menu clientes.py.\n{e}')

def open_ordenes():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['python', 'ordenes.py'], creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        else:
            subprocess.run(['python3', 'ordenes.py'])
            root.destroy()
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir ordenes.py.\n{e}')

def open_facturas_pdf():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['python', 'FacturaPDF.py'], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.call(['python3', 'FacturaPDF.py'], shell=True)
    except Exception as e:
        mb.showerror('Error', f'No se pudo abrir FacturaPDF.py.\n{e}')

# Botones con los estilos configurados
icono_clientes = PhotoImage(file='./iconos y logo/icono_clientes.png')
btn_clientes = ttk.Button(frame, text='Clientes', image=icono_clientes, compound='top', command=open_clientes, style='TButton')
btn_clientes.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

icono_almacen = PhotoImage(file='./iconos y logo/icono_almacen.png')
btn_almacen = ttk.Button(frame, text='Almacen', image=icono_almacen, compound='top', command=open_almacen, style='TButton')
btn_almacen.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

icono_trabajo = PhotoImage(file='./iconos y logo/icono_trabajo.png')
btn_orden_trabajo = ttk.Button(frame, text='Trabajos', image=icono_trabajo, compound='top', command=open_ordenes, style='TButton')
btn_orden_trabajo.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

icono_factura = PhotoImage(file='./iconos y logo/icono_factura.png')
btn_factura = ttk.Button(frame, text='Facturación', image=icono_factura, compound='top', command=open_facturas_pdf, style='TButton')
btn_factura.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')

# Ajustar el grid para que todos los botones tengan el mismo tamaño
frame.grid_columnconfigure(0, weight=1, uniform="button")
frame.grid_columnconfigure(1, weight=1, uniform="button")
frame.grid_columnconfigure(2, weight=1, uniform="button")
frame.grid_columnconfigure(3, weight=1, uniform="button")

# Botón para salir de la aplicación con el estilo 'Red.TButton'
btn_exit = ttk.Button(root, text='Salir', style='Red.TButton', command=root.destroy)
btn_exit.grid(row=2, column=0, padx=20, pady=20, sticky='ew')

root.mainloop()
