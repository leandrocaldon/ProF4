from modelos.servicio import Servicio
from excepciones import ServicioInvalidoError


class AlquilerEquipo(Servicio):

    def __init__(self, id, nombre, tarifa_base, cantidad_unidades):
        self.cantidad_unidades = cantidad_unidades
        super().__init__(id, nombre, tarifa_base)

    def validar_parametros(self):
        super().validar_parametros()

        if isinstance(self.cantidad_unidades, bool) or not isinstance(self.cantidad_unidades, int):
            raise ServicioInvalidoError(
                "La cantidad de equipos debe ser un número entero."
            )

        if self.cantidad_unidades <= 0:
            raise ServicioInvalidoError(
                "La cantidad de equipos debe ser mayor que cero."
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

        return self.tarifa_base * duracion * self.cantidad_unidades

    def describir(self):
        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Cantidad: {self.cantidad_unidades} unidades. "
            f"Tarifa por día: {self.tarifa_base}."
        )
