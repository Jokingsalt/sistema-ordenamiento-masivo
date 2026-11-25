def _antes(descendente):
    if descendente:
        return lambda a, b: a > b
    return lambda a, b: a < b


def burbuja(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    n = len(a)
    for i in range(n - 1):
        intercambio = False
        for j in range(n - 1 - i):
            if antes(a[j + 1], a[j]):
                a[j], a[j + 1] = a[j + 1], a[j]
                intercambio = True
        if not intercambio:
            break
    return a


def seleccion(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if antes(a[j], a[m]):
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
    return a


def insercion(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    for i in range(1, len(a)):
        clave, j = a[i], i - 1
        while j >= 0 and antes(clave, a[j]):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = clave
    return a


def shell(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    n, h = len(a), 1
    while h < n // 3:
        h = 3 * h + 1
    while h >= 1:
        for i in range(h, n):
            clave, j = a[i], i
            while j >= h and antes(clave, a[j - h]):
                a[j] = a[j - h]
                j -= h
            a[j] = clave
        h //= 3
    return a


def quicksort(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    pila = [(0, len(a) - 1)]
    while pila:
        lo, hi = pila.pop()
        if lo >= hi:
            continue
        mid = (lo + hi) // 2
        if antes(a[mid], a[lo]): a[lo], a[mid] = a[mid], a[lo]
        if antes(a[hi], a[lo]): a[lo], a[hi] = a[hi], a[lo]
        if antes(a[mid], a[hi]): a[mid], a[hi] = a[hi], a[mid]
        pivote, i = a[hi], lo
        for j in range(lo, hi):
            if antes(a[j], pivote):
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        pila.append((lo, i - 1))
        pila.append((i + 1, hi))
    return a


def heapsort(datos, descendente=False):
    a, antes = list(datos), _antes(descendente)
    n = len(a)

    def hundir(i, tam):
        while True:
            hijo = 2 * i + 1
            if hijo >= tam:
                return
            if hijo + 1 < tam and antes(a[hijo], a[hijo + 1]):
                hijo += 1
            if antes(a[i], a[hijo]):
                a[i], a[hijo] = a[hijo], a[i]
                i = hijo
            else:
                return

    for i in range(n // 2 - 1, -1, -1):
        hundir(i, n)
    for fin in range(n - 1, 0, -1):
        a[0], a[fin] = a[fin], a[0]
        hundir(0, fin)
    return a


def radix(datos, descendente=False):
    a = list(datos)
    if len(a) <= 1:
        return a
    minimo = min(a)
    a = [v - minimo for v in a]
    exp, maximo = 1, max(a)
    while maximo // exp > 0:
        conteo = [0] * 10
        for v in a:
            conteo[(v // exp) % 10] += 1
        for d in range(1, 10):
            conteo[d] += conteo[d - 1]
        salida = [0] * len(a)
        for v in reversed(a):
            d = (v // exp) % 10
            conteo[d] -= 1
            salida[conteo[d]] = v
        a = salida
        exp *= 10
    a = [v + minimo for v in a]
    return a[::-1] if descendente else a


ALGORITMOS_INTERNOS = {
    "burbuja": burbuja,
    "seleccion": seleccion,
    "insercion": insercion,
    "shell": shell,
    "quicksort": quicksort,
    "heapsort": heapsort,
    "radix": radix,
}
