from modelos.servicio import Servicio
from excepciones import ServicioInvalidoError


class ReservaSala(Servicio):

    def __init__(self, id, nombre, tarifa_base, capacidad):
        self.capacidad = capacidad
        super().__init__(id, nombre, tarifa_base)

    def validar_parametros(self):
        super().validar_parametros()

        if isinstance(self.capacidad, bool) or not isinstance(self.capacidad, int):
            raise ServicioInvalidoError(
                "La capacidad debe ser un número entero."
            )

        if self.capacidad <= 0:
            raise ServicioInvalidoError(
                "La capacidad debe ser mayor que cero."
            )

    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ServicioInvalidoError(
                "La duración debe ser numérica."
            )

        if duracion <= 0:
            raise ServicioInvalidoError(
                "La duración debe ser mayor que cero."
            )

        return self.tarifa_base * duracion

    def describir(self):
        return (
            f"Sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas. "
            f"Tarifa por hora: {self.tarifa_base}."
        )
