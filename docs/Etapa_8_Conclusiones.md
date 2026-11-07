# Etapa 8: Conclusiones y aprendizaje

## 1. Conclusión general

En este trabajo mejoramos un sistema sencillo de solicitudes académicas que ya funcionaba. Primero guardamos la versión inicial y analizamos su calidad. Después encontramos nueve problemas en el código y realizamos mejoras para hacerlo más claro y fácil de mantener. El sistema conserva sus cinco operaciones: registrar solicitudes, cambiar estados, asignar responsables, listar o filtrar y mostrar un reporte.

## 2. Decisiones que tomamos

Mantuvimos Python y usamos funciones, listas y diccionarios, sin agregar clases ni herramientas complejas. Separamos las tareas del registro, evitamos repetir la búsqueda de solicitudes, mejoramos las validaciones y el manejo del archivo JSON. Aplicamos cuatro refactorings documentados y conservamos la versión inicial para comparar el antes y el después.

## 3. Pruebas y revisión

La Etapa 6 registró doce pruebas aprobadas. Las pruebas normales compararon la versión inicial con la mejorada y no mostraron cambios negativos en los casos revisados. En la Etapa 7, el checklist de code review cumplió sus doce puntos. Esto nos permitió respaldar las mejoras con evidencias y no solo con explicaciones.

## 4. Dificultades y límites

Uno de los desafíos técnicos fue mejorar el código sin cambiar lo que el programa hace para el usuario. También fue importante mantener las soluciones simples para poder entenderlas y explicarlas. El trabajo se limita a un sistema pequeño con datos guardados en un archivo JSON; no pretende cubrir todas las situaciones posibles.

## 5. Mejoras pendientes

Quedaron dos posibles mejoras para el futuro: comprobar con más detalle que los datos guardados sean coherentes entre sí y mostrar mensajes más claros si aparece un error al guardar por permisos u otros problemas. Estas mejoras quedaron registradas en el code review y **no se consideran resueltas**.

## 6. Relación con la materia

Este TPI me ayudó a relacionar calidad interna y externa, deuda técnica, code smells, Clean Code, SOLID, refactoring seguro, pruebas y code review. Comprendimos que un sistema no solo tiene que funcionar: también tiene que ser sencillo de revisar, corregir y mantener.

## 7. Reflexión individual

Mi principal aprendizaje fue entender que mejorar un programa no siempre significa agregar funciones nuevas. Muchas veces alcanza con organizar mejor el código y comprobar que siga funcionando igual. El diagnóstico y las pruebas me ayudaron a ver por qué conviene justificar cada cambio.


