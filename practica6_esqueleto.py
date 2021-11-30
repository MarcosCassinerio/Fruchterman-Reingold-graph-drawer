#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        c1: constante de repulsión
        c2: constante de atracción
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        # Completar
        self.posiciones = {}
        self.fuerzas = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        pass

def leer_grafo(nombre_archivo):
    lines = []
    with open(nombre_archivo) as f:
        lines = f.readlines()

    n = 0
    vertices = []
    aristas = []
    if (len(lines) > 0):
        n = lines[0].rstrip('\n')
        if n.isnumeric():
            n = int(n)
            if len(lines) < (n + 1):
                raise Exception('Cantidad invalida de vertices')
            for i in range(1, n + 1):
                line = lines[i].rstrip('\n')
                if line.count(' ') != 0:
                    raise Exception('Nombre de vertice invalido')
                vertices.append(line)
            for i in range(n + 1, len(lines)):
                line = lines[i].rstrip('\n')
                args = line.split(' ')
                if len(args) != 2 or vertices.count(args[0]) == 0 or vertices.count(args[1]) == 0:
                    raise Exception('Arista invalida')
                arista = (args[0], args[1])
                if aristas.count(arista) != 0:
                    raise Exception('Arista duplicada')
                if arista[0] == arista[1]:
                    raise Exception('Lazo no permitido')
                aristas.append(arista)
    else:
        print('p[pipi')

    return vertices, aristas

def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)

    leer_grafo(args.file_name)

    return

    # TODO: Borrar antes de la entrega
    grafo1 = ([1, 2, 3, 4, 5, 6, 7],
              [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo1,  # TODO: Cambiar para usar grafo leido de archivo
        iters=args.iters,
        refresh=1,
        c1=0.1,
        c2=5.0,
        verbose=args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
