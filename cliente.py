from modelos.entidad import Entidad
from excepciones import ClienteInvalidoError
import re

class Cliente(Entidad):
    documentos_registrados = set()

    def __init__(self, nombre, documento, email, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

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