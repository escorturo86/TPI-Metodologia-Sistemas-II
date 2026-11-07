# Etapa 6: Pruebas y verificación

## Objetivo

Se verifica que el comportamiento normal del sistema se conserve después del refactoring. También se comprueban los casos especiales indicados para la versión actual.

## Cómo se probó

Se ejecutó `python tests/verificar_etapa6.py`. El script comparó el tag `estado-inicial` con el programa actual y usó carpetas temporales para los programas y los datos.

## Resultados

| N.º | Caso | Resultado | Evidencia breve |
|---|---|---|---|
| 1 | Registrar solicitud de Ana, tipo certificado, prioridad alta. | OK | Se registró la solicitud ID 1 con estudiante, tipo y prioridad esperados. |
| 2 | Asignar responsable 1 a solicitud 1. | OK | Se mostró `Responsable asignado` y quedó el ID 1 en el JSON. |
| 3 | Cambiar estado a `en_proceso`. | OK | Se mostró `Estado actualizado` y quedó ese estado en el JSON. |
| 4 | Filtrar por `en_proceso`. | OK | La solicitud apareció en la salida del filtro. |
| 5 | Ver reporte. | OK | Se mostraron total 1, pendiente 0, en_proceso 1 y resuelta 0. |
| 6 | Cerrar y volver a ejecutar. | OK | La solicitud volvió a aparecer y las salidas coincidieron. |
| 7 | Cambiar estado de solicitud ID 999. | OK | Se mostró `Dato inválido` y el archivo conservó sus bytes. |
| 8 | Ingresar `²` como ID. | OK | Se mostró `Dato inválido` y el programa terminó sin error. |
| 9 | Cargar JSON mal escrito. | OK | Se mostró `Error en datos.json` sin abrir el menú. |
| 10 | Cargar JSON sin `estudiantes`. | OK | Se mostró `Datos inválidos` sin abrir el menú. |
| 11 | Ejecutar desde otra carpeta e importar `app`. | OK | Se pudo salir del programa y la importación mostró solo `IMPORT_OK`. |
| 12 | Revisar claves de solicitud y archivo temporal. | OK | Las siete claves conservaron su orden y no quedó `datos.tmp`. |

## Antes y después

Para las operaciones normales de los casos 1 a 6, el script comparó las salidas y los datos de la versión inicial y la actual. Los casos 7 a 12 comprobaron situaciones especiales de la versión mejorada.

## Conclusión

Aprobaron 12 de 12 comprobaciones. No se observaron regresiones en los casos normales comparados.

## Evidencia

La salida real está en `docs/evidencias/Etapa_6_Resultados.txt` y el script utilizado está en `tests/verificar_etapa6.py`.
