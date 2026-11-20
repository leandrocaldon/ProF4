# ======================================================================
# INTEGRANTE 2 - Clientes (Sebastián)
# ESTADO: código real de main, con 1 cambio (buscar >>> CAMBIO)
# MOVIDO: de la raíz del repo a modelos/cliente.py.
#   Por qué: el test lo importa como 'from modelos.cliente import Cliente'
#   y el plan de trabajo lo pone en modelos/.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

from modelos.entidad import Entidad
from excepciones import ClienteInvalidoError
import re

class Cliente(Entidad):
    documentos_registrados = set()

    def __init__(self, nombre, documento, email, telefono):
        super().__init__()
        self.nombre = nombre
        # >>> CAMBIO: el documento se asigna de último (antes iba de segundo).
        #     Antes, si el email o el teléfono estaban malos, el documento ya quedaba
        #     guardado en documentos_registrados y al corregir los datos salía "Documento duplicado".
        self.email = email
        self.telefono = telefono
        self.documento = documento

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if not valor or not str(valor).strip():
            raise ClienteInvalidoError("El documento no puede estar vacío")
        valor = str(valor).strip()
        if not valor.isdigit():
            raise ClienteInvalidoError("El documento debe contener solo números")
        if valor in Cliente.documentos_registrados:
            raise ClienteInvalidoError("Documento duplicado")
        Cliente.documentos_registrados.add(valor)
        self._documento = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, str(valor)):
            raise ClienteInvalidoError("Email inválido")
        self._email = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).strip():
            raise ClienteInvalidoError("El teléfono no puede estar vacío")
        valor = str(valor).strip()
        if not valor.isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números")
        self._telefono = valor

    def describir(self):
        """Devuelve una descripcion completa del cliente."""
        return (
            f"Cliente: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Email: {self.email} | "
            f"Telefono: {self.telefono}"
        )
