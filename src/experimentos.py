"""Experimentos: tiempo de CPU y memoria máxima de las tres versiones de LCS.

Genera las parejas de cadenas (semilla fija, reproducible), mide cada algoritmo y guarda:
  resultados/datos/pareja_<n>.txt   cadenas usadas
  resultados/medidas.csv            medidas de las parejas grandes (B y C)
  resultados/medidas_pequenas.csv   medidas de las parejas pequeñas (A, B y C)

Tiempo: time.process_time() (CPU del proceso), mediana de REPETICIONES ejecuciones.
Memoria: pico de memoria reservada por el algoritmo, medido con tracemalloc en una ejecución aparte
(para que tracemalloc no altere el tiempo).
"""
import csv
import os
import random
import statistics
import sys
import time
import tracemalloc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lcs import ALGORITMOS, es_subsecuencia, lcs_pd  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados')
ALFABETO = 'ACGT'
SEMILLA = 2026
TAMANOS_GRANDES = [100, 250, 500, 1000, 2000, 4000]
TAMANOS_PEQUENOS = [4, 6, 8, 10, 12, 14, 16, 18, 20]
LIMITE_RECURSIVA_S = 60.0
REPETICIONES = 3


def generar(n: int, rnd: random.Random) -> tuple:
    return (''.join(rnd.choice(ALFABETO) for _ in range(n)),
            ''.join(rnd.choice(ALFABETO) for _ in range(n)))


def medir(f, x, y, repeticiones=REPETICIONES):
    tiempos, res = [], None
    for _ in range(repeticiones):
        t0 = time.process_time()
        res = f(x, y)
        tiempos.append(time.process_time() - t0)
    tracemalloc.start()
    f(x, y)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return statistics.median(tiempos), pico, res


def main():
    os.makedirs(os.path.join(RAIZ, 'datos'), exist_ok=True)
    rnd = random.Random(SEMILLA)

    # ---- Parejas pequeñas: las tres versiones ----
    filas = []
    recursiva_activa = True
    for n in TAMANOS_PEQUENOS:
        x, y = generar(n, rnd)
        esperado = len(lcs_pd(x, y))
        for nombre, f in ALGORITMOS.items():
            if nombre == 'A_recursiva' and not recursiva_activa:
                continue
            rep = 1 if nombre == 'A_recursiva' and n >= 12 else REPETICIONES
            t, mem, r = medir(f, x, y, rep)
            assert len(r) == esperado and es_subsecuencia(r, x) and es_subsecuencia(r, y), (nombre, n)
            filas.append({'algoritmo': nombre, 'n': n, 'lcs': len(r), 'tiempo_s': f'{t:.6f}', 'memoria_kib': f'{mem / 1024:.1f}'})
            print(f'[pequeñas] n={n:5d} {nombre:24s} lcs={len(r):4d} t={t:10.4f}s mem={mem / 1024:9.1f} KiB', flush=True)
            if nombre == 'A_recursiva' and t > LIMITE_RECURSIVA_S / 4:
                recursiva_activa = False  # la siguiente tardaría más que el límite
    with open(os.path.join(RAIZ, 'medidas_pequenas.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)

    # ---- Parejas grandes: B y C (A es inviable) ----
    filas = []
    for n in TAMANOS_GRANDES:
        x, y = generar(n, rnd)
        with open(os.path.join(RAIZ, 'datos', f'pareja_{n}.txt'), 'w') as fh:
            fh.write(x + '\n' + y + '\n')
        longitudes = set()
        for nombre in ('B_hirschberg', 'C_programacion_dinamica'):
            t, mem, r = medir(ALGORITMOS[nombre], x, y)
            assert es_subsecuencia(r, x) and es_subsecuencia(r, y)
            longitudes.add(len(r))
            filas.append({'algoritmo': nombre, 'n': n, 'lcs': len(r), 'tiempo_s': f'{t:.6f}', 'memoria_kib': f'{mem / 1024:.1f}'})
            print(f'[grandes]  n={n:5d} {nombre:24s} lcs={len(r):4d} t={t:10.4f}s mem={mem / 1024:9.1f} KiB', flush=True)
        assert len(longitudes) == 1, 'B y C deben dar la misma longitud'
    with open(os.path.join(RAIZ, 'medidas.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    print('Medidas guardadas en resultados/')


if __name__ == '__main__':
    main()
