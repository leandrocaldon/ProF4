from modelos.servicio import Servicio
from excepciones import ServicioInvalidoError


class Asesoria(Servicio):

    MULTIPLICADORES = {
        "basico": 1.0,
        "intermedio": 1.5,
        "avanzado": 2.0
    }

    def __init__(self, id, nombre, tarifa_base, nivel_especializacion):
        self.nivel_especializacion = nivel_especializacion
        super().__init__(id, nombre, tarifa_base)

    def validar_parametros(self):
        super().validar_parametros()

        if not isinstance(self.nivel_especializacion, str):
            raise ServicioInvalidoError(
                "El nivel de especialización debe ser texto."
            )

        if self.nivel_especializacion.lower() not in self.MULTIPLICADORES:
            raise ServicioInvalidoError(
                "El nivel debe ser basico, intermedio o avanzado."
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

        multiplicador = self.MULTIPLICADORES[
            self.nivel_especializacion.lower()
        ]

        return self.tarifa_base * duracion * multiplicador

    def describir(self):
        return (
            f"Asesoría: {self.nombre}. "
            f"Nivel: {self.nivel_especializacion}. "
            f"Tarifa por sesión: {self.tarifa_base}."
        )
