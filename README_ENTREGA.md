# Software FJ – Proyecto completo para revisar (Fase 4)

Versión armada por Jefferson (Integrante 4) el 20/11/2026 con el código que hay en GitHub
(`main` de Sebastián y `feature/servicios` de Lauren) más su módulo de reservas.

Al juntar los módulos tal como están en GitHub el código no se ejecutaba, porque las partes no se conectaban
entre ellas. Se hicieron ajustes pequeños para que funcione, y como el rol del Integrante 5 no lo tenía nadie
(somos 4), también se completó esa parte siguiendo el plan de trabajo (`docs/Plan_de_trabajo_equipo.md`).

Todo lo que se cambió o se agregó está marcado en el código con `>>> CAMBIO` (búsquenlo con Ctrl+F),
y cada archivo dice arriba de qué integrante es y qué se hizo.

## Cómo ejecutarlo

```
python main.py
```

Corre 10 operaciones de clientes, servicios y reservas, unas buenas y otras malas a propósito, mostrando
los datos de cada una y su resultado. El programa no se cae. Todos los errores y eventos quedan en
`logs/sistema.log` (se crea solo al ejecutar).

Pruebas de todos los módulos (48 pruebas):

```
pip install pytest
python -m pytest
```

No se le da Run a un archivo dentro de `tests/` (sale `ModuleNotFoundError`); se corren con el comando de arriba
desde la carpeta principal.

## Estado por integrante

### Integrante 1 – Coordinación (Leandro)
| Archivo | Qué se hizo |
|---|---|
| `main.py` | `>>> CAMBIO`: antes solo imprimía "Simulación pendiente". Ahora configura el log y corre la simulación. |

### Integrante 2 – Clientes (Sebastián)
| Archivo | Qué se hizo |
|---|---|
| `modelos/entidad.py` | Movido de la raíz a `modelos/` (el código lo importa como `modelos.entidad`). `>>> CAMBIO`: el id quedó opcional, `def __init__(self, id=None)`, porque Servicio le pasa un id y salía `TypeError`. |
| `modelos/cliente.py` | Movido de la raíz a `modelos/`. `>>> CAMBIO`: el documento se asigna de último; antes, si el correo estaba malo, el documento quedaba guardado y al corregirlo salía "Documento duplicado". |
| `tests/test_cliente.py` | Movido de la raíz a `tests/`. Sin cambios. Usa pytest. |

### Integrante 3 – Servicios (Lauren)
| Archivo | Qué se hizo |
|---|---|
| `modelos/servicio.py`, `sala.py`, `equipo.py`, `asesoria.py`, `tests/test_servicios.py` | Sin cambios, idénticos a la rama `feature/servicios`. Falta abrir su Pull Request. |

### Integrante 4 – Reservas y cálculos (Jefferson)
| Archivo | Qué se hizo |
|---|---|
| `modelos/reserva.py`, `servicios_core/calculadora.py`, `tests/test_reserva.py` | Ya están en GitHub: rama `feature/reservas-jeffersonMurillo` y Pull Request #1 hacia `main` (https://github.com/leandrocaldon/ProF4/pull/1). |

### Integrante 5 – Gestor, logs y simulación (rol sin asignar, hecho por Jefferson para revisión)
| Archivo | Qué hace |
|---|---|
| `excepciones.py` | Jerarquía completa del plan: `SoftwareFJError` como base, `ClienteInvalidoError`, `ServicioInvalidoError`, `ServicioNoDisponibleError`, `ReservaError`, `ReservaNoDisponibleError`, `EstadoReservaError`, `CalculoError`. `>>> CAMBIO`: `ClienteInvalidoError` (de Sebastián) ahora hereda de la base. |
| `utilidades/logger.py` | Configura `logs/sistema.log`; todos los módulos escriben ahí. |
| `servicios_core/gestor.py` | `GestorSistema` con listas internas de clientes, servicios y reservas. Cada operación usa try/except/else/finally y deja registro en el log. Encadena con `raise ... from` cuando la tarifa llega en texto. Permite marcar un servicio como no disponible. |
| `simulacion.py` | Las 10 operaciones, válidas e inválidas. Los datos son de ejemplo. |
| `tests/test_gestor.py` | 11 pruebas del gestor. |

## Qué pide la rúbrica y dónde está

| Requisito | Dónde |
|---|---|
| Excepciones personalizadas | `excepciones.py` |
| try/except, try/except/else, try/except/finally | `gestor.py` (todas las operaciones), `simulacion.py`, `reserva.py` (`procesar`) |
| Encadenamiento `raise ... from` | `gestor.py` (tarifa en texto), `calculadora.py` (error del servicio) |
| Errores y eventos en un archivo de logs | `utilidades/logger.py` → `logs/sistema.log` |
| Mínimo 10 operaciones, válidas e inválidas, sin caerse | `simulacion.py` (`python main.py`) |
| Datos erróneos, servicios no disponibles, reservas inválidas | Operaciones 2, 5, 7, 8, 9 y 10 de la simulación |
| Listas internas sin base de datos | `GestorSistema` |

## Cómo subirlo a GitHub

Cada integrante revisa su parte y la sube desde su cuenta y su rama, borrando el recuadro de comentarios de arriba
de cada archivo. La parte del Integrante 5 la puede subir quien el grupo decida.
