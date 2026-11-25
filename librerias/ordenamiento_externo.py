import os

from .archivos import borrar_temporal, copiar_archivo, crear_temporal
from .ordenamiento_interno import quicksort


def _siguiente_entero(f):
    for linea in f:
        linea = linea.strip()
        if linea:
            return int(linea)
    return None


def _leer_enteros(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        while True:
            v = _siguiente_entero(f)
            if v is None:
                return
            yield v


def _comparador(descendente):
    return (lambda a, b: a > b) if descendente else (lambda a, b: a < b)


def _contar(ruta):
    n = 0
    for _ in _leer_enteros(ruta):
        n += 1
    return n


class _Corrida:
    def __init__(self, f, limite=None):
        self.f = f
        self.restante = limite

    def siguiente(self):
        if self.restante is not None:
            if self.restante <= 0:
                return None
            self.restante -= 1
        v = _siguiente_entero(self.f)
        if v is None:
            self.restante = 0
        return v


def _mezcla_k(corridas, antes, out):
    cabezas = [c.siguiente() for c in corridas]
    escritos = 0
    while True:
        m = -1
        for j in range(len(cabezas)):
            if cabezas[j] is not None and (m == -1 or antes(cabezas[j], cabezas[m])):
                m = j
        if m == -1:
            return escritos
        out.write(f"{cabezas[m]}\n")
        escritos += 1
        cabezas[m] = corridas[m].siguiente()


def mezcla_directa(entrada, salida, descendente=False):
    antes = _comparador(descendente)
    tmp = crear_temporal(os.path.dirname(os.path.abspath(salida)))
    A, B, C = (os.path.join(tmp, n) for n in ("A.txt", "B.txt", "C.txt"))
    try:
        copiar_archivo(entrada, A)
        n, L, pasadas = _contar(A), 1, 0
        while L < n:
            with open(B, "w") as fb, open(C, "w") as fc:
                destinos = (fb, fc)
                i = 0
                for v in _leer_enteros(A):
                    destinos[(i // L) % 2].write(f"{v}\n")
                    i += 1
            with open(B, "r", encoding="utf-8") as fb, \
                    open(C, "r", encoding="utf-8") as fc, \
                    open(A, "w") as fa:
                while True:
                    escritos = _mezcla_k([_Corrida(fb, L), _Corrida(fc, L)], antes, fa)
                    if escritos == 0:
                        break
            L *= 2
            pasadas += 1
        copiar_archivo(A, salida)
        return pasadas
    finally:
        borrar_temporal(tmp)


def mezcla_equilibrada(entrada, salida, descendente=False, vias=3):
    antes = _comparador(descendente)
    tmp = crear_temporal(os.path.dirname(os.path.abspath(salida)))
    ent = [os.path.join(tmp, f"E{j}.txt") for j in range(vias)]
    sal = [os.path.join(tmp, f"S{j}.txt") for j in range(vias)]
    try:
        n = 0
        fs = [open(r, "w") for r in ent]
        try:
            for v in _leer_enteros(entrada):
                fs[n % vias].write(f"{v}\n")
                n += 1
        finally:
            for f in fs:
                f.close()
        L, pasadas = 1, 0
        while L < n:
            lectores = [open(r, "r", encoding="utf-8") for r in ent]
            escritores = [open(r, "w") for r in sal]
            try:
                destino = 0
                while True:
                    escritos = _mezcla_k([_Corrida(f, L) for f in lectores], antes,
                                         escritores[destino % vias])
                    if escritos == 0:
                        break
                    destino += 1
            finally:
                for f in lectores + escritores:
                    f.close()
            ent, sal = sal, ent
            L *= vias
            pasadas += 1
        copiar_archivo(ent[0], salida)
        return pasadas
    finally:
        borrar_temporal(tmp)


def intercalacion(entrada, salida, descendente=False, tam_bloque=500):
    antes = _comparador(descendente)
    tmp = crear_temporal(os.path.dirname(os.path.abspath(salida)))
    runs = []
    try:
        bloque = []

        def volcar():
            if not bloque:
                return
            ruta = os.path.join(tmp, f"run_{len(runs)}.txt")
            with open(ruta, "w") as f:
                for v in quicksort(bloque, descendente):
                    f.write(f"{v}\n")
            runs.append(ruta)
            del bloque[:]

        for v in _leer_enteros(entrada):
            bloque.append(v)
            if len(bloque) >= tam_bloque:
                volcar()
        volcar()

        archivos_runs = [open(r, "r", encoding="utf-8") for r in runs]
        try:
            with open(salida, "w") as out:
                _mezcla_k([_Corrida(f) for f in archivos_runs], antes, out)
        finally:
            for f in archivos_runs:
                f.close()
        return len(runs)
    finally:
        borrar_temporal(tmp)


ALGORITMOS_EXTERNOS = {
    "mezcla_directa": mezcla_directa,
    "mezcla_equilibrada": mezcla_equilibrada,
    "intercalacion": intercalacion,
}
