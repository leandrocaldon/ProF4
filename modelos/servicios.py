from abc import abstractmethod
from modelos.entidad import Entidad
from excepciones import ServicioInvalidoError


class Servicio(Entidad):

    def __init__(self, id, nombre, tarifa_base):
        super().__init__(id)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")

        if isinstance(self.tarifa_base, bool) or not isinstance(self.tarifa_base, (int, float)):
            raise ServicioInvalidoError("La tarifa base debe ser numérica.")

        if self.tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa base debe ser mayor que cero.")

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass
