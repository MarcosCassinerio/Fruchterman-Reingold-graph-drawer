#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import random

import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np


class LayoutGraph:

    def __init__(self, grafo, iters, temperature, refresh, c1, c2, width, height, verbose=False):
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
        self.temperature = temperature
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        self.width = width
        self.height = height

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        self.randomize_positions()
        self.show_graph()
        pass

    def show_graph(self):
        for pos in self.posiciones.values():
            plt.scatter(pos[0], pos[1], color='blue')
        for arist in self.grafo[1]:
            plt.plot([self.posiciones[arist[0]][0], self.posiciones[arist[1]][0]],
                     [self.posiciones[arist[0]][1], self.posiciones[arist[1]][1]],
                     color='green')

        plt.show()


    def randomize_positions(self):
        for vertice in self.grafo[0]:
            self.posiciones[vertice] = (random.randint(0, self.width), random.randint(0, self.height))

    def initialize_forces(self):
        for vertice in self.grafo[0]:
            self.fuerzas[vertice] = (0, 0)


def leer_grafo(nombre_archivo):
    lines = []
    with open(nombre_archivo) as f:
        lines = f.readlines()

    n = 0
    vertices = []
    aristas = []
    if len(lines) > 0:
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
        raise Exception('Archivo vacio')

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
    # Refresh
    parser.add_argument(
        '--ref',
        type=int,
        help='Tasa de refresco',
        default=1
    )
    # Constante de repulsion
    parser.add_argument(
        '--cr',
        type=float,
        help='Constante de repulsion',
        default=0.1
    )
    # Constante de atraccion
    parser.add_argument(
        '--ca',
        type=float,
        help='Constante de atraccion',
        default=5.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    grafo = leer_grafo(args.file_name)

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,
        iters=args.iters,
        temperature=args.temp,
        refresh=args.ref,
        c1=args.cr,
        c2=args.ca,
        width=640,
        height=420,
        verbose=args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
