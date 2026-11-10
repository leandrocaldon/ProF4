# Plan de trabajo – Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)



---

## 1. Qué pide realmente la actividad (resumen)

| Requisito | Dónde se cumple |
|---|---|
| Clase abstracta para entidades generales | `Entidad` (base de `Cliente`, `Servicio`, `Reserva`) |
| Clase `Cliente` con validaciones y encapsulación de datos personales | `modelos/cliente.py` |
| Clase abstracta `Servicio` + **al menos 3** servicios derivados | `Servicio` → `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| Polimorfismo: calcular costo, describir, validar parámetros | Métodos sobrescritos en cada servicio |
| Clase `Reserva` (cliente, servicio, duración, estado) con confirmar / cancelar / procesar | `modelos/reserva.py` |
| Métodos sobrecargados (costo con impuestos, descuentos, parámetros opcionales) | `CalculadorCostos` (ver sección 4) |
| Listas internas para clientes, servicios, reservas | `GestorSistema` |
| Excepciones personalizadas + try/except, try/except/else, try/except/finally, encadenamiento (`raise ... from ...`) | `excepciones.py` y en todo el flujo |
| Log de todos los errores y eventos relevantes | `utilidades/logger.py` → `logs/sistema.log` |
| Mínimo 10 operaciones simuladas (válidas e inválidas) | `simulacion.py` |
| Sin base de datos | Solo objetos, listas y archivos de log |

---

## 2. Ideas para empezar

1. **Diseñar antes de programar.** Dibujar en equipo el diagrama de clases (puede ser en draw.io, Lucidchart o papel) y acordar nombres de clases, atributos y métodos.
2. **Definir el "contrato" entre partes.** Cada integrante debe saber qué recibe y qué devuelve cada clase, para que las piezas encajen sin sorpresas.
3. **Empezar por el esqueleto funcional.** Primero una versión mínima que haga *un* flujo completo (crear cliente → crear servicio → reservar → cancelar), y luego agregar robustez.
4. **Construir la jerarquía de excepciones primero.** Así todos usan las mismas excepciones desde el inicio.
5. **Un solo repositorio compartido (GitHub/GitLab)** con ramas por integrante y revisiones (pull requests) antes de unir al `main`.
6. **Pruebas tempranas.** Cada clase debe tener al menos un caso válido y uno inválido antes de integrarse.
7. **Documentar mientras se programa** (docstrings y README), no al final.

---

## 3. Estructura propuesta del proyecto

```
software_fj/
├── README.md                  # Descripción, cómo ejecutar, integrantes
├── main.py                    # Punto de entrada (ejecuta la simulación)
├── simulacion.py              # Mínimo 10 operaciones (válidas e inválidas)
├── excepciones.py             # Excepciones personalizadas
├── modelos/
│   ├── __init__.py
│   ├── entidad.py             # Clase abstracta Entidad
│   ├── cliente.py             # Cliente (validaciones, encapsulación)
│   ├── servicio.py            # Clase abstracta Servicio
│   ├── sala.py                # ReservaSala(Servicio)
│   ├── equipo.py              # AlquilerEquipo(Servicio)
│   ├── asesoria.py            # Asesoria(Servicio)
│   └── reserva.py             # Reserva (confirmar, cancelar, procesar)
├── servicios_core/
│   ├── __init__.py
│   ├── calculadora.py         # Métodos sobrecargados de costos
│   └── gestor.py              # GestorSistema: listas internas y operaciones
├── utilidades/
│   ├── __init__.py
│   └── logger.py              # Configuración del archivo de logs
├── logs/
│   └── sistema.log            # Generado al ejecutar
└── tests/
    ├── test_cliente.py
    ├── test_servicios.py
    ├── test_reserva.py
    └── test_gestor.py
```

---

## 4. Diseño sugerido (mínimo necesario)

**Jerarquía de excepciones personalizadas** (`excepciones.py`):
- `SoftwareFJError` (base)
  - `ClienteInvalidoError`
  - `ServicioInvalidoError`
  - `ReservaError`
    - `ReservaNoDisponibleError`
    - `EstadoReservaError` (operación no permitida según estado)
  - `ServicioNoDisponibleError`
  - `CalculoError`

**Clases:**
- `Entidad` (abstracta): atributo `id`, método abstracto `describir()`.
- `Cliente(Entidad)`: atributos privados `__nombre`, `__documento`, `__email`, `__telefono` con *properties* y validaciones.
- `Servicio(Entidad)` (abstracta): `nombre`, `tarifa_base`, métodos abstractos `calcular_costo()`, `validar_parametros()`, `describir()`.
  - `ReservaSala`: costo por hora y capacidad.
  - `AlquilerEquipo`: costo por día y cantidad de unidades.
  - `Asesoria`: costo por sesión y nivel de especialización.
- `Reserva`: cliente, servicio, duración, `estado` (PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA). Métodos `confirmar()`, `cancelar()`, `procesar()`; cada uno valida el estado actual y lanza `EstadoReservaError` si no es permitido.
- `CalculadorCostos` (sobrecarga, Python no tiene sobrecarga nativa → usar `*args`, `**kwargs` o parámetros opcionales con `None`):
  - `costo(servicio, duracion)`
  - `costo(servicio, duracion, impuesto=0.19)`
  - `costo(servicio, duracion, descuento=0.10)`
  - `costo(servicio, duracion, impuesto=..., descuento=...)`
- `GestorSistema`: listas `self.__clientes`, `self.__servicios`, `self.__reservas`; métodos `registrar_cliente()`, `registrar_servicio()`, `crear_reserva()`, `cancelar_reserva()`, etc.

**Patrón de manejo de errores** a usar en todas las operaciones (demuestra los tres bloques exigidos):
```python
try:
    cliente = Cliente(...)
