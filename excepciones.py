# ======================================================================
# INTEGRANTE 5 - Gestor, logs y simulación (rol sin asignar en el grupo)
# ESTADO: completado por Jefferson como propuesta para que el grupo lo revise.
# En main solo existía ClienteInvalidoError (la subió Sebastián). Se armó la
# jerarquía de la sección 4 del plan de trabajo, con los mismos nombres.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de SoftwareFJError para poder atraparlas juntas.
"""


class SoftwareFJError(Exception):
    """Base de todas las excepciones del sistema."""


# >>> CAMBIO: la subió Sebastián heredando de Exception; ahora hereda de SoftwareFJError.
class ClienteInvalidoError(SoftwareFJError):
    """Error cuando los datos del cliente son invalidos."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Los datos del servicio no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio existe pero no se puede reservar en este momento."""


class ReservaError(SoftwareFJError):
    """Error general de la reserva, ej. duración inválida o datos que no existen."""


class ReservaNoDisponibleError(ReservaError):
    """La reserva pedida no existe en el sistema."""


class EstadoReservaError(ReservaError):
    """Operación no permitida según el estado de la reserva."""


class CalculoError(SoftwareFJError):
    """Error en el cálculo del costo, ej. impuesto o descuento fuera de 0 a 1."""
