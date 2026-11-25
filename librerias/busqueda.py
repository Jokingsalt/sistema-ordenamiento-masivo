def secuencial(datos, objetivo):
    for i, v in enumerate(datos):
        if v == objetivo:
            return i
    return -1


def binaria(datos, objetivo, descendente=False):
    lo, hi, hallado = 0, len(datos) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = datos[mid]
        if v == objetivo:
            hallado, hi = mid, mid - 1
        elif (v < objetivo) != descendente:
            lo = mid + 1
        else:
            hi = mid - 1
    return hallado


class TablaHash:

    def __init__(self, datos, factor=1.5):
        self.m = max(11, int(len(datos) / factor) | 1)
        self.cubetas = [[] for _ in range(self.m)]
        for i, v in enumerate(datos):
            self.cubetas[v % self.m].append((v, i))

    def buscar(self, objetivo):
        for v, i in self.cubetas[objetivo % self.m]:
            if v == objetivo:
                return i
        return -1


def hash_busqueda(datos, objetivo):
    return TablaHash(datos).buscar(objetivo)