except ClienteInvalidoError as e:
    registrar_log("ERROR", str(e))
else:
    gestor.registrar_cliente(cliente)
    registrar_log("INFO", "Cliente registrado")
finally:
    registrar_log("DEBUG", "Operación de registro finalizada")
```
Y para encadenamiento:
```python
try:
    tarifa = float(texto)
except ValueError as e:
    raise ServicioInvalidoError("Tarifa no numérica") from e
```

---

## 5. Reparto de responsabilidades (5 integrantes)

| Integrante | Rol | Entregables principales |
|---|---|---|
| **Integrante 1** – Coordinador / Arquitecto | Diseño general, README, repositorio, integración final | Diagrama de clases, `main.py`, README, revisión de PRs |
| **Integrante 2** – Clientes | Clase `Entidad` y `Cliente` con validaciones | `modelos/entidad.py`, `modelos/cliente.py`, tests de cliente |
| **Integrante 3** – Servicios | Clase abstracta `Servicio` y 3 servicios derivados | `modelos/servicio.py`, `sala.py`, `equipo.py`, `asesoria.py`, tests |
| **Integrante 4** – Reservas y cálculos | `Reserva` (estados) y `CalculadorCostos` (sobrecarga) | `modelos/reserva.py`, `servicios_core/calculadora.py`, tests |
| **Integrante 5** – Gestor, logs y simulación | `GestorSistema`, `logger.py`, excepciones y simulación de 10 operaciones | `servicios_core/gestor.py`, `utilidades/logger.py`, `excepciones.py`, `simulacion.py` |

> Todos revisan el código de al menos otro compañero, y todos aportan a la documentación final y al video/sustentación.

---

## 6. Cronograma sugerido

| Etapa | Fecha sugerida | Tareas | Responsable(s) |
|---|---|---|---|
| **1. Planeación** | Día 1–2 | Reunión inicial, reparto de roles, creación del repo, acordar convenciones (nombres en español, estilo PEP 8) | Todos |
| **2. Diseño** | Día 3 | Diagrama de clases y firmas de métodos, jerarquía de excepciones | Coordinador + todos |
| **3. Núcleo** | Día 4–7 | Clases base: `Entidad`, `Cliente`, `Servicio` y derivados, `Reserva` | Int. 2, 3, 4 |
| **4. Gestor y logs** | Día 7–9 | `GestorSistema`, logger, excepciones, calculadora | Int. 4, 5 |
| **5. Simulación** | Día 9–10 | `simulacion.py` con mínimo 10 operaciones (válidas e inválidas) | Int. 5 + Int. 1 |
| **6. Pruebas y depuración** | Día 11–12 | Tests, revisar que el programa no se caiga ante ningún error, revisar el log | Todos |
| **7. Documentación** | Día 13 | README, comentarios, informe, diagrama final | Int. 1 + Int. 2 |
| **8. Revisión y entrega** | Día 14 | Checklist final (sección 8), empaquetar y subir | Todos |

*Ajustar las fechas según el calendario real de la unidad.*

---

## 7. Flujo de trabajo con Git

1. Crear el repositorio y subir la estructura base (Integrante 1).
2. Cada integrante trabaja en su rama:
   - Integrante 1: `feature/base-documentacion` (estructura, `main.py`, README, integración)
   - Integrante 2: `feature/cliente`
   - Integrante 3: `feature/servicios`
   - Integrante 4: `feature/reservas`
   - Integrante 5: `feature/gestor-logs` (incluye excepciones y simulación)
3. Hacer commits pequeños y con mensajes claros, por ejemplo: `feat(cliente): validación de email`.
4. Abrir **Pull Request** hacia `main` y pedir revisión a un compañero.
5. Sincronizar con `main` al menos una vez al día para evitar conflictos (`git pull --rebase`).
6. No modificar archivos de otro integrante sin avisar en el grupo.



---

## 8. Checklist final antes de entregar

- [ ] Clase abstracta de entidades general implementada
- [ ] `Cliente` con validaciones y atributos encapsulados
- [ ] `Servicio` abstracto + al menos 3 servicios derivados con costo, descripción y validación sobrescritos
- [ ] `Reserva` con confirmar, cancelar y procesar, validando estados
- [ ] Métodos sobrecargados (costo con impuestos, descuentos, parámetros opcionales)
- [ ] Listas internas para clientes, servicios y reservas
- [ ] Excepciones personalizadas creadas y usadas
- [ ] Uso de `try/except`, `try/except/else`, `try/except/finally`
- [ ] Encadenamiento de excepciones (`raise ... from ...`)
- [ ] Todos los errores y eventos quedan en `logs/sistema.log`
- [ ] Simulación con **mínimo 10 operaciones**, incluyendo casos válidos e inválidos
- [ ] El programa **no se detiene** ante errores graves
- [ ] Sin bases de datos
- [ ] README con instrucciones de ejecución e integrantes
- [ ] Código comentado y ordenado
- [ ] Probado en un equipo distinto al del desarrollador (para verificar que ejecuta)

---

## 9. Próximo paso inmediato

1. Compartir este documento con el grupo.
2. Agendar una reunión de 1 hora para validar el reparto de roles y el diseño de clases.
3. Crear el repositorio y la estructura de carpetas de la sección 3.
4. Cada integrante escribe en el grupo qué rol acepta.
