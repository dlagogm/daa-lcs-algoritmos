"""Pruebas unitarias: python3 -m unittest discover -s tests"""
import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from lcs import ALGORITMOS, es_subsecuencia, lcs_pd, lcs_hirschberg, lcs_recursiva  # noqa: E402


def lcs_fuerza_bruta(x, y):
    """Longitud de la LCS probando todas las subsecuencias de x (solo para cadenas muy cortas)."""
    for k in range(len(x), -1, -1):
        for idx in itertools.combinations(range(len(x)), k):
            if es_subsecuencia(''.join(x[i] for i in idx), y):
                return k
    return 0


class TestLCS(unittest.TestCase):
    def comprobar(self, x, y, longitud):
        for nombre, f in ALGORITMOS.items():
            r = f(x, y)
            self.assertEqual(len(r), longitud, f'{nombre} con {x!r}, {y!r}')
            self.assertTrue(es_subsecuencia(r, x) and es_subsecuencia(r, y), nombre)

    def test_casos_borde(self):
        self.comprobar('', '', 0)
        self.comprobar('ABC', '', 0)
        self.comprobar('', 'ABC', 0)
        self.comprobar('A', 'A', 1)
        self.comprobar('A', 'B', 0)
        self.comprobar('ABC', 'DEF', 0)
        self.comprobar('AAAA', 'AA', 2)

    def test_casos_conocidos(self):
        self.comprobar('ABCBDAB', 'BDCABA', 4)        # ejemplo clásico de Cormen et al.
        self.comprobar('AGGTAB', 'GXTXAYB', 4)        # GTAB
        self.comprobar('PROGRAMACION', 'PROGRAMACION', 12)

    def test_contra_fuerza_bruta(self):
        rnd = random.Random(1)
        for _ in range(150):
            x = ''.join(rnd.choice('ACGT') for _ in range(rnd.randint(0, 8)))
            y = ''.join(rnd.choice('ACGT') for _ in range(rnd.randint(0, 8)))
            self.comprobar(x, y, lcs_fuerza_bruta(x, y))

    def test_b_y_c_coinciden_en_cadenas_largas(self):
        rnd = random.Random(7)
        for n, m in [(300, 250), (500, 500), (1000, 700)]:
            x = ''.join(rnd.choice('ACGT') for _ in range(n))
            y = ''.join(rnd.choice('ACGT') for _ in range(m))
            b, c = lcs_hirschberg(x, y), lcs_pd(x, y)
            self.assertEqual(len(b), len(c))
            self.assertTrue(es_subsecuencia(b, x) and es_subsecuencia(b, y))

    def test_recursiva_igual_a_pd_en_cortas(self):
        rnd = random.Random(3)
        for _ in range(30):
            x = ''.join(rnd.choice('AB') for _ in range(rnd.randint(0, 9)))
            y = ''.join(rnd.choice('AB') for _ in range(rnd.randint(0, 9)))
            self.assertEqual(len(lcs_recursiva(x, y)), len(lcs_pd(x, y)))


if __name__ == '__main__':
    unittest.main()
