import numpy as np
import random
import copy
from colorama import init, Fore

init(autoreset=True)
N=9
tam_poblacion = 400
num_generaciones = 2000
prob_mutacion = 0.09

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

def poblacion_inicial(sudoku_inicial, tam_poblacion):
    poblacion = []
    
    for _ in range(tam_poblacion):
        individuo = copy.deepcopy(sudoku_inicial)

        for fila in range(N):
            fijos = [num for num in individuo[fila] if num != 0]
            faltantes = [n for n in range(1, N+1) if n not in fijos]
            random.shuffle(faltantes)
            
            idx = 0
            for col in range(N):
                if individuo[fila][col] == 0:
                    individuo[fila][col] = faltantes[idx]
                    idx += 1                

        poblacion.append(individuo)

    return poblacion

def aptitud(solucion):
    errores = 0
    
    for fila in solucion:
        errores += N - len(set(fila))
    
    for col in range(N):
        columna = [solucion[fila][col] for fila in range(N)]
        errores += N - len(set(columna))

    for fila_ini in [0, 3, 6]:
        for col_ini in [0, 3, 6]:
            bloque = []
            for i in range(3):
                for j in range(3):
                    bloque.append(solucion[fila_ini + i][col_ini + j])
            errores += N - len(set(bloque))
    return 1 / (1 + errores)

#1/1+ataques
#seleccion por ruleta , cruza y mutacion uniforme
def seleccion_ruleta(poblacion):
    seleccionados = []
    aptitudes = [aptitud(individuo) for individuo in poblacion]
    suma_aptitudes = sum(aptitudes)
    valor_esperado = [ap/suma_aptitudes for ap in aptitudes]
    suma_esperados = sum(valor_esperado)
    
    for _ in range(tam_poblacion):
        suma_acumulada = 0
        r = random.uniform(0, suma_esperados)
        for i, v in enumerate(valor_esperado):
            suma_acumulada += v
            if suma_acumulada >= r:
                seleccionados.append(poblacion[i])
                break
        
    return seleccionados 

def cruza_uniforme(p1, p2, prob=0.5):
    hijo = []

    for i in range(N):  
        if random.random() < prob:
            hijo.append(copy.deepcopy(p1[i]))
        else:
            hijo.append(copy.deepcopy(p2[i]))
    
    return hijo


def mutar_uniforme(individuo, fijas, prob_mutacion=0.1):
    for i in range(N):  
        libres = [j for j in range(N) if not fijas[i][j]]
        if len(libres)>=2 and random.random() <= prob_mutacion:
            a, b = random.sample(libres, 2)
            
            individuo[i][a], individuo[i][b] = individuo[i][b], individuo[i][a]
    return individuo


def imprimir_tablero(tablero, fijas):
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            
            if sudoku_inicial[i][j] ==0:
                print(tablero[i][j], end=" ")
            else:
                print(Fore.BLUE+str(tablero[i][j]), end=" ")
        print()

def main():
    poblacion = poblacion_inicial(sudoku_inicial, tam_poblacion)
    celdas_fijas = [[sudoku_inicial[i][j] != 0 for j in range(N)] for i in range(N)]
    mejor_global = max(poblacion, key=aptitud)
    for generacion in range(num_generaciones):
        poblacion = seleccion_ruleta(poblacion)
        nueva_poblacion = []
        
        for i in range(0, tam_poblacion, 2):
            padre1, padre2 = poblacion[i], poblacion[i+1]
            hijo1, hijo2 = mutar_uniforme(cruza_uniforme(padre1,padre2),celdas_fijas,prob_mutacion), mutar_uniforme(cruza_uniforme(padre2,padre1),celdas_fijas,prob_mutacion)
            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion  
        
        mejor_actual= max(poblacion, key=aptitud)
        if aptitud(mejor_actual) > aptitud(mejor_global):
            mejor_global = copy.deepcopy(mejor_actual)
        else:
            # Reemplaza el peor por el mejor_global
            peor_idx = min(range(len(poblacion)), key=lambda i: aptitud(poblacion[i]))
            poblacion[peor_idx] = copy.deepcopy(mejor_global)
        if aptitud(mejor_global) == 1.0:
            print(f"Solución encontrada en la generación {generacion+1} con aptitud: {aptitud(mejor_global)}, errores={(1/aptitud(mejor_global))-1}")
            break


        
        print(f"Generación {generacion+1}, Mejor aptitud: {aptitud(mejor_global)}, errores={(1/aptitud(mejor_global))-1}")
    imprimir_tablero(mejor_global, celdas_fijas)
    
    
if __name__ == "__main__":
    main()
    
    
#evolucion diferencial