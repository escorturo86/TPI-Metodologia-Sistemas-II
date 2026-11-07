# Etapa 5: Refactorings seguros

Los fragmentos «antes» pertenecen al `app.py` del tag local `estado-inicial`; los fragmentos «después» pertenecen al `app.py` actualizado.

| N.º | Técnica | Función afectada | Propósito |
|---|---|---|---|
| 1 | Extract Method | `registrar_solicitud`, `pedir_datos_solicitud` | Separar las preguntas y validaciones del registro. |
| 2 | Reubicación de responsabilidad | `registrar_solicitud`, `crear_solicitud` | Construir la solicitud sin preguntar ni guardar. |
| 3 | Introduce Parameter Object / simplificación equivalente | `pedir_datos_solicitud`, `crear_solicitud` | Agrupar los cuatro datos de entrada en `detalles`. |
| 4 | Eliminar duplicación mediante Extract Method | `cambiar_estado`, `asignar_responsable`, `buscar_solicitud`, `convertir_id` | Compartir la conversión de IDs y la búsqueda de solicitudes. |

## 1. Extract Method

**Antes:**

```python
def registrar_solicitud(datos):
    for estudiante in datos["estudiantes"]:
        print(estudiante["id"], estudiante["nombre"])

    estudiante_ingresado = input("ID de estudiante: ").strip()
    if not estudiante_ingresado.isdigit():
        print("Dato inválido")
        return
```

**Después:**

```python
def pedir_datos_solicitud(datos):
    for estudiante in datos["estudiantes"]:
        print(estudiante["id"], estudiante["nombre"])

    estudiante_ingresado = input("ID de estudiante: ").strip()
    estudiante_id = convertir_id(estudiante_ingresado)
```

Las preguntas y sus validaciones salieron de `registrar_solicitud` y quedaron en `pedir_datos_solicitud`.  
El registro ahora recibe los datos preparados antes de crear y guardar la solicitud.

## 2. Reubicación de responsabilidad

**Antes:**

```python
    nuevo_id = max((solicitud["id"] for solicitud in datos["solicitudes"]), default=0) + 1
    solicitud = {
        "id": nuevo_id,
        "estudiante_id": estudiante_id,
        "tipo": tipos[tipo_ingresado],
        "prioridad": prioridades[prioridad_ingresada],
        "descripcion": descripcion,
        "estado": "pendiente",
        "responsable_id": None,
    }
```

**Después:**

```python
def crear_solicitud(datos, detalles):
    nuevo_id = max((solicitud["id"] for solicitud in datos["solicitudes"]), default=0) + 1
    solicitud = {
        "id": nuevo_id,
        "estudiante_id": detalles["estudiante_id"],
        "tipo": detalles["tipo"],
        "prioridad": detalles["prioridad"],
        "descripcion": detalles["descripcion"],
        "estado": "pendiente",
        "responsable_id": None,
    }
    return solicitud
```

La construcción del diccionario pasó a `crear_solicitud`.  
Esa función calcula el ID y devuelve la solicitud; no pide datos, no imprime y no guarda archivos.

## 3. Introduce Parameter Object / simplificación equivalente

**Antes:**

```python
    solicitud = {
        "id": nuevo_id,
        "estudiante_id": estudiante_id,
        "tipo": tipos[tipo_ingresado],
        "prioridad": prioridades[prioridad_ingresada],
        "descripcion": descripcion,
        "estado": "pendiente",
        "responsable_id": None,
    }
```

**Después:**

```python
    detalles = {
        "estudiante_id": estudiante_id,
        "tipo": TIPOS[tipo_ingresado],
        "prioridad": PRIORIDADES[prioridad_ingresada],
        "descripcion": descripcion,
    }
    return detalles
```

```python
    solicitud = crear_solicitud(datos, detalles)
```

Los cuatro valores que antes se usaban directamente al armar la solicitud ahora forman el diccionario `detalles`.  
`crear_solicitud` recibe ese único grupo de datos, sin clases ni objetos especiales.

## 4. Eliminar duplicación mediante Extract Method

**Antes:** el mismo fragmento estaba en `cambiar_estado` y `asignar_responsable`.

```python
    id_ingresado = input("ID de solicitud: ").strip()
    if not id_ingresado.isdigit():
        print("Dato inválido")
        return
    solicitud = next((solicitud for solicitud in datos["solicitudes"]
                      if solicitud["id"] == int(id_ingresado)), None)
```

**Después:**

```python
def convertir_id(texto):
    if not texto or not all("0" <= caracter <= "9" for caracter in texto):
        return None
    try:
        return int(texto)
    except ValueError:
        return None


def buscar_solicitud(datos, identificador):
    for solicitud in datos["solicitudes"]:
        if solicitud["id"] == identificador:
            return solicitud
    return None
```

```python
    solicitud_id = convertir_id(id_ingresado)
    if solicitud_id is None:
        print("Dato inválido")
        return
    solicitud = buscar_solicitud(datos, solicitud_id)
```

Las dos operaciones usan ahora las mismas funciones para convertir el ID y buscar la solicitud.  
Así, una corrección de estas tareas se hace en un solo lugar.

## Comprobaciones realizadas

Se ejecutaron sobre copias temporales de `app.py` y `datos.json` fuera del proyecto.

| N.º | Comprobación | Resultado |
|---|---|---|
| 1 | Registrar la solicitud de Ana con ID 1, tipo certificado, prioridad alta, estado pendiente y responsable vacío. | OK |
| 2 | Asignar la solicitud 1 a María Gómez y guardar el cambio. | OK |
| 3 | Cambiar la solicitud 1 a `en_proceso` y guardar el cambio. | OK |
| 4 | Filtrar por `en_proceso` y encontrar la solicitud. | OK |
| 5 | Reporte: total 1, pendiente 0, en_proceso 1, resuelta 0. | OK |
| 6 | Cerrar, volver a ejecutar y conservar la solicitud. | OK |
| 7 | Rechazar el ID 999 con `Dato inválido` sin cambiar el JSON. | OK |
| 8 | Rechazar `²` como ID de estudiante sin error de Python. | OK |
| 9 | Mostrar `Error en datos.json` ante JSON mal escrito y terminar sin menú. | OK |
| 10 | Mostrar `Datos inválidos` si falta `estudiantes` y terminar sin menú. | OK |
| 11 | Encontrar los datos al ejecutar desde otra carpeta e importar `app` sin iniciar el menú. | OK |
| 12 | Conservar los siete campos y no dejar `datos.tmp` después de guardar. | OK |

## Conclusión

Las 12 comprobaciones dieron `OK`. Las cinco operaciones y los resultados normales se conservaron; `datos.json` del proyecto no se modificó.
