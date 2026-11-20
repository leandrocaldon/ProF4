# ======================================================================
# INTEGRANTE 1 - Coordinación (Leandro)
# ESTADO: el de main solo imprimía "estructura base lista. Simulación pendiente."
# >>> CAMBIO: ahora configura el log y corre la simulación (lo que decía su docstring).
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""Punto de entrada del Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ).

La simulación completa está en `simulacion.py`.
"""

from simulacion import ejecutar_simulacion
from utilidades.logger import configurar_logger


def main() -> None:
    configurar_logger()      # prepara logs/sistema.log
    ejecutar_simulacion()    # corre las 10 operaciones


if __name__ == "__main__":
    main()
