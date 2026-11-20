"""
simulacion.py
Simula 10 operaciones del sistema Software FJ, válidas e inválidas,
mostrando los datos de cada una y su resultado, sin que el programa se caiga.
"""

from excepciones import SoftwareFJError
from servicios_core.gestor import GestorSistema
from utilidades.logger import RUTA_LOG, registrar_log

gestor = GestorSistema()                  # sistema con las listas internas
reservas = {}                             # reservas creadas en la simulación, por nombre
conteo = {"exitosas": 0, "con_error": 0}  # resultado de las operaciones


# ---------- operaciones que hacen varios pasos ----------
def reservar_y_procesar(clave, documento, id_servicio, duracion, impuesto=None, descuento=None):
    """Crea la reserva, la confirma y la procesa."""
    reserva = gestor.crear_reserva(documento, id_servicio, duracion)
    reservas[clave] = reserva
    gestor.confirmar_reserva(reserva.id)
    gestor.procesar_reserva(reserva.id, impuesto, descuento)
    return reserva.describir()


def reservar_servicio_fuera_de_servicio(documento, id_servicio, duracion):
    """Marca el servicio como no disponible e intenta reservarlo."""
    gestor.cambiar_disponibilidad(id_servicio, False)
    return gestor.crear_reserva(documento, id_servicio, duracion).describir()


# ---------- las 10 operaciones ----------
# (módulo, descripción, datos que entran, operación)
OPERACIONES = [
    ("Cliente", "Registrar cliente",
     "nombre=Ana Gómez | documento=1006123456 | email=ana@gmail.com | tel=3104567890",
     lambda: gestor.registrar_cliente("Ana Gómez", "1006123456", "ana@gmail.com", "3104567890").describir()),

    ("Cliente", "Registrar cliente con correo inválido",
     "nombre=Luis Pardo | documento=1122334455 | email=luis-gmail.com | tel=3001112233",
     lambda: gestor.registrar_cliente("Luis Pardo", "1122334455", "luis-gmail.com", "3001112233").describir()),

    ("Servicios", "Crear sala",
     "tipo=sala | id=S01 | nombre=Sala principal | tarifa por hora=100000 | capacidad=20",
     lambda: gestor.registrar_servicio("sala", "S01", "Sala principal", 100000, 20).describir()),

    ("Servicios", "Crear asesoría",
     "tipo=asesoria | id=A01 | nombre=Asesoría informática | tarifa por sesión=120000 | nivel=avanzado",
     lambda: gestor.registrar_servicio("asesoria", "A01", "Asesoría informática", 120000, "avanzado").describir()),

    ("Servicios", "Crear alquiler de equipos con tarifa en texto",
     "tipo=equipo | id=E01 | nombre=Computador | tarifa por día=cincuenta mil | unidades=3",
     lambda: gestor.registrar_servicio("equipo", "E01", "Computador", "cincuenta mil", 3).describir()),

    ("Reservas", "Reservar la sala 3 horas con 10 % de descuento y 19 % de IVA",
     "cliente=1006123456 | servicio=S01 | duración=3 | descuento=0.10 | impuesto=0.19",
     lambda: reservar_y_procesar("sala", "1006123456", "S01", 3, impuesto=0.19, descuento=0.10)),

    ("Reservas", "Reservar la asesoría cuando no está disponible",
     "cliente=1006123456 | servicio=A01 (marcado no disponible) | duración=2",
     lambda: reservar_servicio_fuera_de_servicio("1006123456", "A01", 2)),

    ("Reservas", "Reservar la sala con duración 0",
     "cliente=1006123456 | servicio=S01 | duración=0",
     lambda: reservar_y_procesar("cero", "1006123456", "S01", 0)),

    ("Reservas", "Procesar una reserva con descuento del 150 %",
     "cliente=1006123456 | servicio=S01 | duración=1 | descuento=1.5",
     lambda: reservar_y_procesar("descuento", "1006123456", "S01", 1, descuento=1.5)),

    ("Reservas", "Cancelar la reserva de la operación 6, que ya fue procesada",
     "reserva de la operación 6 | estado=PROCESADA",
     lambda: gestor.cancelar_reserva(reservas["sala"].id).describir()),
]


def ejecutar(numero, modulo, descripcion, datos, operacion):
    """Corre una operación con try/except/else/finally para que nada tumbe el programa."""
    print(f"\n[{numero:02d}] ({modulo}) {descripcion}")
    print(f"     Datos:     {datos}")
    registrar_log("INFO", f"--- Operación {numero} ({modulo}) {descripcion} | Datos: {datos}")
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        # errores previstos del sistema
        conteo["con_error"] += 1
        print(f"     Resultado: ERROR {type(error).__name__}: {error}")
        if error.__cause__ is not None:
            print(f"     Causa:     {type(error.__cause__).__name__}: {error.__cause__}")
    except Exception as error:
        # cualquier error que no se haya previsto
        conteo["con_error"] += 1
        print(f"     Resultado: FALLO INESPERADO {type(error).__name__}: {error}")
        registrar_log("CRITICAL", f"Operación {numero}: error inesperado {type(error).__name__}: {error}")
    else:
        conteo["exitosas"] += 1
        print(f"     Resultado: OK -> {resultado}")
    finally:
        print("     " + "-" * 64)


def ejecutar_simulacion():
    """Corre las 10 operaciones y muestra el resumen."""
    print("=" * 72)
    print("  SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print("=" * 72)
    registrar_log("INFO", "===== Inicio de la simulación =====")

    for numero, operacion in enumerate(OPERACIONES, start=1):
        ejecutar(numero, *operacion)

    print("\n" + "=" * 72)
    print(f"  Operaciones: {len(OPERACIONES)} | Exitosas: {conteo['exitosas']} | "
          f"Con error controlado: {conteo['con_error']}")
    print(f"  {gestor.resumen()}")
    print("  El programa terminó sin caerse.")
    print(f"  Los errores y eventos quedaron guardados en: {RUTA_LOG}")
    print("=" * 72)
    registrar_log("INFO", f"===== Fin de la simulación. {gestor.resumen()} =====")
