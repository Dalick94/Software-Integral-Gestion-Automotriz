import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import sqlite3
import json
import subprocess
import sys



client_dropdown  = None
vehicle_dropdown = None
repair_status_dropdown = None
work_text = None
workers_listbox = None
articulos_listbox = None
root = None

def connect_to_db():
    # Asegúrate de que la ruta al archivo de la base de datos es correcta.
    conn = sqlite3.connect('Taller.db')  # Ruta actualizada al archivo subido
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrdenesTrabajo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni_cliente TEXT,
            matricula TEXT,
            descripcion_trabajo TEXT,
            estado_reparacion TEXT,
            detalles TEXT
        )
    ''')
    
    # Crear tabla para trabajadores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trabajadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER,
            nombre TEXT,
            tipo_trabajo TEXT,
            horas_trabajadas INTEGER,
            FOREIGN KEY (orden_id) REFERENCES OrdenesTrabajo(id)
        )
    ''')
    
    # Crear tabla para piezas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Piezas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER,
            descripcion TEXT,
            cantidad INTEGER,
            FOREIGN KEY (orden_id) REFERENCES OrdenesTrabajo(id)
        )
    ''')
    
    conn.commit()
    return conn
def buscar_orden_por_vehiculo():
    vehiculo = vehicle_dropdown.get()
    if not vehiculo:
        messagebox.showwarning("Error", "Por favor, selecciona un vehículo para buscar.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT dni_cliente, descripcion_trabajo, estado_reparacion, detalles FROM OrdenesTrabajo WHERE matricula = ?", (vehiculo,))
    orden = cursor.fetchone()
    conn.close()

    if orden:
        # Rellenar campos de la GUI con los datos recuperados
        dni_cliente, descripcion_trabajo, estado_reparacion, detalles = orden
        client_dropdown.set(dni_cliente)
        work_text.delete('1.0', tk.END)
        work_text.insert(tk.END, descripcion_trabajo)
        repair_status_dropdown.set(estado_reparacion)

        # Rellenar la lista de trabajadores
        workers_listbox.delete(0, tk.END)
        articulos_listbox.delete(0, tk.END)

        if detalles:
            workers_and_parts = json.loads(detalles)
            workers = workers_and_parts.get('trabajadores', [])
            for worker in workers:
                add_worker(workers_listbox, worker['nombre'], worker['tipo_trabajo'], worker['horas_trabajadas'])

            articulos = workers_and_parts.get('piezas', [])
            for articulo in articulos:
                articulos_listbox.insert(tk.END, f"{articulo['descripcion']} - Cantidad: {articulo['cantidad']}")
    else:
        messagebox.showinfo("No encontrado", "No se encontró ninguna orden de trabajo para el vehículo seleccionado.")


def actualizar_datos():
    # Obtener los datos modificados de la interfaz gráfica
    vehiculo = vehicle_dropdown.get()
    dni_cliente = client_dropdown.get()
    descripcion_trabajo = work_text.get("1.0", tk.END).strip()
    estado_reparacion = repair_status_dropdown.get()

    # Recopilar datos de trabajadores desde el Listbox
    trabajadores = []
    for item in workers_listbox.get(0, tk.END):
        name, type, hours = item.split(" - ")
        trabajadores.append({'nombre': name, 'tipo_trabajo': type, 'horas_trabajadas': int(hours.replace(" horas", ""))})
        
    # Recopilar datos de piezas desde el Listbox de artículos
    piezas = []
    for item in articulos_listbox.get(0, tk.END):
        if " - Cantidad: " in item:
            descripcion, cantidad = item.split(" - Cantidad: ")
            piezas.append({'descripcion': descripcion, 'cantidad': int(cantidad)})
        else:
            piezas.append({'descripcion': item, 'cantidad': 1})  # Si el formato no es el esperado, asumimos una cantidad de 1

    detalles = json.dumps({'trabajadores': trabajadores, 'piezas': piezas})

    # Actualizar los datos en la base de datos
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE OrdenesTrabajo SET dni_cliente=?, descripcion_trabajo=?, estado_reparacion=?, detalles=? WHERE matricula=?", (dni_cliente, descripcion_trabajo, estado_reparacion, detalles, vehiculo))
    conn.commit()
    conn.close()

    # Mostrar un mensaje de confirmación
    messagebox.showinfo("Actualizar", "Datos actualizados correctamente.")

def get_unique_dnis():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT dni_cliente FROM vehiculos ORDER BY dni_cliente")
    dnis = cursor.fetchall()
    conn.close()
    return [dni[0] for dni in dnis]

def get_vehicles_by_client_dni(dni):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT matricula FROM vehiculos WHERE dni_cliente = ?", (dni,))
    vehicles = cursor.fetchall()
    conn.close()
    return [vehicle[0] for vehicle in vehicles]

def get_vehicle_details(vehicle):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT dni_cliente FROM vehiculos WHERE matricula = ?", (vehicle,))
    dni = cursor.fetchone()
    conn.close()

    if dni is not None:
        return dni[0], vehicle
    else:
        return None, None

def get_articulos():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion, unidades FROM articulos WHERE unidades > 0")
    articulos = cursor.fetchall()
    conn.close()
    return articulos

def restar_stock_articulo(descripcion, cantidad, articulo_dropdown, articulos_listbox):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE articulos SET unidades = unidades - ? WHERE descripcion = ?", (cantidad, descripcion))
    conn.commit()
    conn.close()
    articulos = get_articulos()
    articulo_dropdown['values'] = [f"{articulo[1]} ({articulo[2]} disponibles)" for articulo in articulos]
    if articulos:
        articulo_dropdown.set(articulo_dropdown['values'][0])
    else:
        articulo_dropdown.set("")
    articulos_listbox.insert(tk.END, f"{descripcion} - Cantidad restada: {cantidad}")

def update_vehicles(event):
    global vehicle_dropdown
    selected_dni = client_dropdown.get()
    vehicles = get_vehicles_by_client_dni(selected_dni)
    vehicle_dropdown['values'] = vehicles
    vehicle_dropdown.set('')

def add_worker(listbox, name, type, hours):
    entry = f"{name} - {type} - {hours} horas"
    listbox.insert(tk.END, entry)

def save_data():
    conn = connect_to_db()
    cursor = conn.cursor()
    global descripcion_trabajo
    # Recopilación de datos de la interfaz
    vehicle = vehicle_dropdown.get()
    dni_cliente, matricula = get_vehicle_details(vehicle)
    descripcion_trabajo = work_text.get("1.0", tk.END).strip()
    estado_reparacion = repair_status_dropdown.get()

    # Recopilar datos de trabajadores desde el Listbox
    trabajadores = []
    for item in workers_listbox.get(0, tk.END):
        name, type, hours = item.split(" - ")
        trabajadores.append({'nombre': name, 'tipo_trabajo': type, 'horas_trabajadas': int(hours.replace(" horas", ""))})
        
    # Recopilar datos de piezas desde el Listbox de artículos
    piezas = []
    for item in articulos_listbox.get(0, tk.END):
        descripcion, cantidad = item.split(" - Cantidad restada: ")
        piezas.append({'descripcion': descripcion, 'cantidad': int(cantidad)})

    detalles = json.dumps({'trabajadores': trabajadores, 'piezas': piezas})

    # Datos a guardar
    datos = (dni_cliente, matricula, descripcion_trabajo, estado_reparacion, detalles)

    # Insertar en la tabla de OrdenesTrabajo
    cursor.execute('''
        INSERT INTO OrdenesTrabajo (dni_cliente, matricula, descripcion_trabajo, estado_reparacion, detalles)
        VALUES (?, ?, ?, ?, ?)
    ''', datos)
    orden_id = cursor.lastrowid  # Obtener el ID de la última fila insertada

    # Insertar trabajadores en la tabla Trabajadores
    for trabajador in trabajadores:
        cursor.execute('''
            INSERT INTO Trabajadores (orden_id, nombre, tipo_trabajo, horas_trabajadas)
            VALUES (?, ?, ?, ?)
        ''', (orden_id, trabajador['nombre'], trabajador['tipo_trabajo'], trabajador['horas_trabajadas']))
    
    # Insertar piezas en la tabla Piezas
    for pieza in piezas:
        cursor.execute('''
            INSERT INTO Piezas (orden_id, descripcion, cantidad)
            VALUES (?, ?, ?)
        ''', (orden_id, pieza['descripcion'], pieza['cantidad']))
    
    conn.commit()
    conn.close()

    # Mensaje de confirmación
    messagebox.showinfo("Guardar", "Datos guardados correctamente.")

    # Limpieza de campos
    vehicle_dropdown.set('')
    work_text.delete('1.0', tk.END)
    repair_status_dropdown.set('')
    workers_listbox.delete(0, tk.END)
    articulos_listbox.delete(0, tk.END)


def setup_main_window():
    global root
    global client_dropdown  ,vehicle_dropdown ,work_text,repair_status_dropdown,workers_listbox,articulos_listbox
    root = tk.Tk()
    root.title("Gestión de Órdenes de Trabajo")
    root.configure(bg="white")
    root.state('zoomed')
    
    try:
        logo_image = ImageTk.PhotoImage(Image.open('./iconos y logo/logo.png'))
        logo_label = tk.Label(root, image=logo_image, bg="white")
        logo_label.image = logo_image
        logo_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='nsew')
    except Exception as e:
        messagebox.showerror("Error al cargar la imagen", str(e))

    # Configuración de la columna
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    # Configuración y creación del Combobox para seleccionar cliente
    ttk.Label(root, text="Seleccione Cliente:", background='white', foreground='#311B92').grid(row=1, column=0, padx=20, pady=5, sticky='nw')
    client_dropdown = ttk.Combobox(root, width=50)
    client_dropdown.grid(row=2, column=0, padx=20, pady=5, sticky='nw')
    client_dropdown['values'] = get_unique_dnis()  # Cargar DNIs después de inicializar el Combobox
    client_dropdown.bind("<<ComboboxSelected>>", update_vehicles)

    ttk.Label(root, text="Seleccione Vehículo:", background='white', foreground='#311B92').grid(row=3, column=0, padx=20, pady=5, sticky='nw')
    vehicle_dropdown = ttk.Combobox(root, width=50)
    vehicle_dropdown.grid(row=4, column=0, padx=20, pady=5, sticky='nw')
    tk.Button(root, text="Buscar por Vehículo", bg='#311B92', fg='white', command=buscar_orden_por_vehiculo, width=15, height=1).grid(row=4, column=0, padx=5, pady=5, sticky='e')

    
    ttk.Label(root, text="Trabajos a realizar:", background='white', foreground='#311B92').grid(row=5, column=0, padx=20, pady=5, sticky='nw')
    work_text = scrolledtext.ScrolledText(root, width=40, height=10)
    work_text.grid(row=6, column=0, rowspan=10, padx=20, pady=5, sticky='nsew')

    # Estado de la reparación
    ttk.Label(root, text="Estado de la Reparación:", background='white', foreground='#311B92').grid(row=16, column=0, padx=20, pady=5, sticky='nw')
    repair_status_dropdown = ttk.Combobox(root, width=50, values=["ENTRADA", "EN PROCESO", "PENDIENTE DE PERITACIÓN", "FINALIZADO"])
    repair_status_dropdown.grid(row=17, column=0, padx=20, pady=5, sticky='nw')

    # Section for adding workers
    ttk.Label(root, text="Nombre del Trabajador:", background='white', foreground='#311B92').grid(row=1, column=1, padx=20, pady=5, sticky='nw')
    worker_name = ttk.Entry(root, width=50)
    worker_name.grid(row=2, column=1, padx=20, pady=5, sticky='nw')

    ttk.Label(root, text="Tipo de Trabajo:", background='white', foreground='#311B92').grid(row=3, column=1, padx=20, pady=5, sticky='nw')
    work_type = ttk.Combobox(root, width=47, values=["Mecánico", "Chapista", "Pintor"])
    work_type.grid(row=4, column=1, padx=20, pady=5, sticky='nw')

    ttk.Label(root, text="Horas Trabajadas:", background='white', foreground='#311B92').grid(row=5, column=1, padx=20, pady=5, sticky='nw')
    hours_worked = ttk.Entry(root, width=50)
    hours_worked.grid(row=6, column=1, padx=20, pady=5, sticky='nw')

    tk.Button(root, text="Agregar Trabajador", bg='#311B92', fg='white', command=lambda: add_worker(workers_listbox, worker_name.get(), work_type.get(), hours_worked.get())).grid(row=7, column=1,  padx=20, pady=5, sticky='w')
    workers_listbox = tk.Listbox(root, width=80, height=10)
    workers_listbox.grid(row=8, column=1, columnspan=2, padx=20, pady=10, sticky='nw')

    # Section for articles
    ttk.Label(root, text="Seleccione Artículo:", background='white', foreground='#311B92').grid(row=10, column=1, padx=20, pady=5, sticky='nw')
    articulo_var = tk.StringVar()
    articulo_dropdown = ttk.Combobox(root, textvariable=articulo_var, width=50)
    articulo_dropdown['values'] = [f"{articulo[1]} ({articulo[2]} disponibles)" for articulo in get_articulos()]
    articulo_dropdown.grid(row=11, column=1, padx=20, pady=5, sticky='nw')

    articulos_listbox = tk.Listbox(root, width=60, height=10)
    articulos_listbox.grid(row=12, column=1, columnspan=2, padx=20, pady=10, sticky='nw')

    tk.Button(root, text="Restar Stock Artículo", bg='#311B92', fg='white', command=lambda: restar_stock_articulo(articulo_dropdown.get().split(' (')[0], 1, articulo_dropdown, articulos_listbox),width=15).grid(row=11, column=1, padx=1, pady=5)
    
    # Botones de acción
    tk.Button(root, text="Guardar", bg='#311B92', fg='white', command=save_data, width=15).grid(row=18, column=0, padx=20, pady=5)
    tk.Button(root, text="Modificar", bg='#311B92', fg='white', command=actualizar_datos, width=15).grid(row=18, column=1, padx=20, pady=5)
    tk.Button(root, text="Salir", bg='red', fg='white', command=exit_to_main_menu).grid(row=18, column=2, padx=20, pady=5, sticky='ew')
    root.mainloop()

def exit_to_main_menu():
    global root
    if root is not None:
        root.destroy()
        root = None
    # Ejecutar Menuprincipal.py sin abrir una ventana de comandos
    subprocess.Popen([sys.executable, 'Menuprincipal.py'], creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == '__main__':
    setup_main_window()
