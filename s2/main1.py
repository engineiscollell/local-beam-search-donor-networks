import numpy as np
from timeit import default_timer as timer
import copy
import random

def distancia(p1, p2):
    """ Distància Euclidiana entre dos punts"""
    return np.linalg.norm(p1 - p2)

def distancia_mitjana_xarxa(problema, xarxa):
    sumatori_distancia = 0

    for i in range(len(xarxa) - 1):
        for j in range(i + 1, len(xarxa)):
            sumatori_distancia += problema["matriu_distancies"][xarxa[i], xarxa[j]]

    return sumatori_distancia * 2 / (len(xarxa) * (len(xarxa) - 1))

def calcul_distancia_mitjana(problema, estat_actual):
    sumatori_distancies = 0

    for g in range(problema["n_groups"]):
        sumatori_distancies += len(estat_actual[g]) * distancia_mitjana_xarxa(problema, estat_actual[g])

    return sumatori_distancies / problema["n_elements"]

# Definició estats inicials
def assignacio_hospitals_aleatoria(problema):
    xarxes = [[] for _ in range(problema["n_groups"])] 

    for i in range(problema["n_elements"]):
        xarxes[random.randrange(0, problema["n_groups"])].append(i)  # Guardem només l'índex

    return xarxes

def creacio_beam_aleatories(problema, beam_size):
    return [assignacio_hospitals_aleatoria(problema) for _ in range(beam_size)]

def assignacio_beam(problema, beam, beam_size):
    for i in range(beam_size):
        estat_actual = beam[i]
        distancia = calcul_distancia_mitjana(problema, estat_actual)
        beam[i] = (estat_actual, distancia) 

def generar_veins(problema, beam, beam_size):
    nous_veins = []

    # Generem els veïns usant el mètode swap
    for e in range(beam_size):
        estat_actual = beam[e][0]

        for fila1 in range(problema["n_groups"]):  
            for fila2 in range(problema["n_groups"]):
                if fila1 != fila2:
                    for i in range(len(estat_actual[fila1])):
                        for j in range(len(estat_actual[fila2])):
                            vei = copy.deepcopy(estat_actual)
                            vei[fila1][i], vei[fila2][j] = vei[fila2][j], vei[fila1][i]
                            distancia_mitjana = calcul_distancia_mitjana(problema, vei)
                            nous_veins.append([vei, distancia_mitjana])

    # Generem els veïns usant el mètode shift
    for e in range(beam_size):
        estat_actual = beam[e][0]

        for fila_origen in range(problema["n_groups"]): 
            for fila_desti in range(problema["n_groups"]):
                if fila_origen != fila_desti:  
                    for i in range(len(estat_actual[fila_origen])):
                        vei = copy.deepcopy(estat_actual)
                        valor = vei[fila_origen].pop(i)
                        vei[fila_desti].append(valor)
                        distancia_mitjana = calcul_distancia_mitjana(problema, vei)
                        nous_veins.append([vei, distancia_mitjana])

    # Ordenem els veïns per distància mitjana (menor a major)
    nous_veins = sorted(nous_veins, key=lambda x: x[1])

    # Actualitzem el beam amb els `beam_size` millors veïns
    beam[:] = [vei[0] for vei in nous_veins[:beam_size]]


def cerca_local_beam(problema, beam_size=5, iteracions=10):
    beam = creacio_beam_aleatories(problema, beam_size)
    assignacio_beam(problema, beam, beam_size)
    millor_distancia = min(beam, key=lambda x: x[1])[1]
    millor_estat = min(beam, key=lambda x: x[1])[0]
    iteracions_sense_millora = 0
    
    for _ in range(iteracions):
        generar_veins(problema, beam, beam_size)
        assignacio_beam(problema, beam, beam_size)
        millor_distancia_actual = min(beam, key=lambda x: x[1])[1]
        
        if millor_distancia_actual < millor_distancia:
            millor_distancia = millor_distancia_actual
            millor_estat = min(beam, key=lambda x: x[1])[0]
            iteracions_sense_millora = 0
        else:
            iteracions_sense_millora += 1
        
        if iteracions_sense_millora >= 1:
            break
    
    return millor_estat

def calcular_matriu_distancies(problema):
    matriu = np.zeros((problema["n_elements"], problema["n_elements"]))

    for i in range(problema["n_elements"]):
        for j in range(i + 1, problema["n_elements"]):  # Solo calcular la mitad superior (la matriz es simétrica)
            matriu[i, j] = distancia(problema["data"][i, :2], problema["data"][j, :2])
            matriu[j, i] = matriu[i, j]  # Copiar el valor en la parte inferior

    return matriu

def main():
    # ------------------------------------------------------------
    # 1. Configurem el problema ----------------------------------
    np.random.seed(11)  # Fixem la llavor per reproducibilitat

    # Carreguem les dades
    X = np.loadtxt("datapoints.csv", delimiter=",", dtype=float, skiprows=1)

    problema = dict()
    problema["data"] = X
    problema["n_elements"] = X.shape[0]
    problema["ndim"] = X.shape[1]
    problema["n_groups"] = 4

    #Afegim el càlcul total de distancies (matriu 40x40)
    problema["matriu_distancies"] = calcular_matriu_distancies(problema)

    beam_size = 5  # B
    n_iterations = 100  # K

    t_start = timer()
    res = cerca_local_beam(problema, beam_size, n_iterations)
    t_end = timer()

    print("Millor assignació trobada:", res)
    print("Temps:", t_end - t_start, "segons.")

if __name__ == '__main__':
    main()

