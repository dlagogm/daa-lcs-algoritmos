"""Tres algoritmos para la subsecuencia común más larga (LCS) de dos cadenas.

- lcs_recursiva:  versión A, recursiva directa sin memorización.  Tiempo O(2^(n+m)), espacio O(n+m) (pila).
- lcs_hirschberg: versión B, divide y vencerás de Hirschberg.     Tiempo O(n·m), espacio O(n+m).
- lcs_pd:         versión C, programación dinámica tabular.       Tiempo O(n·m), espacio O(n·m).

Las tres devuelven una LCS (una cadena); su longitud es la misma en las tres.
No se usa ninguna librería externa de LCS.
"""
from array import array
import sys


# ---------------------------------------------------------------------------
# Versión A: recursiva directa
# ---------------------------------------------------------------------------
def lcs_recursiva(x: str, y: str) -> str:
    """Aplica directamente la recurrencia:
        LCS(i, j) = ""                                   si i = 0 o j = 0
                  = LCS(i-1, j-1) + x[i-1]               si x[i-1] = y[j-1]
                  = la más larga de LCS(i-1, j), LCS(i, j-1)  en otro caso
    Los mismos subproblemas se recalculan muchas veces: coste exponencial.
    """
    limite = len(x) + len(y) + 100
    if sys.getrecursionlimit() < limite:
        sys.setrecursionlimit(limite)

    def rec(i: int, j: int) -> str:
        if i == 0 or j == 0:
            return ""
        if x[i - 1] == y[j - 1]:
            return rec(i - 1, j - 1) + x[i - 1]
        a = rec(i - 1, j)
        b = rec(i, j - 1)
        return a if len(a) >= len(b) else b

    return rec(len(x), len(y))


# ---------------------------------------------------------------------------
# Versión C: programación dinámica tabular
# ---------------------------------------------------------------------------
def tabla_lcs(x: str, y: str) -> list:
    """Tabla (n+1) x (m+1) con L[i][j] = longitud de LCS(x[:i], y[:j]).
    Cada fila es un array('i') (4 bytes por celda) para que la memoria sea O(n·m) enteros."""
    n, m = len(x), len(y)
    L = [array('i', [0]) * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        xi = x[i - 1]
        fila, ant = L[i], L[i - 1]
        for j in range(1, m + 1):
            if xi == y[j - 1]:
                fila[j] = ant[j - 1] + 1
            else:
                a, b = ant[j], fila[j - 1]
                fila[j] = a if a >= b else b
    return L


def lcs_pd(x: str, y: str) -> str:
    """Rellena la tabla de abajo arriba y reconstruye la LCS recorriéndola desde L[n][m]."""
    L = tabla_lcs(x, y)
    i, j = len(x), len(y)
    res = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            res.append(x[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(res))


# ---------------------------------------------------------------------------
# Versión B: Hirschberg (divide y vencerás con espacio lineal)
# ---------------------------------------------------------------------------
def _ultima_fila(x: str, y: str) -> array:
    """Última fila de la tabla de PD para x e y guardando solo dos filas: O(len(y)) memoria."""
    m = len(y)
    ant = array('i', [0]) * (m + 1)
    act = array('i', [0]) * (m + 1)
    for xi in x:
        for j in range(1, m + 1):
            if xi == y[j - 1]:
                act[j] = ant[j - 1] + 1
            else:
                a, b = ant[j], act[j - 1]
                act[j] = a if a >= b else b
        ant, act = act, ant
    return ant


def lcs_hirschberg(x: str, y: str) -> str:
    """Divide x por la mitad. Con la última fila hacia delante de la primera mitad (L1) y la última
    fila hacia atrás de la segunda mitad (L2) se elige el corte k de y que maximiza L1[k] + L2[m-k];
    después se resuelven recursivamente las dos mitades y se concatenan las respuestas."""
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        return ""
    if n == 1:
        return x if x in y else ""
    mitad = n // 2
    l1 = _ultima_fila(x[:mitad], y)
    l2 = _ultima_fila(x[mitad:][::-1], y[::-1])
    mejor, k = -1, 0
    for j in range(m + 1):
        v = l1[j] + l2[m - j]
        if v > mejor:
            mejor, k = v, j
    return lcs_hirschberg(x[:mitad], y[:k]) + lcs_hirschberg(x[mitad:], y[k:])


ALGORITMOS = {
    'A_recursiva': lcs_recursiva,
    'B_hirschberg': lcs_hirschberg,
    'C_programacion_dinamica': lcs_pd,
}


def es_subsecuencia(s: str, t: str) -> bool:
    """True si s es subsecuencia de t (para validar resultados)."""
    it = iter(t)
    return all(c in it for c in s)


if __name__ == '__main__':
    a, b = (sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else ('ACCGGTCGAGTGCGCGGAAGCCGGCCGAA', 'GTCGTTCGGAATGCCGTTGCTCTGTAAA')
    for nombre, f in ALGORITMOS.items():
        if nombre == 'A_recursiva' and len(a) + len(b) > 30:
            print(f'{nombre:26s} (omitida: entrada demasiado larga para la versión exponencial)')
            continue
        r = f(a, b)
        print(f'{nombre:26s} longitud={len(r):3d}  {r}')
