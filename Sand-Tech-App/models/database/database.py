import sqlite3
import os


class Database:
    def __init__(self, db_name="clientesDB.db", db_path="./models/database"):
        self.db_name = db_name
        self.db_path = db_path

    def conectar(self):
        ruta_db = os.path.join(self.db_path, self.db_name)
        return sqlite3.connect(ruta_db)

    def crear_tabla_clientes(self):
        try:
            conexion = self.conectar()
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    apellido TEXT,
                    nombre TEXT,
                    dni TEXT UNIQUE
                )""")
            conexion.execute(
                "INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('clientes', 99);")
            print("Se creó la tabla clientes")
            conexion.commit()
        except sqlite3.OperationalError as e:
            print(f"Error al crear la tabla clientes: {e}")
        finally:
            conexion.close()

    def cerrar_conexion(self, conexion):
        conexion.close()
