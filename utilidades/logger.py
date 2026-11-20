# ======================================================================
# INTEGRANTE 5 - Gestor, logs y simulación (rol sin asignar en el grupo)
# ESTADO: hecho por Jefferson como propuesta para que el grupo lo revise.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""
logger.py
Configura el archivo de logs del sistema: logs/sistema.log.
Todos los módulos (clientes, servicios, reservas, gestor) escriben ahí.
"""

import logging
import os

CARPETA_LOGS = "logs"                                  # carpeta del archivo de logs
RUTA_LOG = os.path.join(CARPETA_LOGS, "sistema.log")   # archivo donde quedan errores y eventos


def configurar_logger():
    """Prepara el archivo de logs. Se llama una sola vez al iniciar el programa."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    logging.basicConfig(
        filename=RUTA_LOG,
        filemode="w",  # cada ejecución empieza el archivo de cero
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        encoding="utf-8",
        force=True,
    )


def registrar_log(nivel, mensaje):
    """Escribe un mensaje en el log. nivel: "INFO", "WARNING", "ERROR" o "CRITICAL"."""
    logging.getLogger("software_fj").log(getattr(logging, nivel.upper(), logging.INFO), mensaje)
