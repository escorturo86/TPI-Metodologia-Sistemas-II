# Etapa 3: Deuda técnica y code smells

## Introducción

Este diagnóstico parte de la Etapa 2, pero cada observación se contrastó con el `app.py` actual. `datos.json` tiene la estructura esperada y `README.md` indica ejecutar el programa desde la carpeta del proyecto. Los problemas siguientes están en el código; algunos se manifiestan solo ante datos dañados, una interrupción o una forma distinta de usar el programa. No se aplicaron cambios.

## Problemas identificados

| N.º | Problema | Archivo, función y línea | Riesgo de mantenimiento | Prioridad |
|---|---|---|---|---|
| 1 | JSON mal formado sin respuesta controlada | `app.py`, `leer_datos`, línea 6; `ejecutar`, líneas 147-149 | Alto: una falla del archivo interrumpe el programa sin un mensaje claro. | Alta |
| 2 | Estructura del JSON sin comprobar | `app.py`, `registrar_solicitud`, línea 15 | Alto: un cambio accidental en los datos provoca errores en distintas opciones. | Alta |
| 3 | Validación de ID que acepta ciertos caracteres no convertibles | `app.py`, `registrar_solicitud`, líneas 18-22; también `cambiar_estado`, líneas 66-71, y `asignar_responsable`, líneas 91-96 | Medio: una entrada inesperada puede cerrar el programa. | Media |
| 4 | Guardado directo sobre el único archivo de datos | `app.py`, `guardar_datos`, líneas 9-11 | Alto: una interrupción mientras se escribe puede dejar datos incompletos. | Alta |
| 5 | Ruta de datos dependiente de la carpeta de ejecución | `app.py`, `leer_datos`, línea 5; `guardar_datos`, línea 10 | Bajo: ejecutar desde otra carpeta obliga a investigar por qué no se encuentran los datos. | Baja |
| 6 | Registro con demasiadas tareas juntas | `app.py`, `registrar_solicitud`, líneas 14-62 | Medio: un cambio en el registro exige revisar una función extensa. | Media |
| 7 | Búsqueda y validación de solicitud repetidas | `app.py`, `cambiar_estado`, líneas 66-74; `asignar_responsable`, líneas 91-99 | Medio: una corrección puede quedar aplicada en una opción y faltar en la otra. | Media |
| 8 | Opciones escritas dos veces | `app.py`, `registrar_solicitud`, líneas 27-30 y 36-39; también `cambiar_estado`, líneas 76-79 | Medio: el texto mostrado y el valor guardado pueden dejar de coincidir. | Media |
| 9 | Inicio automático al cargar el archivo | `app.py`, fuera de función, línea 180 | Bajo: dificulta usar sus funciones desde otro archivo o revisarlas por separado. | Baja |

## Explicación y evidencia

### 1. JSON mal formado sin respuesta controlada

**Fragmento (`app.py`, líneas 6 y 147-149):**

```python
return json.load(archivo)

try:
    datos = leer_datos()
except FileNotFoundError:
    print("Falta datos.json")
```

**Por qué es un problema:** se atiende la ausencia del archivo, pero no el caso de un archivo que existe y contiene JSON mal escrito. **Dificultad posible:** el programa termina mostrando un error de Python, como se observó en la Etapa 2, y el usuario no puede continuar. **Posible solución:** reconocer también el error de lectura de JSON y mostrar un mensaje claro.

### 2. Estructura del JSON sin comprobar

**Fragmento (`app.py`, línea 15):**

```python
for estudiante in datos["estudiantes"]:
```

**Por qué es un problema:** `json.load` comprueba la sintaxis, pero no que estén las listas y los campos que el programa espera. El `datos.json` actual sí los tiene; el riesgo aparece si se edita o daña. **Dificultad posible:** si falta `estudiantes`, esta opción termina con `KeyError`; otras opciones dependen de `solicitudes` y `responsables`. **Posible solución:** comprobar la estructura necesaria al cargar los datos y avisar si no es válida.

### 3. Validación de ID que acepta ciertos caracteres no convertibles

**Fragmento (`app.py`, líneas 18-22):**

```python
estudiante_ingresado = input("ID de estudiante: ").strip()
if not estudiante_ingresado.isdigit():
    print("Dato inválido")
    return
estudiante_id = int(estudiante_ingresado)
```

