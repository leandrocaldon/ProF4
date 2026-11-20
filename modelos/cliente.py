"""Cliente del sistema, con datos personales validados y encapsulados."""

from modelos.entidad import Entidad
from excepciones import ClienteInvalidoError
import re

class Cliente(Entidad):
    """Cliente con validaciones de nombre, documento, email y teléfono."""
    documentos_registrados = set()

    def __init__(self, nombre, documento, email, telefono):
        """Crea un cliente validando cada uno de sus datos."""
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
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida y guarda el nombre (no puede estar vacío)."""
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def documento(self):
        """Devuelve el documento del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor):
        """Valida y guarda el documento: solo números y sin repetir."""
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
        """Devuelve el email del cliente."""
        return self._email

    @email.setter
    def email(self, valor):
        """Valida y guarda el email con formato correcto."""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, str(valor)):
            raise ClienteInvalidoError("Email inválido")
        self._email = valor

    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Valida y guarda el teléfono: solo números."""
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
