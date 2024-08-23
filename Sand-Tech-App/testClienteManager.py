import unittest
from unittest.mock import Mock, patch
from controllers.clienteManager import ClienteManager
from models.cliente import Cliente
from models.database.database import Database


class TestClienteManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock(spec=Database)
        self.cliente_manager = ClienteManager(self.mock_db)
        self.mock_db.conectar.return_value.cursor.return_value.fetchall.return_value = [
            ("Perez", "Juan", "12345678")]

    def test_alta_cliente_exitoso(self):
        cliente = Cliente("Perez", "Juan", "12345678")
        self.cliente_manager.alta(cliente)
        self.mock_db.conectar.return_value.cursor.return_value.execute.assert_called_with(
            "INSERT INTO clientes(apellido, nombre, dni) VALUES (?, ?, ?)", ("Perez", "Juan", "12345678"))

    def test_consulta_cliente(self):
        resultado = self.cliente_manager.consulta(1)
        self.assertEqual(resultado, [("Perez", "Juan", "12345678")])
        self.mock_db.conectar.return_value.cursor.return_value.execute.assert_called_with(
            "SELECT apellido, nombre, dni FROM clientes WHERE codigo=?", (1,))

    def test_recuperar_todos(self):
        resultado = self.cliente_manager.recuperar_todos()
        self.assertEqual(resultado, [("Perez", "Juan", "12345678")])
        self.mock_db.conectar.return_value.cursor.return_value.execute.assert_called_with(
            "SELECT codigo, apellido, nombre, dni FROM clientes")

    def test_baja_cliente(self):
        self.mock_db.conectar.return_value.cursor.return_value.rowcount = 1
        resultado = self.cliente_manager.baja(1)
        self.assertEqual(resultado, 1)
        self.mock_db.conectar.return_value.cursor.return_value.execute.assert_called_with(
            "DELETE FROM clientes WHERE codigo=?", (1,))

    def test_modificacion_cliente(self):
        self.mock_db.conectar.return_value.cursor.return_value.fetchone.return_value = None
        self.mock_db.conectar.return_value.cursor.return_value.rowcount = 1
        resultado = self.cliente_manager.modificacion(
            ("Perez", "Juan", "12345678", 1))
        self.assertEqual(resultado, 1)
        self.mock_db.conectar.return_value.cursor.return_value.execute.assert_called_with(
            "UPDATE clientes SET apellido=?, nombre=?, dni=? WHERE codigo=?", ("Perez", "Juan", "12345678", 1))


if __name__ == "__main__":
    unittest.main()
