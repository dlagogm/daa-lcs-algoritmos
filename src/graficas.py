"""Gráficas a partir de resultados/medidas*.csv (requiere matplotlib)."""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados')
ESTILO = {'A_recursiva': ('A · recursiva', '#c0392b', 'o'),
          'B_hirschberg': ('B · Hirschberg', '#2471a3', 's'),
          'C_programacion_dinamica': ('C · PD tabular', '#1e8449', '^')}


def leer(nombre):
    datos = {}
    with open(os.path.join(RAIZ, nombre)) as fh:
        for f in csv.DictReader(fh):
            d = datos.setdefault(f['algoritmo'], {'n': [], 't': [], 'm': []})
            d['n'].append(int(f['n'])); d['t'].append(float(f['tiempo_s'])); d['m'].append(float(f['memoria_kib']))
    return datos


def dibujar(datos, clave, ylabel, fichero, titulo, logx=True):
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for alg, d in datos.items():
        etiqueta, color, marca = ESTILO[alg]
        ax.plot(d['n'], d[clave], marker=marca, color=color, label=etiqueta, linewidth=1.6)
    if logx:
        ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Longitud de cada cadena (n = m)')
    ax.set_ylabel(ylabel)
    ax.set_title(titulo, fontsize=10)
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(RAIZ, fichero), dpi=200)
    plt.close(fig)


def main():
    grandes, pequenas = leer('medidas.csv'), leer('medidas_pequenas.csv')
    dibujar(grandes, 't', 'Tiempo de CPU (s)', 'tiempo_grandes.png', 'Tiempo, cadenas de 100 a 4000 símbolos')
    dibujar(grandes, 'm', 'Memoria máxima (KiB)', 'memoria_grandes.png', 'Memoria, cadenas de 100 a 4000 símbolos')
    dibujar(pequenas, 't', 'Tiempo de CPU (s)', 'tiempo_pequenas.png', 'Tiempo, cadenas pequeñas (incluye la versión A)', logx=False)
    print('Gráficas guardadas en resultados/')


if __name__ == '__main__':
    main()
