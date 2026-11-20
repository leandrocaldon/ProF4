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
