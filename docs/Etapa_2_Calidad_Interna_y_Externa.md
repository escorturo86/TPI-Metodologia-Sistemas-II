# TPI - Etapa 2: Calidad externa e interna

**Materia:** Metodología de Sistemas II  
**Sistema:** Gestión de Solicitudes Académicas  
**Versión analizada:** versión inicial, anterior al refactoring (`estado-inicial`).  
**Archivos revisados:** `app.py`, `datos.json` y `README.md` del proyecto entregado.

## 1. Objetivo

Analizar cómo funciona el programa desde el punto de vista del usuario (calidad externa) y cómo está organizado su código (calidad interna). En esta etapa **no se modifica el programa**.

## 2. Descripción breve del sistema

Es un programa sencillo de consola, desarrollado en Python. Permite registrar solicitudes académicas, cambiar su estado, asignar un responsable, listar o filtrar solicitudes y consultar un reporte. Guarda la información en `datos.json`.

Utiliza tres estructuras principales: **estudiantes**, **responsables** y **solicitudes**. Los datos de ejemplo son ficticios.

## 3. Calidad externa

La calidad externa es lo que vemos cuando usamos el sistema: si permite realizar las tareas y responde de manera adecuada.

| Función o situación probada | Resultado | Evidencia observada |
|---|---|---|
| Registrar una solicitud | Correcto | Se crea la solicitud con ID 1. |
| Asignar un responsable | Correcto | La solicitud queda asignada al responsable con ID 1. |
| Cambiar su estado | Correcto | El estado cambia a `en_proceso`. |
| Filtrar solicitudes | Correcto | La solicitud aparece en el filtro `en_proceso`. |
| Ver el reporte | Correcto | Total: 1; pendiente: 0; en_proceso: 1; resuelta: 0. |
| Cerrar y volver a abrir | Correcto | La solicitud se conserva en el archivo JSON. |
| Ingresar un ID inexistente | Correcto | Muestra `Dato inválido` y no modifica el archivo. |
| Ingresar una descripción vacía | Correcto | Rechaza el dato sin guardar cambios. |
| Elegir una opción inexistente del menú | Correcto | Muestra `Dato inválido`. |
| Iniciar sin `datos.json` | Correcto | Muestra `Falta datos.json` y finaliza. |
| Iniciar con un JSON mal formado | **Error detectado** | El programa termina con `JSONDecodeError` en lugar de mostrar un mensaje sencillo. |

**Cómo se verificó:** se ejecutó una copia temporal de `app.py` y `datos.json` enviando las opciones del menú y revisando las respuestas y el contenido guardado. **Diez de las once comprobaciones dieron resultado correcto.** La última es una prueba adicional de resistencia ante un archivo dañado; no formaba parte de las siete pruebas originales de la Etapa 1.

**Conclusión de calidad externa:** el sistema cumple las funciones solicitadas en condiciones normales. Todavía podría responder mejor ante algunas situaciones inesperadas, como un archivo de datos dañado.

## 4. Calidad interna

La calidad interna es cómo está escrito y organizado el programa. No siempre se ve desde el menú, pero influye en la facilidad para corregir errores y agregar cambios en el futuro.

| Observación | Dónde se ve | Por qué importa |
|---|---|---|
| El código usa funciones con nombres fáciles de entender. | `app.py`, funciones `registrar_solicitud`, `cambiar_estado`, etc. | Facilita leer el programa. Es un punto positivo. |
| Todo está concentrado en un solo archivo de 180 líneas. | `app.py` completo. | Es simple ahora, pero puede ser más difícil de mantener si crece. |
| Registrar una solicitud reúne la carga de datos, la validación, la creación y el guardado. | `app.py`, líneas 14 a 62. | Cambiar esa función puede requerir revisar varias tareas juntas. |
| Se repite la búsqueda y validación del ID de solicitud. | `app.py`, líneas 65 a 74 y 90 a 99. | Si queremos cambiar esa comprobación, hay que hacerlo en más de un lugar. |
| Las funciones combinan preguntas al usuario, mensajes y cambios en los datos. | Por ejemplo, `app.py`, líneas 14 a 62 y 90 a 114. | Resulta más difícil comprobar una parte sin ejecutar el menú. |
| Solo se controla expresamente que falte el archivo JSON. | `app.py`, líneas 146 a 151. | Un archivo con contenido incorrecto puede interrumpir el programa. |
| El archivo JSON se busca por su nombre en la carpeta desde la cual se ejecuta Python. | `app.py`, líneas 4 a 11. | El funcionamiento depende de ejecutar el programa desde la carpeta indicada en el README. |

**Conclusión de calidad interna:** el código es corto, claro y funciona, pero se pueden separar mejor algunas tareas, evitar repeticiones y manejar ciertos errores. Estas son observaciones iniciales; la identificación detallada y priorización de al menos ocho problemas corresponde a la **Etapa 3**.

## 5. Diferencia entre calidad externa e interna

El usuario puede registrar y consultar solicitudes sin notar cómo está organizado el código. Eso muestra una calidad externa adecuada para el alcance pedido. Sin embargo, algunas partes del programa repiten pasos o combinan demasiadas tareas. Eso afecta a la calidad interna y podría dificultar futuras modificaciones.

**Ejemplo concreto:** cambiar el estado de una solicitud funciona correctamente. Pero la validación del ID de solicitud está escrita también en la opción de asignar responsable. Si cambia la forma de validar los IDs, hay que revisar ambas partes. El usuario no ve esta repetición, pero quien mantiene el programa sí.

## 6. Evidencias que guardaremos para el informe final

- Captura del menú principal funcionando.
- Captura de una solicitud registrada, asignada y cambiada de estado.
- Captura del filtro y el reporte con los valores `1, 0, 1, 0`.
- Fragmentos de `app.py` donde se observan las funciones y las validaciones repetidas.
- Referencia al repositorio de GitHub y al tag `estado-inicial`.


**Repositorio:** https://github.com/escorturo86/TPI-Metodologia-Sistemas-II

## 7. Conclusión

La versión inicial cumple las tareas principales y conserva los datos correctamente. Su código también es sencillo de leer, aunque presenta aspectos mejorables en la organización y el manejo de errores. Por eso, en la siguiente etapa vamos a identificar problemas concretos, explicar su impacto y decidir cuáles conviene corregir primero. **En esta etapa no se realizó ningún refactoring ni se modificaron los archivos originales.**
