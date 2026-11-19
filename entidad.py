"""
Modulo que contiene la clase base de las entidades.
"""

from abc import ABC, abstractmethod
from uuid import uuid4


class Entidad(ABC):
    """Clase abstracta que representa una entidad del sistema."""

    def __init__(self):
        """Inicializa una entidad con un identificador unico."""
        self.__id = str(uuid4())

    @property
    def id(self):
        """Obtiene el identificador unico de la entidad."""
        return self.__id

    @abstractmethod
    def describir(self):
        """Define el metodo que deben implementar las clases hijas."""
        pass