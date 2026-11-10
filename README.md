# ProF4
Fase 4 - componente práctico - prácticas simuladas

## Software FJ: Sistema Integral de Gestión de Clientes, Servicios y Reservas

Sistema en Python (sin base de datos) para gestionar clientes, servicios y reservas, con registro de eventos y errores en `logs/sistema.log`.

### Estructura
```
main.py              # Punto de entrada
modelos/             # Entidad, Cliente, Servicio (abstracto), ReservaSala, AlquilerEquipo, Asesoria, Reserva
servicios_core/      # CalculadorCostos y GestorSistema
utilidades/          # Configuración del logger
tests/               # Pruebas unitarias
logs/                # Archivo de log generado al ejecutar
docs/                # Plan de trabajo del equipo
```

### Ejecución
```bash
python main.py
```

### Integrantes
Ver el reparto de roles en [docs/Plan_de_trabajo_equipo.md](docs/Plan_de_trabajo_equipo.md), sección 5.

### Flujo de trabajo
Ramas por integrante (`feature/...`), commits pequeños y Pull Request hacia `main`.
