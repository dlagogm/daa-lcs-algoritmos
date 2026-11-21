PY ?= python3

.PHONY: all test experimentos graficas demo limpiar

## make: pruebas + experimentos + gráficas (todo con un solo comando)
all: test experimentos graficas

test:
	$(PY) -m unittest discover -s tests -v

experimentos:
	$(PY) src/experimentos.py

graficas:
	$(PY) src/graficas.py

## make demo: ejecuta las tres versiones sobre un ejemplo corto
demo:
	$(PY) src/lcs.py ABCBDAB BDCABA

limpiar:
	rm -rf resultados/*.csv resultados/*.png resultados/datos
