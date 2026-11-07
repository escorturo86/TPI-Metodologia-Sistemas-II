import json
import os
from pathlib import Path


RUTA_DATOS = Path(__file__).resolve().parent / "datos.json"

TIPOS = {"1": "certificado", "2": "equivalencia", "3": "consulta"}
PRIORIDADES = {"1": "baja", "2": "media", "3": "alta"}
ESTADOS = {"1": "pendiente", "2": "en_proceso", "3": "resuelta"}
FILTROS = {"1": None, "2": "pendiente", "3": "en_proceso", "4": "resuelta"}


def leer_datos():
    with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    temporal = RUTA_DATOS.with_suffix(".tmp")
    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
    os.replace(temporal, RUTA_DATOS)


def estructura_valida(datos):
    if not isinstance(datos, dict):
        return False
    for clave in ("estudiantes", "responsables", "solicitudes"):
        if clave not in datos or not isinstance(datos[clave], list):
            return False
    for clave in ("estudiantes", "responsables"):
        for persona in datos[clave]:
            if not isinstance(persona, dict):
                return False
            if type(persona.get("id")) is not int or not isinstance(persona.get("nombre"), str):
                return False
    for solicitud in datos["solicitudes"]:
        if not isinstance(solicitud, dict):
            return False
        if type(solicitud.get("id")) is not int or type(solicitud.get("estudiante_id")) is not int:
            return False
        for clave in ("tipo", "prioridad", "descripcion", "estado"):
            if not isinstance(solicitud.get(clave), str):
                return False
        responsable_id = solicitud.get("responsable_id")
        if responsable_id is not None and type(responsable_id) is not int:
            return False
    return True


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


def mostrar_opciones(opciones):
    for clave, valor in opciones.items():
        etiqueta = "Todas" if valor is None else valor
        print(f"{clave}. {etiqueta}")


def pedir_datos_solicitud(datos):
    for estudiante in datos["estudiantes"]:
        print(estudiante["id"], estudiante["nombre"])

    estudiante_ingresado = input("ID de estudiante: ").strip()
    estudiante_id = convertir_id(estudiante_ingresado)
    if estudiante_id is None or not any(estudiante["id"] == estudiante_id for estudiante in datos["estudiantes"]):
        print("Dato inválido")
        return None

    mostrar_opciones(TIPOS)
    tipo_ingresado = input("Tipo: ").strip()
    if tipo_ingresado not in TIPOS:
        print("Dato inválido")
        return None

    mostrar_opciones(PRIORIDADES)
    prioridad_ingresada = input("Prioridad: ").strip()
    if prioridad_ingresada not in PRIORIDADES:
        print("Dato inválido")
        return None

    descripcion = input("Descripción: ").strip()
    if not descripcion:
        print("Dato inválido")
        return None

    detalles = {
        "estudiante_id": estudiante_id,
        "tipo": TIPOS[tipo_ingresado],
        "prioridad": PRIORIDADES[prioridad_ingresada],
        "descripcion": descripcion,
    }
    return detalles


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


def registrar_solicitud(datos):
    detalles = pedir_datos_solicitud(datos)
    if detalles is None:
        return
    solicitud = crear_solicitud(datos, detalles)
    datos["solicitudes"].append(solicitud)
    guardar_datos(datos)
    print(f"Solicitud registrada: ID {solicitud['id']}")


def cambiar_estado(datos):
    id_ingresado = input("ID de solicitud: ").strip()
    solicitud_id = convertir_id(id_ingresado)
    if solicitud_id is None:
        print("Dato inválido")
        return
    solicitud = buscar_solicitud(datos, solicitud_id)
    if solicitud is None:
        print("Dato inválido")
        return

    mostrar_opciones(ESTADOS)
    estado_ingresado = input("Estado: ").strip()
    if estado_ingresado not in ESTADOS:
        print("Dato inválido")
        return

    solicitud["estado"] = ESTADOS[estado_ingresado]
    guardar_datos(datos)
    print("Estado actualizado")


def asignar_responsable(datos):
    id_ingresado = input("ID de solicitud: ").strip()
    solicitud_id = convertir_id(id_ingresado)
    if solicitud_id is None:
        print("Dato inválido")
        return
    solicitud = buscar_solicitud(datos, solicitud_id)
    if solicitud is None:
        print("Dato inválido")
        return

    for responsable in datos["responsables"]:
        print(responsable["id"], responsable["nombre"])
    responsable_ingresado = input("ID de responsable: ").strip()
    responsable_id = convertir_id(responsable_ingresado)
    if responsable_id is None:
        print("Dato inválido")
        return
    if not any(responsable["id"] == responsable_id for responsable in datos["responsables"]):
        print("Dato inválido")
        return

    solicitud["responsable_id"] = responsable_id
    guardar_datos(datos)
    print("Responsable asignado")


def listar_solicitudes(datos):
    mostrar_opciones(FILTROS)
    opcion = input("Opción: ").strip()
    if opcion not in FILTROS:
        print("Dato inválido")
        return

    solicitudes = [solicitud for solicitud in datos["solicitudes"]
                   if FILTROS[opcion] is None or solicitud["estado"] == FILTROS[opcion]]
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
    except json.JSONDecodeError:
        print("Error en datos.json")
        return
    if not estructura_valida(datos):
        print("Datos inválidos")
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


if __name__ == "__main__":
    ejecutar()
