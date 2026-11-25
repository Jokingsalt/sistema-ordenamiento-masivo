import os
import time

from interfaz import Interfaz
from librerias import archivos, busqueda
from librerias.ordenamiento_interno import ALGORITMOS_INTERNOS, insercion
from librerias.ordenamiento_externo import ALGORITMOS_EXTERNOS

NOMBRES = {
    "burbuja": "Burbuja", "seleccion": "Selección", "insercion": "Inserción",
    "shell": "Shell", "quicksort": "Quicksort", "heapsort": "Heapsort", "radix": "Radix",
    "mezcla_directa": "Mezcla directa",
    "mezcla_equilibrada": "Mezcla equilibrada",
    "intercalacion": "Intercalación",
}

ALGORITMOS = [(k, f"{NOMBRES[k]}  [interno]") for k in ALGORITMOS_INTERNOS] + \
             [(k, f"{NOMBRES[k]}  [externo]") for k in ALGORITMOS_EXTERNOS]

RECOMENDACIONES = [
    ("Datos pequeños", "Inserción", "Simple y sin sobrecarga; muy rápida con pocos elementos."),
    ("Datos masivos", "Quicksort (o Radix / Heapsort)", "O(n log n) u O(n·d) con Radix; mucho más rápidos que burbuja o selección."),
    ("Archivos externos", "Mezcla equilibrada / Intercalación", "Ordenan en disco con memoria acotada y pocas pasadas (log base K de n)."),
    ("Datos parcialmente ordenados", "Inserción", "Aprovecha el orden existente: casi O(n) (burbuja con corte anticipado también)."),
    ("Búsquedas frecuentes", "Ordenar una vez + Búsqueda binaria, o Hash", "O(log n) y O(1) promedio frente a O(n) de la secuencial."),
]


def esta_ordenado(lista, descendente=False):
    for i in range(1, len(lista)):
        if (lista[i] > lista[i - 1]) if descendente else (lista[i] < lista[i - 1]):
            return False
    return True


