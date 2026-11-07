"""Pruebas del TPI: no modifica app.py ni datos.json originales."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PROYECTO = Path(__file__).resolve().parents[1]
RESULTADOS = []
LINEAS = []


def mostrar(mensaje):
    LINEAS.append(mensaje)
    print(mensaje)


def git_original(nombre):
    proceso = subprocess.run(
        ["git", "show", f"estado-inicial:{nombre}"],
        cwd=PROYECTO, capture_output=True, text=True, encoding="utf-8"
    )
    if proceso.returncode != 0:
        raise RuntimeError(f"No se pudo leer estado-inicial:{nombre}: {proceso.stderr}")
    return proceso.stdout


def ejecutar(carpeta, entradas, directorio=None):
    entorno = os.environ.copy()
    entorno["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(carpeta / "app.py")],
        input=entradas, capture_output=True, text=True, encoding="utf-8",
        cwd=directorio or carpeta, env=entorno, timeout=15
    )


def verificar(numero, descripcion, condicion):
    correcto = bool(condicion)
    RESULTADOS.append(correcto)
    mostrar(f"{numero:02d}. {'OK' if correcto else 'FALLÓ'} - {descripcion}")


def solicitud_guardada(carpeta):
    datos = json.loads((carpeta / "datos.json").read_text(encoding="utf-8"))
    return datos["solicitudes"][0]


def main():
    origen = git_original("app.py")
    datos_originales = git_original("datos.json")
    actual = (PROYECTO / "app.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="tpi_etapa6_") as temporal:
        raiz = Path(temporal)
        anterior = raiz / "antes"
        nuevo = raiz / "despues"
        for carpeta, codigo in ((anterior, origen), (nuevo, actual)):
            carpeta.mkdir()
            (carpeta / "app.py").write_text(codigo, encoding="utf-8")
            (carpeta / "datos.json").write_text(datos_originales, encoding="utf-8")

        pasos = "1\n1\n1\n3\nNecesito certificado de alumno regular\n3\n1\n1\n2\n1\n2\n4\n3\n5\n0\n"
        antes = ejecutar(anterior, pasos)
        despues = ejecutar(nuevo, pasos)
        guardado_antes = solicitud_guardada(anterior)
        guardado_despues = solicitud_guardada(nuevo)
        iguales = (antes.returncode == despues.returncode == 0 and
                   antes.stdout == despues.stdout and
                   guardado_antes == guardado_despues)

        verificar(1, "Registro de solicitud", iguales and
                 "Solicitud registrada: ID 1" in despues.stdout and
                 guardado_despues["id"] == 1 and guardado_despues["estudiante_id"] == 1 and
                 guardado_despues["tipo"] == "certificado" and guardado_despues["prioridad"] == "alta")
        verificar(2, "Asignación de responsable", iguales and
                 "Responsable asignado" in despues.stdout and guardado_despues["responsable_id"] == 1)
        verificar(3, "Cambio de estado", iguales and
                 "Estado actualizado" in despues.stdout and guardado_despues["estado"] == "en_proceso")
        verificar(4, "Filtro por estado", iguales and
                 json.dumps(guardado_despues, ensure_ascii=False) in despues.stdout)
        verificar(5, "Reporte", iguales and all(linea in despues.stdout for linea in
                 ("Total: 1", "pendiente: 0", "en_proceso: 1", "resuelta: 0")))

        reabrir_antes = ejecutar(anterior, "4\n3\n5\n0\n")
        reabrir_despues = ejecutar(nuevo, "4\n3\n5\n0\n")
        verificar(6, "Persistencia tras reiniciar", reabrir_antes.returncode == reabrir_despues.returncode == 0 and
                 reabrir_antes.stdout == reabrir_despues.stdout and
                 json.dumps(guardado_despues, ensure_ascii=False) in reabrir_despues.stdout)

        archivo = nuevo / "datos.json"
        contenido_anterior = archivo.read_bytes()
        invalido = ejecutar(nuevo, "2\n999\n0\n")
        verificar(7, "ID inexistente sin guardar", invalido.returncode == 0 and
                 "Dato inválido" in invalido.stdout and archivo.read_bytes() == contenido_anterior)
        id_especial = ejecutar(nuevo, "1\n²\n0\n")
        verificar(8, "ID no convertible", id_especial.returncode == 0 and
                 "Dato inválido" in id_especial.stdout and archivo.read_bytes() == contenido_anterior)

        archivo.write_text("{", encoding="utf-8")
        danado = ejecutar(nuevo, "")
        verificar(9, "JSON mal formado", danado.returncode == 0 and
                 "Error en datos.json" in danado.stdout and "GESTIÓN DE" not in danado.stdout)

        estructura = json.loads(datos_originales)
        del estructura["estudiantes"]
        archivo.write_text(json.dumps(estructura, ensure_ascii=False), encoding="utf-8")
        sin_estudiantes = ejecutar(nuevo, "")
        verificar(10, "JSON incompleto", sin_estudiantes.returncode == 0 and
                  "Datos inválidos" in sin_estudiantes.stdout and "GESTIÓN DE" not in sin_estudiantes.stdout)

        archivo.write_text(datos_originales, encoding="utf-8")
        otra_carpeta = raiz / "otra_carpeta"
        otra_carpeta.mkdir()
        desde_otra = ejecutar(nuevo, "0\n", directorio=otra_carpeta)
        importacion = subprocess.run(
            [sys.executable, "-c", f"import sys; sys.path.insert(0, {str(nuevo)!r}); import app; print('IMPORT_OK')"],
            cwd=otra_carpeta, capture_output=True, text=True, encoding="utf-8", timeout=15
        )
        verificar(11, "Ruta e importación sin menú", desde_otra.returncode == 0 and
                  "Fin del programa" in desde_otra.stdout and
                  importacion.returncode == 0 and importacion.stdout.strip() == "IMPORT_OK")

        claves = ["id", "estudiante_id", "tipo", "prioridad", "descripcion", "estado", "responsable_id"]
        verificar(12, "Campos correctos y sin archivo temporal", list(guardado_despues) == claves and
                  not (nuevo / "datos.tmp").exists() and iguales)

    aprobadas = sum(RESULTADOS)
    mostrar(f"RESULTADO: {aprobadas}/{len(RESULTADOS)} comprobaciones aprobadas")
    if aprobadas != len(RESULTADOS):
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError, RuntimeError, subprocess.TimeoutExpired) as error:
        mostrar(f"ERROR AL EJECUTAR LAS PRUEBAS: {error}")
        sys.exit(2)
    finally:
        evidencia = PROYECTO / "docs" / "evidencias" / "Etapa_6_Resultados.txt"
        evidencia.parent.mkdir(parents=True, exist_ok=True)
        evidencia.write_text("\n".join(LINEAS) + "\n", encoding="utf-8")


