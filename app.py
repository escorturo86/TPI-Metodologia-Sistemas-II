import json


def leer_datos():
    with open("datos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def registrar_solicitud(datos):
    for estudiante in datos["estudiantes"]:
        print(estudiante["id"], estudiante["nombre"])

    estudiante_ingresado = input("ID de estudiante: ").strip()
    if not estudiante_ingresado.isdigit():
        print("Dato inválido")
        return
    estudiante_id = int(estudiante_ingresado)
    if not any(estudiante["id"] == estudiante_id for estudiante in datos["estudiantes"]):
        print("Dato inválido")
        return

    print("1. certificado")
    print("2. equivalencia")
    print("3. consulta")
    tipos = {"1": "certificado", "2": "equivalencia", "3": "consulta"}
    tipo_ingresado = input("Tipo: ").strip()
    if tipo_ingresado not in tipos:
        print("Dato inválido")
        return

    print("1. baja")
    print("2. media")
    print("3. alta")
    prioridades = {"1": "baja", "2": "media", "3": "alta"}
    prioridad_ingresada = input("Prioridad: ").strip()
    if prioridad_ingresada not in prioridades:
        print("Dato inválido")
        return

    descripcion = input("Descripción: ").strip()
    if not descripcion:
        print("Dato inválido")
        return

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


def cambiar_estado(datos):
    id_ingresado = input("ID de solicitud: ").strip()
    if not id_ingresado.isdigit():
        print("Dato inválido")
        return
    solicitud = next((solicitud for solicitud in datos["solicitudes"]
                      if solicitud["id"] == int(id_ingresado)), None)
    if solicitud is None:
        print("Dato inválido")
        return

    print("1. pendiente")
    print("2. en_proceso")
    print("3. resuelta")
    estados = {"1": "pendiente", "2": "en_proceso", "3": "resuelta"}
    estado_ingresado = input("Estado: ").strip()
    if estado_ingresado not in estados:
        print("Dato inválido")
        return

    solicitud["estado"] = estados[estado_ingresado]
    guardar_datos(datos)
    print("Estado actualizado")


def asignar_responsable(datos):
    id_ingresado = input("ID de solicitud: ").strip()
    if not id_ingresado.isdigit():
        print("Dato inválido")
        return
    solicitud = next((solicitud for solicitud in datos["solicitudes"]
                      if solicitud["id"] == int(id_ingresado)), None)
    if solicitud is None:
        print("Dato inválido")
        return

    for responsable in datos["responsables"]:
        print(responsable["id"], responsable["nombre"])
    responsable_ingresado = input("ID de responsable: ").strip()
    if not responsable_ingresado.isdigit():
        print("Dato inválido")
        return
    responsable_id = int(responsable_ingresado)
    if not any(responsable["id"] == responsable_id for responsable in datos["responsables"]):
        print("Dato inválido")
        return

    solicitud["responsable_id"] = responsable_id
    guardar_datos(datos)
    print("Responsable asignado")


def listar_solicitudes(datos):
    print("1. Todas")
    print("2. pendiente")
    print("3. en_proceso")
    print("4. resuelta")
    filtros = {"1": None, "2": "pendiente", "3": "en_proceso", "4": "resuelta"}
    opcion = input("Opción: ").strip()
    if opcion not in filtros:
        print("Dato inválido")
        return

    solicitudes = [solicitud for solicitud in datos["solicitudes"]
                   if filtros[opcion] is None or solicitud["estado"] == filtros[opcion]]
    if not solicitudes:
        print("No hay solicitudes")
        return

    for solicitud in solicitudes:
        print(json.dumps(solicitud, ensure_ascii=False))


def ver_reporte(datos):
    solicitudes = datos["solicitudes"]
    print("Total:", len(solicitudes))
    print("pendiente:", sum(solicitud["estado"] == "pendiente" for solicitud in solicitudes))
    print("en_proceso:", sum(solicitud["estado"] == "en_proceso" for solicitud in solicitudes))
    print("resuelta:", sum(solicitud["estado"] == "resuelta" for solicitud in solicitudes))


def ejecutar():
    try:
        datos = leer_datos()
    except FileNotFoundError:
        print("Falta datos.json")
        return

    while True:
        print("GESTIÓN DE SOLICITUDES ACADÉMICAS")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Listar o filtrar solicitudes")
        print("5. Ver reporte")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar_solicitud(datos)
        elif opcion == "2":
            cambiar_estado(datos)
        elif opcion == "3":
            asignar_responsable(datos)
        elif opcion == "4":
            listar_solicitudes(datos)
        elif opcion == "5":
            ver_reporte(datos)
        elif opcion == "0":
            print("Fin del programa")
            break
        else:
            print("Dato inválido")


ejecutar()
