# ======================================================================
# INTEGRANTE 4 - Reservas y cálculos (Jefferson)
# ESTADO: código real, es lo que Jefferson sube a su rama.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""
reserva.py
Clase Reserva: une cliente, servicio, duración y estado.
Autor: Jefferson Stick Murillo Córdoba
"""

import logging
from enum import Enum

from excepciones import CalculoError, EstadoReservaError, ReservaError
from modelos.entidad import Entidad
from servicios_core.calculadora import CalculadorCostos

logger = logging.getLogger(__name__)


class EstadoReserva(str, Enum):
    """Estados posibles de una reserva. También se pueden comparar con texto, ej. "PENDIENTE"."""
    PENDIENTE = "PENDIENTE"    # se acaba de crear
    CONFIRMADA = "CONFIRMADA"  # el cliente la aceptó
    CANCELADA = "CANCELADA"    # se anuló
    PROCESADA = "PROCESADA"    # el servicio ya se prestó


class Reserva(Entidad):
    """Reserva de un servicio hecha por un cliente."""

    def __init__(self, cliente, servicio, duracion):
        super().__init__()  # Entidad genera el id único
        if cliente is None or servicio is None:
            raise ReservaError("La reserva necesita un cliente y un servicio.")
        self._cliente = cliente                        # quién reserva
        self._servicio = servicio                      # qué servicio reserva
        self._duracion = self._validar_duracion(duracion)  # horas o días
        self._estado = EstadoReserva.PENDIENTE         # toda reserva empieza pendiente
        self._costo = None                             # se calcula al procesar
        logger.info(f"Reserva {self.id[:8]} creada con duración {self._duracion}. Estado: PENDIENTE.")

    @staticmethod
    def _validar_duracion(duracion):
        """Revisa que la duración sea un número mayor que cero."""
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ReservaError(f"La duración debe ser un número, llegó {duracion!r}.")
        if duracion <= 0:
            raise ReservaError(f"La duración debe ser mayor que cero, llegó {duracion}.")
        return duracion

    # ---------- propiedades de solo lectura ----------
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    # ---------- cambios de estado ----------
    def _cambiar_estado(self, permitidos, nuevo, accion):
        """Cambia el estado solo si el actual está entre los permitidos."""
        if self._estado not in permitidos:
            raise EstadoReservaError(
                f"No se puede {accion} una reserva en estado {self._estado.value}."
            )
        anterior = self._estado
        self._estado = nuevo
        logger.info(f"Reserva {self.id[:8]}: {anterior.value} -> {nuevo.value}.")

    def confirmar(self):
        """Solo sirve si está PENDIENTE."""
        self._cambiar_estado({EstadoReserva.PENDIENTE}, EstadoReserva.CONFIRMADA, "confirmar")

    def cancelar(self):
        """Sirve si está PENDIENTE o CONFIRMADA."""
        self._cambiar_estado({EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA},
                             EstadoReserva.CANCELADA, "cancelar")

    def procesar(self, impuesto=None, descuento=None):
        """Solo sirve si está CONFIRMADA. Calcula el costo y la deja PROCESADA."""
        if self._estado != EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                f"No se puede procesar una reserva en estado {self._estado.value}."
            )
        try:
            costo = CalculadorCostos.costo(self._servicio, self._duracion, impuesto, descuento)
        except CalculoError as error:
            # deja el registro y vuelve a lanzar el mismo CalculoError
            logger.error(f"No se pudo procesar {self.id[:8]}: {error}")
            raise
        else:
            # solo entra aquí si el cálculo salió bien
            self._costo = costo
            self._cambiar_estado({EstadoReserva.CONFIRMADA}, EstadoReserva.PROCESADA, "procesar")
            return costo
        finally:
            # se ejecuta siempre, haya salido bien o mal
            logger.info(f"Intento de procesar {self.id[:8]} terminado. Estado: {self._estado.value}.")

    # ---------- método abstracto de Entidad ----------
    def describir(self):
        """Devuelve un texto con los datos de la reserva."""
        costo = self._costo if self._costo is not None else "sin calcular"
        return (f"Reserva {self.id[:8]}: {self._servicio.nombre}, duración {self._duracion}, "
                f"estado {self._estado.value}, costo {costo}.")
