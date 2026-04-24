## Solución propuesta: Pipeline ETL

Se construyó un pipeline **ETL** (Extract → Transform → Load) compuesto por tres etapas:

### 1. Extract — `src/parser.py`
Se lee el archivo `log_casilleros.txt` línea por línea. Solo se procesan las líneas que contienen el evento `name=QUEUE_msg_received`. De cada línea válida se extrae:
- La **fecha y hora** mediante expresión regular.
- El **`moduloId`** parseando el campo `msg_body` como JSON.

### 2. Transform — `src/transformer.py`
Con los registros extraídos se construye un `DataFrame` de pandas donde:
- Se eliminan **duplicados** usando la combinación `(fecha_hora, moduloId)` como clave única (ya en el parser).
- Se **normalizan los tipos**: la fecha queda como `date` y la hora como `time`, separados desde el string original.
- Se descartan filas con fecha u hora inválida (`dropna`).

### 3. Load — `src/reporter.py`
Se genera un archivo Excel `casilleros_log_estructurado.xlsx` con dos hojas:

| Hoja | Columnas | Descripción |
|------|----------|-------------|
| **Registros** | `FECHA`, `HORA`, `NÚMERO DE MÓDULO` | Un registro por apertura única |
| **Resumen** | `Módulo`, `Veces abierto` | Conteo de aperturas por módulo, ordenado por ID |

La hoja **Resumen** responde directamente la pregunta del administrador.

---

## Estructura del proyecto

```
casilleros/
├── main.py                          # Entry point — orquesta el pipeline
├── log_casilleros.txt               # Archivo de log de entrada
├── log_pipeline.txt                 # Log de monitoreo generado en cada ejecución del Pipeline
├── casilleros_log_estructurado.xlsx # Archivo Excel de salida
└── src/
    ├── logger.py                    # Configuración del logger compartido
    ├── parser.py                    # Etapa Extract
    ├── transformer.py               # Etapa Transform
    └── reporter.py                  # Etapa Load
```

---

## Monitoreo

Cada ejecución genera o actualiza `log_pipeline.txt` con el detalle de lo que hizo el pipeline, incluyendo fecha, hora, módulo que lo registró y nivel del evento:

```
2026-04-24 10:23:01 | INFO     | main        | === Inicio del pipeline ===
2026-04-24 10:23:01 | INFO     | parser      | Iniciando lectura del archivo: log_casilleros.txt
2026-04-24 10:23:02 | INFO     | parser      | Lectura completada: 2925 registros únicos extraídos, 0 líneas omitidas.
2026-04-24 10:23:02 | INFO     | transformer | DataFrame listo: 2925 filas.
2026-04-24 10:23:02 | INFO     | reporter    | Archivo Excel escrito exitosamente.
2026-04-24 10:23:02 | INFO     | main        | === Fin del pipeline ===
```

Los niveles usados son `INFO` para el flujo normal y `WARNING` para situaciones inesperadas no fatales (JSON inválido, filas descartadas, log vacío).

---
## Tecnologías utilizadas
La solución fue desarrollada en Python como lenguaje de programación principal para la construcción de todas las funciones del pipeline. Las herramientas específicas usadas son:

**pandas** — para estructurar los registros extraídos en un DataFrame, aplicar la deduplicación, normalizar los tipos de fecha y hora, y generar el conteo de aperturas por módulo.
**openpyxl** — como motor de escritura para generar el archivo Excel de salida con sus dos hojas (Registros y Resumen).
**re (expresiones regulares)** — para identificar y extraer las líneas clave del log de casilleros: detectar el evento QUEUE_msg_received y capturar el timestamp de cada registro.
**logging** — módulo estándar de Python para el monitoreo del pipeline, que persiste cada paso de la ejecución en log_pipeline.txt

---

## Replicación

### Requisitos
- Python 3.10+

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd prueba_tecnica_proteccion
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Colocar el archivo de log

Asegúrate de que `log_casilleros.txt` (este es el nombre que se le dió al archivo proporcionado para ser tratado) esté en la raíz del proyecto (al mismo nivel que `main.py`).

### 4. Ejecutar el pipeline

```bash
python main.py
```

Al finalizar encontrarás `casilleros_log_estructurado.xlsx` y `log_pipeline.txt` en la raíz del proyecto.

---

## Dependencias (`requirements.txt`)

```
pandas
openpyxl
```