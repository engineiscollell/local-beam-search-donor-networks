import numpy as np
from bn import BayesNet, ProbDist


def variable_elimination(X, e, bn, elimination_order):
    """
     Calcula la distribució de la variable `X` donat que
     s'ha observat `E=e` fent servir variable-elimination.
     Retorna una distribució de probabilitat sobre X.
    """
    assert X not in e, "No es pot demanar la distribució d'una variable observada"
    factors = []
    for i in elimination_order:
        var = bn.variables[i]
        f = bn.variable_node(var).to_factor(bn)
        # REDUIR `f` amb els valors d'`e`, si s'escau
        factors.append(f)
        # si var pertany a H (no és X ni pertany a E):
            # TREURE de `factors` tots aquells que facin servir la variable `var`
            # PRODUCTE de tots els factors extrets al pas anterior
            # MARGINALITZAR (eliminar) variable `var` del factor resultant del pas anterior
            # AFEGIR a `factors` el factor resultant del pas anterior

    # PRODUCTE de tots els factors que puguin quedar a `factors`
    # NORMALITZAR el factor resultant del pas anterior
    # RETORNAR la distribució de probabilitat resultant del pas anterior


# _________________________________________________________________________
# _________________________________________________________________________
# _________________________________________________________________________



def rejection_sampling(X, e, bn, sampling_ordering, N=1000):
    """
     Estima la distribució de la variable `X` donat que
     s'ha observat `E=e` fent servir rejection-sampling.
     Retorna una distribució de probabilitat sobre X.
    """
    counts = {x: 0.1 for x in bn.variable_values(X)}
    for _ in range(N):
        # Obtenim un exemple de la xarxa Bayesiana `bn`
        exemple = forward_sampling(bn, sampling_ordering)
        # És consistent amb l'observat si els valors de les variables
        # observades és el mateix (a l'exemple i a `e`)
        consistencia = all(exemple.get(var) == valor
                           for var, valor in e.items())
        if consistencia:
            counts[exemple[X]] += 1 # el comptem només si és consistent
    return ProbDist(X, counts)


def forward_sampling(bn:BayesNet, sampling_ordering):
    """
    Obtenir un exemple de la distribució conjunta representada
    per la xarxa Bayesiana `bn`. Necessita un ordre en què
    obtener una mostra de les variables
    Retorna un diccionari {variable: valor}
    """
    exemple = {}
    for i in sampling_ordering:
        node = bn.variable_node(bn.variables[i])
        exemple[node.variable] = node.sample(exemple)
    return exemple




# _________________________________________________________________________
# _________________________________________________________________________
# _________________________________________________________________________


def weighted_sampling(X, e, bn, sampling_ordering, N=1000):
    """
     Estima la distribució de la variable `X` donat que
     s'ha observat `E=e` fent servir rejection-sampling.
     Retorna una distribució de probabilitat sobre X.
    """
    for _ in range(N):
        _# OBTENIR UN EXEMPLE I EL SEU PES amb `likelihood_weighting`
        # ACUMULAR PES com correspongui

    # RETORNA una distribució de probablitat segons els pesos


def likelihood_weighting(e, bn, sampling_ordering):
    """
    Obtenir un exemple de la distribució conjunta representada
    per la xarxa Bayesiana `bn` consistent amb `e`. Necessita un
    ordre en què obtenir una mostra de les variables
    Retorna un exemple (diccionari {variable: valor}) i
     la versemblança d'aquest
    """
    # Pots necessitar mirar-te com funciona el mètode BayesNode.p() del fitxer bn.py
    # RETORNAR exemple i pes

