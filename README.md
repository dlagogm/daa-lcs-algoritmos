# LCS: recursiva, Hirschberg y programación dinámica

Actividad 1 de *Diseño Avanzado de Algoritmos* (UNIPRO). Contiene tres implementaciones de la subsecuencia común más larga (LCS) de dos cadenas y los experimentos que las comparan.

| Versión | Función | Tiempo | Memoria |
|---|---|---|---|
| A · recursiva directa (sin memorización) | `lcs_recursiva` | O(2^(n+m)) en el peor caso | O(n+m) (pila) |
| B · divide y vencerás de Hirschberg | `lcs_hirschberg` | O(n·m) | O(n+m) |
| C · programación dinámica tabular | `lcs_pd` | O(n·m) | O(n·m) |

No se usa ninguna librería externa de LCS: solo la biblioteca estándar de Python. `matplotlib` solo hace falta para las gráficas.

## Requisitos

- Python 3.10 o posterior
- `make`
- `matplotlib` (solo para `make graficas`): `pip install matplotlib`

## Ejecución (un solo comando)

```bash
make
```

`make` ejecuta las pruebas unitarias, los experimentos y las gráficas. Tarda unos 2 minutos.

| Comando | Qué hace |
|---|---|
| `make test` | 5 pruebas: casos borde, ejemplos conocidos, comparación con fuerza bruta en 150 parejas aleatorias y coincidencia de B y C en cadenas de hasta 1000 símbolos |
| `make experimentos` | Mide el tiempo de CPU y la memoria máxima y guarda `resultados/*.csv` |
| `make graficas` | Genera `resultados/*.png` |
| `make demo` | Ejecuta las tres versiones sobre `ABCBDAB` y `BDCABA` |

También se puede llamar directamente a `python3 src/lcs.py CADENA1 CADENA2`.

## Estructura

```
src/lcs.py            las tres versiones y la validación es_subsecuencia
src/experimentos.py   generación de datos (semilla 2026) y medidas
src/graficas.py       gráficas
tests/test_lcs.py     pruebas unitarias
resultados/           CSV, gráficas y cadenas usadas (datos/pareja_<n>.txt)
```

## Metodología de medida

- **Datos:** cadenas aleatorias sobre el alfabeto {A, C, G, T} con semilla fija, por lo que los resultados son reproducibles. Se usan 6 parejas grandes, de 100 a 4000 símbolos, para B y C, y 9 parejas pequeñas, de 4 a 20 símbolos, para las tres versiones.
- **Tiempo:** `time.process_time()`, que mide tiempo de CPU. Se toma la mediana de 3 ejecuciones; para A con n ≥ 12 se hace una sola ejecución.
- **Memoria:** pico de memoria reservada medido con `tracemalloc`, en una ejecución separada para no alterar el tiempo.
- **Validación:** cada resultado se comprueba como subsecuencia de ambas cadenas, y las longitudes de las tres versiones deben coincidir.
