#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import math
import random

import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
import time


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
        self.temperatureConstant = 0.95

        self.kAttraction = c2 * math.sqrt(self.width * self.height / len(self.grafo[0]))
        self.kRepulsion = c1 * math.sqrt(self.width * self.height / len(self.grafo[0]))

        self.error = 0.05

        plt.rcParams["figure.figsize"] = (self.width / 100 + 1, self.height / 100 + 1)

    def layout(self):
        self.randomize_positions()
        for i in range(self.iters):
            self.fruchterman_reingold_step()
            if i % self.refresh == 0:
                self.show_graph()
        time.sleep(5)
        pass

    def show_graph(self):
        plt.clf()
        plt.xlim([0, self.width])
        plt.ylim([0, self.height])
        for pos in self.posiciones.values():
            plt.scatter(pos[0], pos[1], color='blue')
        for arist in self.grafo[1]:
            plt.plot([self.posiciones[arist[0]][0], self.posiciones[arist[1]][0]],
                     [self.posiciones[arist[0]][1], self.posiciones[arist[1]][1]],
                     color='green')
        plt.pause(0.1)

    def randomize_positions(self):
        for vertice in self.grafo[0]:
            self.posiciones[vertice] = (random.randint(0, self.width), random.randint(0, self.height))

    def initialize_forces(self):
        for v in self.grafo[0]:
            self.fuerzas[v] = (0.0, 0.0)

    def compute_attraction_forces(self):
        for v1, v2 in self.grafo[1]:
            distance = self.calculate_distance(self.posiciones[v1], self.posiciones[v2])
            if distance > self.error:
                mod_fa = self.f_attraction(distance)
                force = self.calculate_force(mod_fa, distance, self.posiciones[v1], self.posiciones[v2])
                self.fuerzas[v1] = sumar_tupla(self.fuerzas[v1], force)
                self.fuerzas[v2] = restar_tupla(self.fuerzas[v2], force)

    def compute_repulsion_forces(self):
        for v1 in self.grafo[0]:
            for v2 in self.grafo[0]:
                if v1 != v2:
                    distance = self.calculate_distance(self.posiciones[v1], self.posiciones[v2])
                    if distance > self.error:
                        mod_fr = self.f_respulsion(distance)
                        force = self.calculate_force(mod_fr, distance, self.posiciones[v1], self.posiciones[v2])
                        self.fuerzas[v1] = sumar_tupla(self.fuerzas[v1], force)
                        self.fuerzas[v2] = restar_tupla(self.fuerzas[v2], force)
                    else:
                        force = (random.randint(-int(self.width / 4), int(self.width / 4)),
                                 random.randint(-int(self.height / 4), int(self.height / 4)))
                        self.fuerzas[v1] = sumar_tupla(self.fuerzas[v1], force)
                        self.fuerzas[v2] = restar_tupla(self.fuerzas[v2], force)

    @staticmethod
    def calculate_distance(v1, v2):
        return math.sqrt(math.pow(v1[0] - v2[0], 2) +
                         math.pow(v1[1] - v2[1], 2))

    @staticmethod
    def calculate_force(mod_fa, distance, v1, v2):
        return (mod_fa * (v2[0] - v1[0]) / distance,
                mod_fa * (v2[1] - v1[1]) / distance)

    def update_positions(self):
        for v in self.grafo[0]:
            modulo = math.sqrt(math.pow(self.fuerzas[v][0], 2) + math.pow(self.fuerzas[v][1], 2))
            if modulo > self.temperature:
                self.fuerzas[v] = (self.fuerzas[v][0] * self.temperature / modulo,
                                   self.fuerzas[v][1] * self.temperature / modulo)
            pos = sumar_tupla(self.posiciones[v], self.fuerzas[v])
            if pos[0] < 0:
                pos = 0, pos[1]
            if pos[0] > self.width:
                pos = self.width, pos[1]
            if pos[1] < 0:
                pos = pos[0], 0
            if pos[1] > self.height:
                pos = pos[0], self.height
            self.posiciones[v] = pos

    def f_attraction(self, distance):
        return math.pow(distance, 2) / self.kAttraction

    def f_respulsion(self, distance):
        return math.pow(self.kRepulsion, 2) / distance

    def compute_gravity_forces(self):
        for v in self.grafo[0]:
            center = self.width / 2, self.height / 2
            distance = self.calculate_distance(self.posiciones[v], center)
            mod_fa = self.f_attraction(distance)
            force = self.calculate_force(mod_fa, distance, self.posiciones[v], center)
            force = force[0] / 10, force[1] / 10
            self.fuerzas[v] = sumar_tupla(self.fuerzas[v], force)

    def update_temperature(self):
        self.temperature = self.temperatureConstant * self.temperature

    def fruchterman_reingold_step(self):
        self.initialize_forces()
        self.compute_attraction_forces()
        self.compute_repulsion_forces()
        self.compute_gravity_forces()
        self.update_positions()
        self.update_temperature()
        """
        # initialize temperature()
        # initialize forces()
        # compute attraction forces()
        # compute repulsion forces()
        # compute gravity forces()
        # update positions()
        # update temperature()
        {nombre, ((,),(,))
        """


def sumar_tupla(a, b):
    return a[0] + b[0], a[1] + b[1]


def restar_tupla(a, b):
    return a[0] - b[0], a[1] - b[1]


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
        default=100
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
        default=50.0
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
        width=400,
        height=400,
        verbose=args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
