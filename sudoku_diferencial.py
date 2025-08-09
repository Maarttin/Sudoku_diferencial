import numpy as np
import random
import copy
from colorama import init, Fore

init(autoreset=True)
N = 9
pop_size = 400
generations = 2000
F = 0.5
CR = 0.3

sudoku_inicial = [
    [8, 0, 6, 0, 0, 0, 1, 0, 7],
    [0, 0, 0, 6, 0, 2, 0, 0, 0],
    [0, 5, 3, 0, 0, 4, 8, 0, 6],
    [7, 0, 4, 8, 0, 0, 6, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [1, 0, 0, 5, 0, 0, 4, 0, 0],
    [0, 0, 1, 2, 0, 0, 7, 0, 9],
    [2, 0, 0, 0, 9, 6, 0, 0, 0],
    [0, 7, 0, 0, 1, 0, 0, 8, 0]
]

def generar_individuo(base, fijas):
    individuo = copy.deepcopy(base)
    for i in range(N):
        faltantes = [n for n in range(1, 10) if n not in individuo[i]]
        random.shuffle(faltantes)
        idx = 0
        for j in range(N):
            if not fijas[i][j]:
                individuo[i][j] = faltantes[idx]
                idx += 1
    return individuo

def poblacion_inicial(base, tam):
    fijas = [[cell != 0 for cell in row] for row in base]
    return [generar_individuo(base, fijas) for _ in range(tam)], fijas

def aptitud(tablero):
    errores = 0
    for i in range(N):
        errores += N - len(set(tablero[i]))
        errores += N - len(set(tablero[j][i] for j in range(N)))
    for x in range(0, N, 3):
        for y in range(0, N, 3):
            bloque = [tablero[i][j] for i in range(x, x+3) for j in range(y, y+3)]
            errores += N - len(set(bloque))
    return 1 / (1 + errores)

def mutacion(poblacion, i):
    idxs = list(range(pop_size))
    idxs.remove(i)
    r1, r2, r3 = random.sample(idxs, 3)
    trial = []
    for f in range(N):
        v = np.array(poblacion[r1][f]) + F * (np.array(poblacion[r2][f]) - np.array(poblacion[r3][f]))
        v = [int(round(val)) for val in v]
        v = [min(max(1, val), 9) for val in v]
        trial.append(v)
    return trial

def cruce(mutante, objetivo, fijas):
    hijo = copy.deepcopy(objetivo)
    for i in range(N):
        for j in range(N):
            if not fijas[i][j] and random.random() < CR:
                hijo[i][j] = mutante[i][j]
    return hijo

def imprimir_tablero(tablero, fijas):
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if fijas[i][j]:
                print(Fore.BLUE + str(tablero[i][j]), end=" ")
            else:
                print(str(tablero[i][j]), end=" ")
        print()

def main():
    poblacion, fijas = poblacion_inicial(sudoku_inicial, pop_size)
    mejor = max(poblacion, key=aptitud)

    for gen in range(generations):
        nueva_poblacion = []
        for i in range(pop_size):
            mutante = mutacion(poblacion, i)
            trial = cruce(mutante, poblacion[i], fijas)
            if aptitud(trial) > aptitud(poblacion[i]):
                nueva_poblacion.append(trial)
            else:
                nueva_poblacion.append(poblacion[i])

        poblacion = nueva_poblacion
        mejor_actual = max(poblacion, key=aptitud)
        if aptitud(mejor_actual) > aptitud(mejor):
            mejor = copy.deepcopy(mejor_actual)

        print(f"Generación {gen+1}, Aptitud: {aptitud(mejor):.5f}, Errores: {int(1/aptitud(mejor) - 1)}")

        if aptitud(mejor) == 1.0:
            print(f"\nSolución encontrada en la generación {gen+1}:")
            break

    imprimir_tablero(mejor, fijas)

if __name__ == "__main__":
    main()
