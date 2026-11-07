# Etapa 4: Aplicación de SOLID y Clean Code

Se aplicaron las mejoras internas previstas para los nueve problemas del diagnóstico, sin cambiar las operaciones del sistema.

| N.º | Problema | Mejora aplicada |
|---|---|---|
| 1 | JSON mal formado | `ejecutar` muestra `Error en datos.json` si falla la lectura del JSON. |
| 2 | Estructura del JSON sin comprobar | `estructura_valida` comprueba las listas y los tipos de datos pedidos antes de abrir el menú. |
| 3 | Validación de ID | `convertir_id` acepta solo dígitos ASCII y devuelve `None` si la conversión falla. |
| 4 | Guardado directo | `guardar_datos` escribe en `datos.tmp` y reemplaza `datos.json` después de cerrar el archivo. |
| 5 | Ruta de datos | `RUTA_DATOS` localiza `datos.json` junto a `app.py`. |
| 6 | Registro con demasiadas tareas | `pedir_datos_solicitud` reúne las preguntas y `crear_solicitud` construye el diccionario sin interactuar con el usuario ni guardar. |
| 7 | Búsqueda repetida | `buscar_solicitud` sirve tanto para cambiar el estado como para asignar un responsable. |
| 8 | Opciones duplicadas | `mostrar_opciones` imprime las opciones desde los mismos diccionarios que interpretan la respuesta. |
| 9 | Inicio automático | El menú se ejecuta solo cuando `app.py` se inicia directamente. |

**SRP:** separar las preguntas, la creación y el guardado hace que cada función tenga una tarea más clara. **Clean Code:** se redujo la repetición y se reutilizaron validaciones con nombres comprensibles. **OCP** solo se relaciona parcialmente con la organización de las opciones; no se aplica plenamente. **LSP, ISP y DIP** no se implementaron en este programa sencillo.

Las cinco operaciones siguen siendo registrar, cambiar estado, asignar responsable, listar o filtrar y ver reporte.
