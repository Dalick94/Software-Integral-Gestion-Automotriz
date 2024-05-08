import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import subprocess
def setup_db():
    conn = sqlite3.connect('Taller.db')
    conn.close()

def setup_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='white')
    style.configure('TButton', font=('Arial', 14), background='#311B92', foreground='white')
    style.configure('TLabel', font=('Arial', 14), background='white', foreground='#311B92')
    style.configure('TEntry', font=('Arial', 14), background='white', foreground='black')
    style.configure('Treeview', fieldbackground='white', background='white', foreground='black')
    style.configure('Exit.TButton', font=('Arial', 14), background='red', foreground='white')

def abrir_almacen():
    root.destroy()  # Cierra la ventana actual
    subprocess.run(['python', 'Almacen.py'], creationflags=subprocess.CREATE_NO_WINDOW)
    
def load_distribuidores():
    conn = sqlite3.connect('Taller.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM distribuidores')
    rows = cursor.fetchall()
    conn.close()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert('', 'end', values=row)

def insert_distribuidor():
    conn = sqlite3.connect('Taller.db')
    cursor = conn.cursor()
    data = (nombre_entry.get(), domicilio_entry.get(), cif_entry.get(), telefono_entry.get(), email_entry.get(), web_entry.get())
    cursor.execute('INSERT INTO distribuidores (nombre, domicilio, cif, telefono, email, web) VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
    load_distribuidores()
    messagebox.showinfo('Éxito', 'Distribuidor añadido correctamente.')
    # Clear entries
    for entry in [nombre_entry, domicilio_entry, cif_entry, telefono_entry, email_entry, web_entry]:
        entry.delete(0, tk.END)

def delete_distribuidor():
    selected_item = treeview.selection()
    if selected_item:
        distribuidor_id = treeview.item(selected_item, 'values')[0]
        conn = sqlite3.connect('Taller.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM distribuidores WHERE id = ?', (distribuidor_id,))
        conn.commit()
        conn.close()
        load_distribuidores()
        messagebox.showinfo('Éxito', 'Distribuidor eliminado correctamente.')
    else:
        messagebox.showerror('Error', 'Seleccione un distribuidor para eliminar.')

def search_distribuidores(search_entry):
    conn = sqlite3.connect('Taller.db')
    cursor = conn.cursor()
    search_query = search_entry.get()
    cursor.execute('SELECT * FROM distribuidores WHERE nombre LIKE ?', ('%' + search_query + '%',))
    rows = cursor.fetchall()
    conn.close()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert('', 'end', values=row)

def open_update_window():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un distribuidor para modificar.")
        return

    update_window = tk.Toplevel(root)
    update_window.title("Actualizar Distribuidor")
    update_window.geometry("300x350")
    update_window.configure(background='white')

    conn = sqlite3.connect('Taller.db')
    cursor = conn.cursor()
    distribuidor_id = treeview.item(selected_item, 'values')[0]
    cursor.execute('SELECT * FROM distribuidores WHERE id = ?', (distribuidor_id,))
    row = cursor.fetchone()
    conn.close()

    # Labels and Entries for update
    entries_update = {}
    for i, label in enumerate(['Nombre', 'Domicilio', 'CIF', 'Telefono', 'Email', 'Web']):
        ttk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=10)
        entry = ttk.Entry(update_window, width=20)
        entry.insert(0, row[i+1])
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries_update[label.lower()] = entry

    def update_distribuidor():
        new_data = tuple(entry.get() for entry in entries_update.values()) + (distribuidor_id,)
        conn = sqlite3.connect('Taller.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE distribuidores SET nombre=?, domicilio=?, cif=?, telefono=?, email=?, web=? WHERE id=?', new_data)
        conn.commit()
        conn.close()
        load_distribuidores()
        update_window.destroy()
        messagebox.showinfo('Éxito', 'Distribuidor actualizado correctamente.')

    ttk.Button(update_window, text="Guardar Cambios", command=update_distribuidor).grid(row=6, columnspan=2, pady=10)

root = tk.Tk()
root.title('Gestión de Distribuidores')
root.state('zoomed')  # Maximizes the window on start
root.configure(bg='white')
root.iconbitmap('./iconos y logo/icono.ico')

setup_style()
setup_db()

logo_image = Image.open('./iconos y logo/logo.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = ttk.Label(root, image=logo_photo)
logo_label.image = logo_photo  # keep a reference!
logo_label.pack(pady=20)

entry_frame = ttk.Frame(root)
entry_frame.pack(pady=10, fill='x', padx=20)

# Entries for new distributor data
nombre_entry = ttk.Entry(entry_frame)
domicilio_entry = ttk.Entry(entry_frame)
cif_entry = ttk.Entry(entry_frame)
telefono_entry = ttk.Entry(entry_frame)
email_entry = ttk.Entry(entry_frame)
web_entry = ttk.Entry(entry_frame)

labels = ['Nombre', 'Domicilio', 'CIF/NIF', 'Teléfono', 'Email', 'Web']
entries = [nombre_entry, domicilio_entry, cif_entry, telefono_entry, email_entry, web_entry]
for i, label in enumerate(labels):
    ttk.Label(entry_frame, text=label).grid(row=i, column=0, padx=10, pady=5)
    entries[i].grid(row=i, column=1, padx=10, pady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

ttk.Button(button_frame, text="Agregar Distribuidor", command=insert_distribuidor).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Eliminar Distribuidor", command=delete_distribuidor).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Modificar Distribuidor", command=open_update_window).pack(side=tk.LEFT, padx=10)

search_frame = ttk.Frame(root)
search_frame.pack(pady=20, fill='x', padx=20)
search_label = ttk.Label(search_frame, text="Buscar Distribuidor:")
search_label.pack(side=tk.LEFT, padx=10)
search_entry = ttk.Entry(search_frame, width=50)
search_entry.pack(side=tk.LEFT, padx=10)
ttk.Button(search_frame, text="Buscar", command=lambda: search_distribuidores(search_entry)).pack(side=tk.LEFT, padx=10)

treeview = ttk.Treeview(root, columns=('ID', 'Nombre', 'Domicilio', 'CIF/NIF', 'Teléfono', 'Email', 'Web'), show='headings')
for col in treeview['columns']:
    treeview.heading(col, text=col)
treeview.pack(expand=True, fill='both', padx=20, pady=20)

exit_button = ttk.Button(root, text="Salir", command=abrir_almacen, style='Exit.TButton')
exit_button.pack(side='bottom', anchor='e', padx=20, pady=20)

load_distribuidores()

root.mainloop()
