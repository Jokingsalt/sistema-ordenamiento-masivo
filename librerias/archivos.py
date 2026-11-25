import os
import time


def leer(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".txt":
        datos, primera = [], True
        with open(ruta, "r", encoding="utf-8-sig") as f:
            for n, linea in enumerate(f, 1):
                toks = linea.replace(",", " ").split()
                if not toks:
                    continue
                try:
                    nums = [int(t) for t in toks]
                except ValueError:
                    if primera:
                        primera = False
                        continue
                    raise ValueError(f"Línea {n}: '{linea.strip()}' no es un entero válido")
                primera = False
                datos.extend(nums)
        return datos
    if ext == ".xlsx":
        from openpyxl import load_workbook
        wb = load_workbook(ruta, read_only=True, data_only=True)
        datos, primera = [], True
        for fila in wb.active.iter_rows(values_only=True):
            tiene_contenido = False
            for celda in fila:
                if celda is None or str(celda).strip() == "":
                    continue
                tiene_contenido = True
                if isinstance(celda, float) and celda.is_integer():
                    celda = int(celda)
                if isinstance(celda, str):
                    try:
                        celda = int(celda.strip())
                    except ValueError:
                        if primera:
                            continue
                        raise ValueError(f"Valor no entero en el Excel: {celda!r}")
                if not isinstance(celda, int) or isinstance(celda, bool):
                    raise ValueError(f"Valor no entero en el Excel: {celda!r}")
                datos.append(celda)
            if tiene_contenido:
                primera = False
        wb.close()
        return datos
    raise ValueError("Formato no permitido. Use .txt o .xlsx")


def escribir(ruta, datos, reporte=None):
    ext = os.path.splitext(ruta)[1].lower()
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    if ext == ".txt":
        with open(ruta, "w", encoding="utf-8") as f:
            f.writelines(f"{v}\n" for v in datos)
    elif ext == ".xlsx":
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos"
        ws.append(["valor"])
        for v in datos:
            ws.append([v])
        if reporte:
            wr = wb.create_sheet("Reporte")
            for fila in reporte:
                wr.append(list(fila))
            wr.column_dimensions["A"].width = 20
            wr.column_dimensions["B"].width = 40
        wb.save(ruta)
    else:
        raise ValueError("Formato no permitido. Use .txt o .xlsx")


def crear_temporal(base):
    ruta = os.path.join(base, f"_tmp_{time.time_ns()}")
    os.makedirs(ruta)
    return ruta


def borrar_temporal(ruta):
    try:
        for nombre in os.listdir(ruta):
            os.remove(os.path.join(ruta, nombre))
        os.rmdir(ruta)
    except OSError:
        pass


def copiar_archivo(origen, destino):
    with open(origen, "rb") as a, open(destino, "wb") as b:
        while True:
            bloque = a.read(65536)
            if not bloque:
                break
            b.write(bloque)
