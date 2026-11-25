# Sistema de Procesamiento y Ordenamiento Masivo de Datos

Aplicación con interfaz gráfica (Tkinter) en **Python 3.8+** que carga archivos de enteros (TXT / XLSX),
los ordena con librerías propias (internas y externas), busca valores, compara algoritmos y exporta resultados.

## Cumplimiento de las restricciones del examen

- No se usa `.sort()`, `sorted()` ni bibliotecas de ordenamiento: todos los algoritmos están implementados en `librerias/`.
- Módulos usados: `os`, `time`, `openpyxl` (lectura/escritura de XLSX) y `tkinter` (solo para la interfaz gráfica).
- Las librerías propias se importan y se reutilizan desde `main.py`.

## Estructura

```
proyecto/
├── main.py                       # ARCHIVO PRINCIPAL: lógica del programa (se ejecuta este)
├── interfaz.py                   # Solo la interfaz gráfica (ventanas, botones, tablas)
├── requirements.txt              # openpyxl
├── librerias/
│   ├── ordenamiento_interno.py   # burbuja, selección, inserción, shell, quicksort, heapsort, radix
│   ├── ordenamiento_externo.py   # mezcla directa, mezcla equilibrada, intercalación
│   ├── busqueda.py               # secuencial, binaria, hash (tabla propia)
│   └── archivos.py               # lectura/escritura TXT y XLSX, archivos temporales
├── datos/                        # archivos de 1000 y 5000 enteros (TXT y XLSX)
└── salida/                       # resultados exportados
```

`interfaz.py` no contiene lógica de ordenamiento: solo dibuja la ventana y avisa a `main.py` cuando el usuario
pulsa un botón. `main.py` carga los datos, llama a las librerías, mide tiempos y le devuelve los resultados a la interfaz.

## Instrucciones de ejecución

```bash
git clone <URL-DEL-REPOSITORIO>
cd proyecto
py -m pip install -r requirements.txt      # solo necesario para archivos .xlsx
py main.py                                 # inicia el programa
```

En Linux/macOS use `python3` en lugar de `py`. Tkinter viene con Python en Windows y macOS; en Linux
instálelo con `sudo apt install python3-tk`.

## Uso de la interfaz

1. **Cargar archivo**: abre el explorador para elegir un `.txt` (un número por línea) o `.xlsx`
   (valores en celdas; si la primera fila tiene un título, se ignora).
2. **Ordenar datos**: elija el algoritmo (interno o externo), el orden ascendente/descendente y pulse *Ordenar*.
   Debajo del botón se muestra el **tiempo de ejecución** del ordenamiento.
3. **Buscar un valor**: secuencial, binaria (exige datos ordenados; el programa avisa) o hash. Muestra la posición
   (empezando en 1) y el tiempo de la búsqueda.
4. **Exportar resultados**: elija **TXT o XLSX** y guarde el archivo ordenado. Se crea además un reporte con el
   algoritmo utilizado, el orden, el total de registros y el tiempo de ejecución (en XLSX también en la hoja «Reporte»).

A la derecha se muestran el total de registros, el estado, el tiempo de ejecución y los **primeros 20** y **últimos 20**
elementos.

La pestaña **Comparación de algoritmos** tiene la tabla de recomendaciones por escenario y el botón
**Comparar algoritmos**, que ordena una copia de los datos cargados con los 10 algoritmos, mide el tiempo de cada uno,
verifica que el resultado quede ordenado y los muestra de más rápido a más lento.

## Algoritmos

| Tipo | Algoritmo | Complejidad |
|---|---|---|
| Interno | Burbuja (con corte anticipado) | O(n) mejor / O(n²) |
| Interno | Selección | O(n²) |
| Interno | Inserción | O(n) mejor / O(n²) |
| Interno | Shell (secuencia de Knuth) | ~O(n^1.3) |
| Interno | Quicksort (mediana de tres, iterativo) | O(n log n) prom. |
| Interno | Heapsort | O(n log n) |
| Interno | Radix (LSD, base 10, soporta negativos) | O(d·(n+10)) |
| Externo | Mezcla directa (2 vías, 3 archivos, bloques de 1, 2, 4, 8…) | O(n log₂ n) |
| Externo | Mezcla equilibrada (3 vías, 6 archivos) | O(n log₃ n) |
| Externo | Intercalación por bloques (runs ordenados + mezcla de K vías) | O(n log n), memoria O(bloque) |
| Búsqueda | Secuencial / Binaria / Hash (encadenamiento) | O(n) / O(log n) / O(1) prom. |

Los algoritmos externos trabajan con archivos temporales en disco (creados con `os` y borrados al terminar).
Las posiciones se muestran desde 1 (el primer elemento es la posición 1).

## Comparación básica

| Escenario | Algoritmo recomendado | Justificación |
|---|---|---|
| Datos pequeños (< ~100) | **Inserción** | Simple, sin sobrecarga, muy rápida con pocos elementos. |
| Datos masivos | **Quicksort** (o **Radix** para enteros / Heapsort si se exige peor caso garantizado) | O(n log n) u O(n·d); con 5000 datos es ~100× más rápido que burbuja/selección. |
| Archivos externos (no caben en RAM) | **Mezcla equilibrada** / **Intercalación** | Ordenan en disco con memoria acotada y pocas pasadas. |
| Datos parcialmente ordenados | **Inserción** | Aprovecha el orden existente: casi O(n). |
| Búsquedas frecuentes | **Ordenar una vez + búsqueda binaria**, o **Hash** | O(log n) y O(1) promedio frente a O(n) de la secuencial. |

### Resultados de ejemplo (5000 enteros, segundos)

| Algoritmo | Aleatorio | Casi ordenado | Inverso |
|---|---|---|---|
| burbuja | 1.1454 | 0.0006 | 1.3092 |
| seleccion | 0.5115 | 0.4238 | 0.4347 |
| insercion | 0.3469 | 0.0003 | 0.6746 |
| shell | 0.0073 | 0.0020 | 0.0032 |
| quicksort | 0.0042 | 0.0034 | 0.0055 |
| heapsort | 0.0070 | 0.0074 | 0.0065 |
| radix | 0.0031 | 0.0027 | 0.0028 |
| mezcla_directa | 0.0885 | 0.0881 | 0.1117 |
| mezcla_equilibrada | 0.0518 | 0.0365 | 0.0438 |
| intercalacion | 0.0128 | 0.0113 | 0.0123 |

*(Los tiempos varían según el equipo; use el botón «Comparar algoritmos» para obtener los suyos.)*

## Autor
Nombre del alumno — Matrícula — Materia — Fecha
