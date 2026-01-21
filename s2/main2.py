import numpy as np
from timeit import default_timer as timer
import copy

from my_bns import *
from inferencia import rejection_sampling



#Funció objectiu en py:

def distancia(p1, p2):
    """ Distància Euclidiana entre dos punts"""
    return np.linalg.norm(p1 - p2)

def distancia_mitjana_xarxa(problema, xarxa):
    sumatori_distancia = 0

    for i in range(len(xarxa) - 1):
        for j in range(i + 1, len(xarxa)):
            sumatori_distancia += problema["matriu_distancies"][xarxa[i], xarxa[j]]

    return sumatori_distancia * 2 / (len(xarxa) * (len(xarxa) - 1))

def similitud_xarxa(problema, xarxa, model_bn):
    sumatori_similitud = 0
    
    if len(xarxa) < 2:  # Si la xarxa té 1 o 0 hospitals, similitud és 0
        return 0
    
    for i in range(len(xarxa) - 1):
        for j in range(i + 1, len(xarxa)):
            h1 = problema["data"][xarxa[i]]  # Característiques de l'hospital i
            h2 = problema["data"][xarxa[j]]  # Característiques de l'hospital j
            
            # Extreiem els valors de (I, J, K) per cada hospital
            I1, J1, K1 = h1[0], h1[1], h1[2]
            I2, J2, K2 = h2[0], h2[1], h2[2]
            
            # Calculem P(M=True | I1, J1, K1, I2, J2, K2) fent inferència a matchBN
            probabilitat_match = model_bn.probability([('M', True)], {'I1': I1, 'J1': J1, 'K1': K1,
                                                           'I2': I2, 'J2': J2, 'K2': K2})
            sumatori_similitud += probabilitat_match

    return (2 / (len(xarxa) * (len(xarxa) - 1))) * sumatori_similitud

def calcul_match_mitja(problema, estat_actual, mu = 0, model_bn):
    sumatori_match = 0

    for g in range(problema["n_groups"]):
        sumatori_match += len(estat_actual[g]) * (distancia_mitjana_xarxa(problema, estat_actual[g]) - mu * similitud_xarxa(problema, estat_actual[g], model_bn))

    return sumatori_match / problema["n_elements"]

def obtenir_valors_per_variables(descriptors, valors, sufix=""):
    assert len(descriptors) == len(valors)
    e = {}
    for i in range(len(descriptors)):
        if not np.isnan(valors[i]):
            e[descriptors[i]+sufix]=valors[i]
    return e


def cerca_local_beam(problema, beam_size=5, iteracions=10):
    """ Executa la cerca local per feixos (beams).
    `beam_size` determina el nombre d'assignacions que passen entre iteracions
    `iterations` determina el nombre d'iteracions"""
    # CREAR i GUARDAR a `beam` les `beam_size` assignacions inicials
    # AVALUAR les assignacions inicials

    # Per cada iteració, mentre sigui necessari:
        # BUSCAR VEINS de cada assignació del beam que milloren l'actual
        # AVALUAR-LOS
        # SELECCIONAR els `beam_size` millors veins i GUARDAR-los a `beam`

        # COMPROVAR si calen més iteracions

    # RETORNAR millor assignació del beam

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
    np.random.seed(11) # Fixem la llavor per reproducibilitat

    # Carreguem les dades
    X = np.loadtxt("data.csv", delimiter=",", dtype=float, skiprows=1)

    problema = dict()
    problema["data"] = X
    problema["n_elements"] = X.shape[0]
    problema["ndim"] = 2

    problema["n_groups"] = 4

    problema["matriu_distancies"] = calcular_matriu_distancies(problema)

    # Defineix i enllaça aquí la funció d'avaluació
    #problema["weight"] = 1 # pes de la similitud a la funció d'avaluació
    #problema["f_aval"] = la_meva_funcio_davaluacio


    # ------------------------------------------------------------
    # 2. Configurem i executem la cerca local beam ---------------
    beam_size = 5  # B
    n_iterations = 100  # K


    t_start = timer()
    #res = cerca_local_beam(problema, beam_size, n_iterations)
    t_end = timer()

    #print("Millor assignació trobada:", res)
    print("En", t_end - t_start, "segons.")


    # ------------------------------------------------------------
    # ----------- Com fer servir el codi que us donem ------------
    # ------------------------------------------------------------
    # Càlcul de la distància entre dos punts: vigileu, les dades inclouen ara altres variables!
    d = problema["ndim"]
    print("Distància entre punts 1 i 2:", distancia(problema["data"][1,:d], problema["data"][2,:d]))

    # Fer servir rejection-sampling per respondre una pregunta p(X|E=e)
    pd = rejection_sampling("C", {"I":T}, criticalBN, ordre_anc_criticalBN, N=100)
    print("P(C|I=True)=",pd.show())
    print("P(C=True|I=True)=",pd[T])

    # També us donem un mètode per recuperar les dades del dataset
    # d'una manera apropiada per treballar amb BayesNet
    dic = obtenir_valors_per_variables(["I", "J", "K"], problema["data"][1,d:])
    print(problema["data"][1,d:],"es transforma en",dic)

    # Fes servir el prefix si vols canviar el nom de les variables
    dic1 = obtenir_valors_per_variables(["I", "J", "K"], problema["data"][3,d:], sufix="a")
    dic2 = obtenir_valors_per_variables(["I", "J", "K"], problema["data"][4,d:], sufix="b")
    dic = dic1 | dic2
    print(problema["data"][3,d:]," i ", problema["data"][4,d:],"es combinen per formar",dic)


if __name__ == '__main__':
    main()
