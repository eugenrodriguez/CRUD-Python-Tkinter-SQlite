import sqlite3
from models.cliente import Cliente
from logger.logger import Logger


class ClienteManager:
    def __init__(self, db):
        self.db = db
        self.logger = Logger()

    def alta(self, cliente):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            datos = cliente.obtener_datos()
            if datos[0] == "" or datos[1] == "" or datos[2] == "":
                raise ValueError(
                    "El nombre, apellido y DNI no pueden estar vacíos")

            sql = "INSERT INTO clientes(apellido, nombre, dni) VALUES (?, ?, ?)"
            cursor.execute(sql, datos)
            conexion.commit()
            self.logger.info(f"Alta de cliente: {datos}")
        except sqlite3.IntegrityError:
            self.logger.error(
                f"Error al dar de alta cliente con DNI existente: {datos[2]}")
            raise ValueError("El DNI ingresado ya existe.")
        finally:
            self.db.cerrar_conexion(conexion)

    def consulta(self, codigo):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = "SELECT apellido, nombre, dni FROM clientes WHERE codigo=?"
            cursor.execute(sql, (codigo,))
            self.logger.info(f"Consulta de cliente con código: {codigo}")

            return cursor.fetchall()
        finally:
            self.db.cerrar_conexion(conexion)

    def recuperar_todos(self):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = "SELECT codigo, apellido, nombre, dni FROM clientes"
            cursor.execute(sql)
            self.logger.info("Consulta de todos los clientes")
            return cursor.fetchall()
        finally:
            self.db.cerrar_conexion(conexion)

    def baja(self, codigo):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM clientes WHERE codigo=?"
            cursor.execute(sql, (codigo,))
            conexion.commit()
            cantidad = cursor.rowcount
            if cantidad > 0:
                self.logger.info(f"Baja de cliente con código: {codigo}")
            else:
                self.logger.warning(
                    f"Intento de baja de cliente con código no existente: {codigo}")
            return cantidad
        finally:
            self.db.cerrar_conexion(conexion)

    def modificacion(self, datos):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()

            if datos[0] == "" or datos[1] == "" or datos[2] == "":
                raise ValueError(
                    "El nombre, apellido y DNI no pueden estar vacíos")

            # Verificar si el nuevo DNI ya existe
            nuevo_dni = datos[2]
            codigo_cliente = datos[3]
            cursor.execute(
                "SELECT codigo FROM clientes WHERE dni=? AND codigo!=?", (nuevo_dni, codigo_cliente))
            if cursor.fetchone() is not None:
                self.logger.error(f"Error al modificar cliente: DNI {
                                  nuevo_dni} ya existe.")
                raise ValueError("El DNI ingresado ya existe.")

            sql = "UPDATE clientes SET apellido=?, nombre=?, dni=? WHERE codigo=?"
            cursor.execute(sql, datos)
            conexion.commit()
            cantidad = cursor.rowcount
            if cantidad > 0:
                self.logger.info(f"Modificación de cliente: {datos}")
            else:
                self.logger.warning(
                    f"Intento de modificación de cliente con código no existente: {datos}")
            return cantidad
        finally:
            self.db.cerrar_conexion(conexion)
