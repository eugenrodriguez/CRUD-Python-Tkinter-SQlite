class Cliente:
    def __init__(self, apellido, nombre, dni):
        self.apellido = apellido
        self.nombre = nombre
        self.dni = dni

    def obtener_datos(self):
        return (self.apellido, self.nombre, self.dni)
