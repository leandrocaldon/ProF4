# ======================================================================
# INTEGRANTE 4 - Reservas y cálculos (Jefferson)
# ESTADO: código real, es lo que Jefferson sube a su rama.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""
calculadora.py
Calcula el costo de una reserva con impuesto y descuento opcionales.
Autor: Jefferson Stick Murillo Córdoba
"""

import logging

from excepciones import CalculoError, ServicioInvalidoError

logger = logging.getLogger(__name__)


class CalculadorCostos:
    """Calcula el costo de las reservas."""

    @staticmethod
    def _validar_porcentaje(valor, nombre):
        """Revisa que el impuesto o el descuento esté entre 0 y 1."""
        if valor is None:
            return
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise CalculoError(f"El {nombre} debe ser un número, llegó {valor!r}.")
        if not 0 <= valor <= 1:
            raise CalculoError(f"El {nombre} debe estar entre 0 y 1, llegó {valor}.")

    @staticmethod
    def costo(servicio, duracion, impuesto=None, descuento=None):
        """
        Método sobrecargado con parámetros opcionales:
        costo(servicio, duracion)                       -> precio normal
        costo(servicio, duracion, impuesto=0.19)        -> le suma el impuesto
        costo(servicio, duracion, descuento=0.10)       -> le resta el descuento
        costo(servicio, duracion, impuesto, descuento)  -> primero descuento, luego impuesto
        """
        CalculadorCostos._validar_porcentaje(impuesto, "impuesto")
        CalculadorCostos._validar_porcentaje(descuento, "descuento")

        try:
            total = servicio.calcular_costo(duracion)  # precio normal que da cada servicio
        except ServicioInvalidoError as error:
            # encadena el error del servicio con uno de cálculo
            raise CalculoError("El servicio no pudo calcular el costo.") from error

        if descuento is not None:
            total = total * (1 - descuento)  # resta el descuento

        if impuesto is not None:
            total = total * (1 + impuesto)   # suma el impuesto

        total = round(total, 2)
        logger.info(f"Costo calculado: {total} (impuesto={impuesto}, descuento={descuento})")
        return total