class Controlador:
    def __init__(self):
        self.datos, self.original, self.ruta = [], [], None
        self.ordenado = self.descendente = False
        self.algoritmo = self.tiempo = None
        self.tabla_hash = None
        self.ui = Interfaz(self, ALGORITMOS, RECOMENDACIONES, "quicksort")
        self._refrescar()

    def iniciar(self):
        self.ui.mainloop()

    def _refrescar(self):
        n = len(self.datos)
        primeros = [(i + 1, self.datos[i]) for i in range(min(20, n))]
        ultimos = [(i + 1, self.datos[i]) for i in range(max(0, n - 20), n)]
        lineas = [f"Total de registros: {n}"]
        if self.ruta:
            lineas.insert(0, f"Archivo: {os.path.basename(self.ruta)}")
        if self.ordenado:
            lineas.append(f"Ordenado con: {NOMBRES[self.algoritmo]} "
                          f"({'descendente' if self.descendente else 'ascendente'})   |   "
                          f"Tiempo: {self.tiempo:.6f} s")
        else:
            lineas.append("Estado: sin ordenar" if n else "Estado: cargue un archivo para comenzar")
        self.ui.refrescar(n > 0, self.ordenado, primeros, ultimos, "\n".join(lineas))

    def _ejecutar(self, clave, datos, descendente):
        t0 = time.perf_counter()
        if clave in ALGORITMOS_INTERNOS:
            resultado = ALGORITMOS_INTERNOS[clave](datos, descendente)
        else:
            tmp = archivos.crear_temporal(os.getcwd())
            try:
                entrada, salida = os.path.join(tmp, "in.txt"), os.path.join(tmp, "out.txt")
                archivos.escribir(entrada, datos)
                ALGORITMOS_EXTERNOS[clave](entrada, salida, descendente)
                resultado = archivos.leer(salida)
            finally:
                archivos.borrar_temporal(tmp)
        return resultado, time.perf_counter() - t0

    def cargar(self):
        ruta = self.ui.pedir_archivo()
        if not ruta:
            return
        try:
            datos = archivos.leer(ruta)
        except ImportError:
            self.ui.error("Falta openpyxl", "Para leer XLSX instale openpyxl:\n\npip install openpyxl")
            return
        except (OSError, ValueError) as ex:
            self.ui.error("No se pudo cargar el archivo", str(ex))
            return
        if not datos:
            self.ui.aviso("Archivo vacío", "El archivo no contiene números enteros.")
            return
        self.datos, self.original, self.ruta = datos, list(datos), ruta
        self.ordenado, self.algoritmo, self.tiempo, self.tabla_hash = False, None, None, None
        self.ui.mostrar_archivo(os.path.basename(ruta) + f"\n({len(datos)} registros)")
        self.ui.mostrar_busqueda("")
        self.ui.mostrar_tiempo_orden("")
        self._refrescar()
        self.ui.estado(f"Archivo cargado: {len(datos)} registros.")

    def ordenar(self, clave, descendente):
        if not self.datos:
            return
        self.ui.estado(f"Ordenando con {NOMBRES[clave]}…")
        self.ui.ocupado(True)
        self.ui.actualizar()
        try:
            resultado, tiempo = self._ejecutar(clave, list(self.datos), descendente)
        except Exception as ex:
            self.ui.ocupado(False)
            self._refrescar()
            self.ui.error("Error", f"{type(ex).__name__}: {ex}")
            self.ui.estado("Ocurrió un error.")
            return
        self.datos, self.tiempo = resultado, tiempo
        self.ordenado, self.descendente, self.algoritmo = True, descendente, clave
        self.tabla_hash = None
        self.ui.ocupado(False)
        self._refrescar()
        self.ui.mostrar_tiempo_orden(f"⏱ {NOMBRES[clave]}: {tiempo:.6f} s")
        self.ui.estado(f"Ordenado con {NOMBRES[clave]} en {tiempo:.6f} s")

    def buscar(self, texto, metodo):
        if not self.datos:
            return
        try:
            objetivo = int(texto.strip())
        except ValueError:
            self.ui.aviso("Valor inválido", "Escriba un número entero (ej. 42 o -15).")
            return
        if metodo == 1 and not self.ordenado:
            self.ui.info("Datos sin ordenar",
                         "La búsqueda binaria requiere datos ordenados.\n"
                         "Primero use el paso 2 (Ordenar datos).")
            return
        t0 = time.perf_counter()
        if metodo == 0:
            pos = busqueda.secuencial(self.datos, objetivo)
        elif metodo == 1:
            pos = busqueda.binaria(self.datos, objetivo, self.descendente)
        else:
            if self.tabla_hash is None:
                self.tabla_hash = busqueda.TablaHash(self.datos)
            pos = self.tabla_hash.buscar(objetivo)
        t = time.perf_counter() - t0
        nombre = ("secuencial", "binaria", "hash")[metodo]
        if pos >= 0:
            self.ui.mostrar_busqueda(f"✔ {objetivo} encontrado en la posición {pos + 1}\n"
                                     f"({nombre}, {t:.8f} s)", True)
            self.ui.resaltar(pos + 1)
        else:
            self.ui.mostrar_busqueda(f"✘ {objetivo} no existe en los datos\n({nombre}, {t:.8f} s)", False)
        self.ui.estado(f"Búsqueda {nombre} terminada en {t:.8f} s")

    def exportar(self, fmt):
        if not self.ordenado:
            self.ui.info("Nada que exportar", "Primero ordene los datos.")
            return
        ext = "." + fmt
        ruta = self.ui.pedir_guardar(fmt)
        if not ruta:
            return
        if not ruta.lower().endswith(ext):
            ruta = os.path.splitext(ruta)[0] + ext
        info = [("Archivo origen", self.ruta), ("Algoritmo", NOMBRES[self.algoritmo]),
                ("Orden", "descendente" if self.descendente else "ascendente"),
                ("Total registros", len(self.datos)), ("Tiempo (s)", round(self.tiempo, 6))]
        try:
            archivos.escribir(ruta, self.datos, reporte=info)
            base = os.path.splitext(ruta)[0]
            reporte = (base[:-9] if base.endswith("_ordenado") else base) + "_reporte.txt"
            with open(reporte, "w", encoding="utf-8") as f:
                for etiqueta, valor in info:
                    f.write(f"{etiqueta:<16}: {valor}\n")
        except (OSError, ValueError, ImportError) as ex:
            self.ui.error("Error al exportar", str(ex))
            return
        self.ui.info("Exportación completa",
                     f"Archivo ordenado ({fmt.upper()}):\n{ruta}\n\nReporte (algoritmo y tiempo):\n{reporte}"
                     + ("\n(también en la hoja «Reporte» del Excel)" if fmt == "xlsx" else ""))
        self.ui.estado("Resultados exportados.")

    def comparar(self):
        if not self.original:
            self.ui.aviso("Sin datos", "Primero cargue un archivo (paso 1).")
            return
        self.ui.ocupado(True)
        medidas = []
        try:
            for clave, _ in ALGORITMOS:
                self.ui.estado(f"Comparando… {NOMBRES[clave]}")
                self.ui.actualizar()
                resultado, t = self._ejecutar(clave, list(self.original), False)
                correcto = len(resultado) == len(self.original) and esta_ordenado(resultado)
                medidas.append((t, clave, correcto))
        except Exception as ex:
            self.ui.ocupado(False)
            self.ui.error("Error al comparar", f"{type(ex).__name__}: {ex}")
            self.ui.estado("Ocurrió un error.")
            return
        medidas = insercion(medidas)
        filas = []
        for i, (t, clave, correcto) in enumerate(medidas):
            tipo = "interno" if clave in ALGORITMOS_INTERNOS else "externo"
            filas.append((i + 1, NOMBRES[clave], tipo, f"{t:.6f}",
                          "✔ correcto" if correcto else "✘ incorrecto"))
        rapido, lento = medidas[0], medidas[-1]
        nota = (f"{len(self.original)} registros (ascendente).  Más rápido: {NOMBRES[rapido[1]]} "
                f"({rapido[0]:.6f} s).  Más lento: {NOMBRES[lento[1]]} ({lento[0]:.6f} s).  "
                f"Los externos incluyen el tiempo de escribir y leer archivos temporales.")
        self.ui.ocupado(False)
        self.ui.mostrar_comparacion(filas, nota)
        self.ui.estado("Comparación terminada.")


if __name__ == "__main__":
    Controlador().iniciar()
