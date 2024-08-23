import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from models.database.database import Database
from models.cliente import Cliente
from controllers.clienteManager import ClienteManager


class ClientesApp:
    def __init__(self):
        self.db = Database()
        self.db.crear_tabla_clientes()
        self.cliente_manager = ClienteManager(self.db)

        self.ventana1 = tk.Tk()
        self.ventana1.title("Gestión de clientes")
        self.cuaderno1 = ttk.Notebook(self.ventana1)

        self.alta_clientes()
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()

        self.cuaderno1.grid(column=0, row=0, padx=10, pady=10)
        self.ventana1.mainloop()

    def alta_clientes(self):
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="Alta de clientes")

        self.labelframe1 = ttk.LabelFrame(self.pagina1, text="Cliente")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)

        ttk.Label(self.labelframe1, text="Apellido:").grid(
            column=0, row=0, padx=4, pady=4)
        self.apellidoalta = tk.StringVar()
        ttk.Entry(self.labelframe1, textvariable=self.apellidoalta).grid(
            column=1, row=0, padx=4, pady=4)

        ttk.Label(self.labelframe1, text="Nombre:").grid(
            column=0, row=1, padx=4, pady=4)
        self.nombrealta = tk.StringVar()
        ttk.Entry(self.labelframe1, textvariable=self.nombrealta).grid(
            column=1, row=1, padx=4, pady=4)

        ttk.Label(self.labelframe1, text="DNI:").grid(
            column=0, row=2, padx=4, pady=4)
        self.dnialta = tk.StringVar()
        ttk.Entry(self.labelframe1, textvariable=self.dnialta).grid(
            column=1, row=2, padx=4, pady=4)

        ttk.Button(self.labelframe1, text="Confirmar", command=self.agregar).grid(
            column=1, row=3, padx=4, pady=4)

    def agregar(self):
        datos = (self.apellidoalta.get(),
                 self.nombrealta.get(), self.dnialta.get())
        cliente = Cliente(*datos)
        try:
            self.cliente_manager.alta(cliente)
            mb.showinfo("Información", "Los datos fueron cargados")
        except ValueError as e:
            mb.showerror("Error", str(e))
        self.apellidoalta.set("")
        self.nombrealta.set("")
        self.dnialta.set("")

    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text="Consulta por Nro de codigo")

        self.labelframe2 = ttk.LabelFrame(self.pagina2, text="Cliente")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)

        ttk.Label(self.labelframe2, text="Codigo:").grid(
            column=0, row=0, padx=4, pady=4)
        self.codigo = tk.StringVar()
        ttk.Entry(self.labelframe2, textvariable=self.codigo).grid(
            column=1, row=0, padx=4, pady=4)

        ttk.Label(self.labelframe2, text="Apellido:").grid(
            column=0, row=1, padx=4, pady=4)
        self.apellido = tk.StringVar()
        ttk.Entry(self.labelframe2, textvariable=self.apellido,
                  state="readonly").grid(column=1, row=1, padx=4, pady=4)

        ttk.Label(self.labelframe2, text="Nombre:").grid(
            column=0, row=2, padx=4, pady=4)
        self.nombre = tk.StringVar()
        ttk.Entry(self.labelframe2, textvariable=self.nombre,
                  state="readonly").grid(column=1, row=2, padx=4, pady=4)

        ttk.Label(self.labelframe2, text="DNI:").grid(
            column=0, row=3, padx=4, pady=4)
        self.dni = tk.StringVar()
        ttk.Entry(self.labelframe2, textvariable=self.dni,
                  state="readonly").grid(column=1, row=3, padx=4, pady=4)

        ttk.Button(self.labelframe2, text="Consultar", command=self.consultar).grid(
            column=1, row=4, padx=4, pady=4)

    def consultar(self):
        codigo = self.codigo.get()
        respuesta = self.cliente_manager.consulta(codigo)
        if respuesta:
            self.apellido.set(respuesta[0][0])
            self.nombre.set(respuesta[0][1])
            self.dni.set(respuesta[0][2])
        else:
            self.apellido.set('')
            self.nombre.set('')
            self.dni.set('')
            mb.showinfo("Información",
                        "No existe un cliente con dicho codigo")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Listado completo")

        self.labelframe3 = ttk.LabelFrame(
            self.pagina3, text="Listado de Clientes")
        self.labelframe3.grid(column=0, row=0, padx=5, pady=10)

        self.boton_listar = ttk.Button(
            self.labelframe3, text="Listar clientes", command=self.listar_clientes)
        self.boton_listar.grid(column=0, row=0, padx=4, pady=4)

        self.texto_listado = st.ScrolledText(
            self.labelframe3, width=30, height=10)
        self.texto_listado.grid(column=0, row=1, padx=4, pady=4)

    def listar_clientes(self):
        self.texto_listado.delete(1.0, tk.END)
        clientes = self.cliente_manager.recuperar_todos()
        if clientes:
            for cliente in clientes:
                self.texto_listado.insert(tk.END, f"Codigo: {cliente[0]}\n")
                self.texto_listado.insert(tk.END, f"Apellido: {cliente[1]}\n")
                self.texto_listado.insert(tk.END, f"Nombre: {cliente[2]}\n")
                self.texto_listado.insert(tk.END, f"DNI: {cliente[3]}\n\n")
        else:
            self.texto_listado.insert(tk.END, "No hay clientes registrados.")

    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina4, text="Borrado de clientes")

        self.labelframe4 = ttk.LabelFrame(
            self.pagina4, text="Cliente a borrar")
        self.labelframe4.grid(column=0, row=0, padx=5, pady=10)

        ttk.Label(self.labelframe4, text="Codigo:").grid(
            column=0, row=0, padx=4, pady=4)
        self.codigoborrar = tk.StringVar()
        ttk.Entry(self.labelframe4, textvariable=self.codigoborrar).grid(
            column=1, row=0, padx=4, pady=4)

        ttk.Button(self.labelframe4, text="Borrar", command=self.borrar).grid(
            column=1, row=1, padx=4, pady=4)

    def borrar(self):
        codigo = self.codigoborrar.get()
        if codigo:
            cantidad = self.cliente_manager.baja(codigo)
            if cantidad > 0:
                mb.showinfo("Información", "Cliente eliminado correctamente.")
            else:
                mb.showinfo("Información",
                            "No existe un cliente con dicho codigo.")
            self.codigoborrar.set("")
        else:
            mb.showwarning("Advertencia", "Debe ingresar un codigo.")

    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina5, text="Modificación de clientes")

        self.labelframe5 = ttk.LabelFrame(
            self.pagina5, text="Cliente a modificar")
        self.labelframe5.grid(column=0, row=0, padx=5, pady=10)

        ttk.Label(self.labelframe5, text="Codigo:").grid(
            column=0, row=0, padx=4, pady=4)
        self.codigomod = tk.StringVar()
        ttk.Entry(self.labelframe5, textvariable=self.codigomod).grid(
            column=1, row=0, padx=4, pady=4)

        ttk.Button(self.labelframe5, text="Consultar", command=self.consultar_modificacion).grid(
            column=1, row=1, padx=4, pady=4)

        self.labelframe6 = ttk.LabelFrame(self.pagina5, text="Modificar datos")
        self.labelframe6.grid(column=0, row=1, padx=5, pady=10)

        ttk.Label(self.labelframe6, text="Apellido:").grid(
            column=0, row=0, padx=4, pady=4)
        self.apellidomod = tk.StringVar()
        ttk.Entry(self.labelframe6, textvariable=self.apellidomod).grid(
            column=1, row=0, padx=4, pady=4)

        ttk.Label(self.labelframe6, text="Nombre:").grid(
            column=0, row=1, padx=4, pady=4)
        self.nombremod = tk.StringVar()
        ttk.Entry(self.labelframe6, textvariable=self.nombremod).grid(
            column=1, row=1, padx=4, pady=4)

        ttk.Label(self.labelframe6, text="DNI:").grid(
            column=0, row=2, padx=4, pady=4)
        self.dnimod = tk.StringVar()
        ttk.Entry(self.labelframe6, textvariable=self.dnimod).grid(
            column=1, row=2, padx=4, pady=4)

        ttk.Button(self.labelframe6, text="Modificar", command=self.modificar_datos).grid(
            column=1, row=3, padx=4, pady=4)

    def consultar_modificacion(self):
        codigo = self.codigomod.get()
        respuesta = self.cliente_manager.consulta(codigo)
        if respuesta:
            self.apellidomod.set(respuesta[0][0])
            self.nombremod.set(respuesta[0][1])
            self.dnimod.set(respuesta[0][2])
        else:
            self.apellidomod.set('')
            self.nombremod.set('')
            self.dnimod.set('')
            mb.showinfo("Información",
                        "No existe un cliente con dicho codigo")

    def modificar_datos(self):
        codigo = self.codigomod.get()
        if codigo:
            datos = (self.apellidomod.get(), self.nombremod.get(),
                     self.dnimod.get(), codigo)
            try:
                cantidad = self.cliente_manager.modificacion(datos)
                if cantidad > 0:
                    mb.showinfo("Información",
                                "Datos del cliente modificados correctamente.")
                else:
                    mb.showinfo("Información",
                                "No existe un cliente con dicho código.")
            except ValueError as e:
                mb.showerror("Error", str(e))
        else:
            mb.showwarning("Advertencia", "Debe ingresar un código.")
