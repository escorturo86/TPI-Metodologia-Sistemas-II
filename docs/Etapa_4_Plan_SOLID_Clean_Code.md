# Etapa 4: Plan de SOLID y Clean Code

## 1. Introducción

El sistema ya funciona y permite realizar las cinco operaciones previstas. En esta etapa se planifican mejoras internas a partir del diagnóstico anterior. Todavía no se cambia el código.

## 2. Mejoras previstas

| N.º del diagnóstico | Problema | Mejora prevista | Explicación |
|---|---|---|---|
| 1 | JSON mal formado | Mostrar un mensaje claro cuando no se pueda leer el JSON. | Un archivo mal escrito hoy interrumpe el inicio del programa. |
| 2 | Estructura del JSON sin comprobar | Comprobar que estén las listas y los datos necesarios al cargar el archivo. | Un JSON válido puede carecer de datos que el programa necesita. |
| 3 | Validación de ID | Usar una sola función para convertir IDs a enteros sin que el programa se cierre ante entradas inválidas. | La validación actual acepta algunos caracteres que después no se pueden convertir. |
| 4 | Guardado directo | Guardar primero en un archivo temporal y reemplazar el original al terminar. | El guardado actual vacía el archivo antes de escribir los datos nuevos. |
| 5 | Ruta de datos | Obtener la ruta de `datos.json` desde la ubicación de `app.py`. | La ruta actual depende de la carpeta desde la que se inicia Python. |
| 6 | Registro con demasiadas tareas | Separar la creación de la solicitud de la lectura de datos del usuario y del guardado, usando funciones simples. | El registro reúne preguntas, validaciones, creación y guardado en una función. |
| 7 | Búsqueda repetida | Usar una función común para buscar una solicitud por ID. | La misma búsqueda aparece al cambiar el estado y al asignar un responsable. |
| 8 | Opciones duplicadas | Mostrar las opciones desde el mismo diccionario que contiene sus valores. | Los nombres de las opciones están escritos tanto en el menú como en el diccionario. |
| 9 | Inicio automático | Ejecutar el menú con `if __name__ == "__main__":`. | El menú se inicia incluso cuando otro archivo carga `app.py`. |

## 3. SOLID

- **SRP:** se relaciona con separar tareas dentro de funciones pequeñas y es el principio que principalmente orienta este plan.
- **OCP:** no se aplica plenamente; organizar las opciones ayuda a evitar cambios repetidos.
- **LSP:** no corresponde aplicarlo porque no hay herencia.
- **ISP:** no corresponde aplicarlo porque no hay interfaces.
- **DIP:** no se implementará; no se crearán capas, clases ni abstracciones solo para cumplirlo.

## 4. Clean Code

El plan busca funciones con una tarea clara, menos repetición, validaciones reutilizadas, errores comprensibles y nombres claros.

## 5. Conclusión

Estas mejoras están previstas, pero todavía no se realizaron. Se conservarán las mismas cinco operaciones y se verificará su comportamiento cuando llegue la etapa de pruebas.
