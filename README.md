# Practice 1 — Donor Networks (AI 2024/25)

> Author: **Lluís F. Collell**  
> **Artificial Intelligence** course · University of Girona

## 📜 Description

Algorithm to build **4 donor networks** from **40 hospitals** by combining:

1. **Euclidean distance** between hospitals.  
2. **Population similarity** (`matchBN`) weighted by a parameter `µ` (0 ≤ µ ≤ 1).

The goal is to **minimize the intra-network distance** of each network while **maximizing** population similarity (`µ·sim`) among hospitals in the same network.

---

## ✏️ Algorithm

The solution is based on **Local Beam Search (LBS)** with *swap* and *shift* neighborhoods.

- **State representation:** vector of length 40 with values `{0, 1, 2, 3}` indicating the network assigned to each hospital.
- **Initial states:** `B` random assignments generated with `creacio_beam_aleatories`.

### Neighborhood

- `swap(i, j)`: exchanges two hospitals belonging to different networks.  
- `shift(i → j)`: moves a hospital from its current network to another one.

### Objective function

The function to optimize is:

where:
- `dist(g)`: average distance between hospitals within the same network (intra-network).
- `sim(g)`: average similarity between hospitals within the same network, computed using the Bayesian network `matchBN`.
- `µ`: weighting parameter balancing distance and similarity (0 ≤ µ ≤ 1).

### Stopping criterion

The algorithm stops when:

- No improvement is found in an iteration, **or**
- A maximum of `K` iterations is reached.

### Complexity (worst case)

| Step               | Complexity   |
|--------------------|--------------|
| Generate neighbors | B · N²       |
| Evaluate the beam  | B · N²       |
| Total iterations   | K · B · N²   |

---

## 🧠 Bayesian Networks and Inference

- `criticalBN` (provided): models the probability of critical cases using variables `I`, `J`, `C`, `K`.
- `matchBN` (implemented): duplicates the structure of `criticalBN` for two hospitals and adds the variable `M` (*match*).

### Main rule

> If `C₁ = C₂` then `P(M = T) = 0.95`;  
> Otherwise, `P(M = T) = 0.10`.

### Inference

- **Exact:** `variable_elimination`, requiring a good elimination order.
- **Approximate:**
  - `rejection_sampling`
  - `weighted_sampling` (with likelihood weighting)

The report analyzes how many samples (`N`) are required for approximate inference to converge to the exact results.

This Bayesian network allows us to incorporate **population similarity** directly into the objective function via the term `µ·sim(g)`.

---

## 🗂️ Project structure

```text
.
├── s1/                    # Session 1 materials
│   ├── main1.py
│   └── datapoints.csv
├── s2/                    # Session 2 materials / final submission
│   ├── main2.py
│   ├── data.csv
│   ├── bn.py
│   ├── my_bns.py
│   └── inferencia.py
├── p1.py                  # Main algorithm (Local Beam Search)
├── report.pdf             # Full project report
├── p1_statement.pdf       # Assignment statement
└── README.md              # This file
