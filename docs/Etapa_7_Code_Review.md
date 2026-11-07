# Etapa 7: Code Review profesional

## Objetivo

Revisar la versión actual del sistema sin cambiar el código ni repetir las pruebas. Se comprueba el checklist pedido con el código, los documentos, la evidencia archivada y los tags locales.

## Checklist técnico

| N.º | Punto | Estado | Evidencia breve |
|---|---|---|---|
| 1 | Alcance | Cumple | `ejecutar` muestra las cinco operaciones y la opción de salir. |
| 2 | Código sencillo | Cumple | `app.py` usa funciones, listas y diccionarios, sin clases ni frameworks. |
| 3 | Responsabilidades separadas | Cumple | `pedir_datos_solicitud` pide y valida, `crear_solicitud` arma el diccionario y `registrar_solicitud` coordina y guarda. |
| 4 | Validación de IDs | Cumple | `pedir_datos_solicitud`, `cambiar_estado` y `asignar_responsable` llaman a `convertir_id` para los IDs ingresados. |
| 5 | Búsqueda compartida | Cumple | `cambiar_estado` y `asignar_responsable` llaman a `buscar_solicitud`. |
| 6 | Menús sin opciones duplicadas | Cumple | `mostrar_opciones` recibe `TIPOS`, `PRIORIDADES`, `ESTADOS` y `FILTROS` en las operaciones correspondientes. |
| 7 | JSON incorrecto | Cumple | `ejecutar` trata el archivo ausente y el JSON mal escrito, y usa `estructura_valida` para revisar la estructura. |
| 8 | Ruta de datos | Cumple | `RUTA_DATOS` se calcula desde la carpeta de `app.py`. |
| 9 | Guardado protegido | Cumple | `guardar_datos` escribe en `datos.tmp` y luego llama a `os.replace`. |
| 10 | Importación segura | Cumple | `app.py` llama a `ejecutar()` solo dentro de `if __name__ == "__main__":`. |
| 11 | Evidencia de pruebas | Cumple | `Etapa_6_Resultados.txt` registra 12/12 aprobadas y sus doce casos coinciden con `Etapa_6_Pruebas.md`. |
| 12 | Trazabilidad | Cumple | Existen los documentos de diagnóstico, planificación, refactoring y pruebas, y `git tag --list` muestra los cuatro tags locales pedidos. |

## Observaciones y feedback

1. **Ubicación:** `pedir_datos_solicitud`, `crear_solicitud` y `registrar_solicitud` en `app.py`; **observado:** el registro separa entrada, creación y guardado, lo que facilita entender cada tarea. **Feedback:** mantener estas funciones pequeñas y claras.
2. **Ubicación:** `convertir_id` y `buscar_solicitud` en `app.py`; **observado:** la validación y la búsqueda se reutilizan, lo que evita repetirlas en varias operaciones. **Feedback:** conservar estas funciones compartidas.
3. **Ubicación:** `estructura_valida` en `app.py`; **observado:** revisa presencia y tipos, pero no todas las relaciones entre IDs ni todos los valores permitidos si se edita el JSON a mano, por lo que ciertos datos incoherentes podrían pasar; es un límite no bloqueante. **Feedback:** anotarlo como mejora futura, sin cambiarlo ahora.
4. **Ubicación:** `guardar_datos` en `app.py`; **observado:** no presenta un mensaje propio ante errores de escritura o permisos, por lo que el usuario vería un error de Python; es un límite no bloqueante. **Feedback:** anotarlo como mejora futura, sin cambiarlo ahora.

## Correcciones realizadas en etapas anteriores

| Problema anterior | Corrección realizada | Evidencia en la versión actual |
|---|---|---|
| Registro con varias tareas juntas | Se dividió el registro en funciones sencillas. | `pedir_datos_solicitud`, `crear_solicitud` y `registrar_solicitud`. |
| Conversión y búsqueda de IDs repetidas | Se crearon funciones compartidas para convertir IDs y buscar solicitudes. | `convertir_id` y `buscar_solicitud`. |
| Opciones mostradas y definidas por separado | Se muestran desde los diccionarios de opciones. | `mostrar_opciones`, `TIPOS`, `PRIORIDADES`, `ESTADOS` y `FILTROS`. |
| Lectura, ruta y guardado frágiles de `datos.json` | Se agregaron validación de estructura, ruta junto a `app.py` y guardado mediante temporal. | `leer_datos`, `estructura_valida`, `RUTA_DATOS` y `guardar_datos`. |

## Criterios de aceptación

1. Los puntos 1 al 12 del checklist están en **Cumple**: **sí**.
2. La evidencia archivada informa **12/12** pruebas aprobadas y no se observa contradicción entre los documentos y el código revisado: **sí**.
3. Las observaciones 3 y 4 quedaron registradas como mejoras futuras no bloqueantes, sin considerarlas resueltas: **sí**.

**Resultado: Apto para continuar.**

## Conclusión

La revisión encontró 12 de 12 puntos cumplidos según el código y la evidencia disponible.  
Los dos límites pendientes quedaron registrados sin hacer correcciones nuevas.  
