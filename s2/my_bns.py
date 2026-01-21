from bn import BayesNet

# Per simplificar la notació, redefinim True i False com T i F
T, F = True, False

# Xarxa Bayesian CriticalBN
criticalBN = BayesNet([
    ('I', '', 0.7),
    ('J', 'I', {T: 0.8, F: 0.3}),
    ('C', 'I J',
     {(T, T): 0.95, (T, F): 0.64, (F, T): 0.29, (F, F): 0.01}),
    ('K', 'C', {T: 0.7, F: 0.1})
])

# Variables auxiliars per a CriticalBN
descriptors_criticalBN = ["I", "J", "K"]
var_depenent_criticalBN = "C"
ordre_anc_criticalBN = [0, 1, 2, 3]

# Xarxa Bayesian MatchBN
matchBN = BayesNet([
    # Primera subxarxa (Hospital 1)
    ('I1', '', 0.7),
    ('J1', 'I1', {T: 0.8, F: 0.3}),
    ('C1', 'I1 J1',
     {(T, T): 0.95, (T, F): 0.64, (F, T): 0.29, (F, F): 0.01}),
    ('K1', 'C1', {T: 0.7, F: 0.1}),

    # Segona subxarxa (Hospital 2)
    ('I2', '', 0.7),
    ('J2', 'I2', {T: 0.8, F: 0.3}),
    ('C2', 'I2 J2',
     {(T, T): 0.95, (T, F): 0.64, (F, T): 0.29, (F, F): 0.01}),
    ('K2', 'C2', {T: 0.7, F: 0.1}),

    # Node de similitud M entre els dos hospitals
    ('M', 'C1 C2', {
        (T, T): 0.95,
        (T, F): 0.1,
        (F, T): 0.1,
        (F, F): 0.1
    })
])

# Variables auxiliars per a MatchBN
descriptors_matchBN = ["I1", "J1", "K1", "I2", "J2", "K2"]
var_depenent_matchBN = ["C1", "C2"]
ordre_anc_matchBN = [0, 1, 2, 3, 4, 5, 6]
