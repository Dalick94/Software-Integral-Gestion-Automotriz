import sqlite3
# Establecer la conexión con la base de datos y crear las tablas si no existen
conexion = sqlite3.connect('Taller.db')
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS distribuidores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        domicilio TEXT,
        cif TEXT,
        telefono TEXT,
        email TEXT,
        web TEXT
    )
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS articulos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referencia_fabricante TEXT,
                    referencia_interna TEXT,
                    descripcion TEXT,
                    unidades INTEGER,
                    precio_compra REAL,
                    precio_venta REAL,
                    fecha_alta DATE,
                    nombre_distribuidor TEXT,
                    albaran TEXT,
                    imagen TEXT
                );''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehiculos (
        id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT,
        numero_bastidor TEXT ,
        marca TEXT,
        modelo TEXT,
        version TEXT,
        codigo_motor TEXT,
        planta_motriz TEXT CHECK(planta_motriz IN ('Gasolina', 'Diésel', 'FULL HYBRID', 'HEV', 'MHEV', 'Eléctrico 100%')),
        kilometros INTEGER DEFAULT 0,
        etiqueta_medioambiental TEXT,
        fecha_itv_ok DATE,
        color_carroceria TEXT,
        foto_vehiculo TEXT,
        comentario_descripcion TEXT,
        dni_cliente TEXT,
        FOREIGN KEY(dni_cliente) REFERENCES clientes(DNI_NIE)
    )
''')


conexion.commit()
conexion.close()
for db_name in ['Clientes.db', 'Taller.db']:
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre TEXT,
                    Apellido1 TEXT,
                    Apellido2 TEXT,
                    Telefono1 INTEGER,
                    Telefono2 INTEGER,
                    Correo TEXT,
                    DNI_NIE TEXT UNIQUE,
                    Direccion TEXT,
                    Codigo_postal INTEGER,
                    Municipio TEXT,
                    Provincia TEXT,
                    Comentario TEXT
                )
            ''')
            conn.commit()
            conn.close()
