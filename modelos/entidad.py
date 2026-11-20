"""
Modulo que contiene la clase base de las entidades.
"""

from abc import ABC, abstractmethod
from uuid import uuid4


class Entidad(ABC):
    """Clase abstracta que representa una entidad del sistema."""

    # >>> CAMBIO: antes era def __init__(self):
    #     Servicio (Lauren) hace super().__init__(id) y daba TypeError porque no recibía nada.
    #     Con id opcional sirve para los dos: Cliente y Reserva no pasan id, Servicio sí.
    def __init__(self, id=None):
        """Inicializa una entidad con un identificador unico."""
        self.__id = str(id) if id is not None else str(uuid4())  # >>> CAMBIO (antes: self.__id = str(uuid4()))

    @property
    def id(self):
        """Obtiene el identificador unico de la entidad."""
        return self.__id

    @abstractmethod
    def describir(self):
        """Define el metodo que deben implementar las clases hijas."""
        pass