**Por qué es un problema:** `"²".isdigit()` da `True`, pero `int("²")` produce un error. La misma combinación aparece al pedir otros IDs. **Dificultad posible:** una entrada no prevista interrumpe el menú en vez de mostrar `Dato inválido`. **Posible solución:** validar usando una conversión a entero controlada y tratar el fallo como dato inválido.

### 4. Guardado directo sobre el único archivo de datos

**Fragmento (`app.py`, líneas 9-11):**

```python
def guardar_datos(datos):
    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
```

**Por qué es un problema:** abrir con `"w"` vacía el archivo antes de escribir el contenido nuevo. **Dificultad posible:** si el proceso se interrumpe durante la escritura, el único archivo puede quedar incompleto y luego no abrirse. **Posible solución:** escribir primero el contenido completo en un archivo temporal y reemplazar el original al terminar.

### 5. Ruta de datos dependiente de la carpeta de ejecución

**Fragmento (`app.py`, líneas 5 y 10):**

```python
with open("datos.json", "r", encoding="utf-8") as archivo:
with open("datos.json", "w", encoding="utf-8") as archivo:
```

**Por qué es un problema:** el nombre relativo busca el archivo en la carpeta desde la que se ejecutó Python. El README indica correctamente entrar en la carpeta del proyecto, por lo que el uso documentado funciona. **Dificultad posible:** al lanzar el programa desde otra carpeta, puede informar que falta el archivo aunque esté junto a `app.py`. **Posible solución:** construir la ruta a partir de la ubicación de `app.py`.

### 6. Registro con demasiadas tareas juntas

**Fragmentos (`app.py`, líneas 14-18 y 50-62):**

```python
def registrar_solicitud(datos):
    for estudiante in datos["estudiantes"]:
        print(estudiante["id"], estudiante["nombre"])

    estudiante_ingresado = input("ID de estudiante: ").strip()
```

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
    datos["solicitudes"].append(solicitud)
    guardar_datos(datos)
    print(f"Solicitud registrada: ID {nuevo_id}")
```

**Por qué es un problema:** una sola función muestra opciones, pide datos, los valida, arma la solicitud y la guarda. **Dificultad posible:** al modificar una de esas tareas hay que recorrer toda la función para entender sus efectos. **Posible solución:** cuando corresponda refactorizar, separar la entrada y validación de la creación y el guardado mediante funciones sencillas.

### 7. Búsqueda y validación de solicitud repetidas

**Fragmentos (`app.py`, líneas 66-74 y 91-99):**

```python
id_ingresado = input("ID de solicitud: ").strip()
if not id_ingresado.isdigit():
    print("Dato inválido")
    return
solicitud = next((solicitud for solicitud in datos["solicitudes"]
                  if solicitud["id"] == int(id_ingresado)), None)
```

**Por qué es un problema:** este bloque aparece tanto al cambiar el estado como al asignar un responsable. **Dificultad posible:** corregir la validación en un lugar y olvidar el otro genera comportamientos diferentes. **Posible solución:** reunir la búsqueda y validación de la solicitud en una función compartida.

### 8. Opciones escritas dos veces

**Fragmento (`app.py`, líneas 27-30):**

```python
print("1. certificado")
print("2. equivalencia")
print("3. consulta")
tipos = {"1": "certificado", "2": "equivalencia", "3": "consulta"}
```

**Por qué es un problema:** los nombres y números están repetidos en lo que ve el usuario y en la tabla que interpreta su elección. Ocurre también con prioridades y estados. **Dificultad posible:** si se cambia una opción en un lugar y no en el otro, el menú anuncia algo distinto de lo que registra. **Posible solución:** mostrar las opciones a partir de la misma tabla que se usa para interpretarlas.

### 9. Inicio automático al cargar el archivo

**Fragmento (`app.py`, línea 180):**

```python
ejecutar()
```

**Por qué es un problema:** la llamada está fuera de una condición; cargar `app.py` desde otro programa inicia el menú de inmediato. **Dificultad posible:** resulta incómodo revisar o reutilizar una función aislada sin abrir el programa entero. **Posible solución:** ejecutar el menú solo cuando `app.py` sea el archivo iniciado directamente.

## Conclusión

Se identificaron **9 problemas reales**. El sistema funciona con los datos actuales y según la forma de ejecución documentada, pero estos puntos pueden dificultar su mantenimiento o su respuesta ante situaciones inesperadas. Las soluciones son propuestas para una etapa posterior.