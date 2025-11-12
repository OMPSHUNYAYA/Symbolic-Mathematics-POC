# **Getting Started — Scenario 07: Hardware — multiply–accumulate chain**

**Domain.** Hardware / Systems *(multiply–accumulate pipeline)*

**What this shows.** Classical multiply–accumulate gives a single total. SSM keeps the same total and adds an alignment lane `a` that shows when the chain is trending toward instability *(e.g., saturation risk or fragile gain)*.

**1) Setup (inputs)**  
Three weight–input pairs `(m_w, a_w)` and `(m_x, a_x)` feed a multiply–accumulate stage.

**Weights**  
- `w1 = 0.5`, `a_w1 = +0.20`  
- `w2 = -1.2`, `a_w2 = +0.10`  
- `w3 = 0.8`, `a_w3 = +0.60`

**Inputs**  
- `x1 = 2.0`, `a_x1 = +0.30`  
- `x2 = -1.0`, `a_x2 = +0.70`  
- `x3 = 1.5`, `a_x3 = -0.10`

Notes. `a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

**2) Classical arithmetic (computer-algebra arithmetic)**

**Products**
- `p1 = w1 * x1 = 0.5 * 2.0 = 1.0`  
- `p2 = w2 * x2 = (-1.2) * (-1.0) = 1.2`  
- `p3 = w3 * x3 = 0.8 * 1.5 = 1.2`

**Accumulate**
- `total = p1 + p2 + p3 = 1.0 + 1.2 + 1.2 = 3.4`

**Classical result.** `3.4`

```python
# classical MAC only (no alignment)
w = [0.5, -1.2, 0.8]
x = [2.0, -1.0, 1.5]

p = [w[i] * x[i] for i in range(3)]
total = sum(p)
print(p)     # [1.0, 1.2, 1.2]
print(total) # 3.4

```

**3) SSM calculation (same magnitude + alignment lane)**

**Collapse parity (magnitude).** `phi((m,a)) = m` → classical total `m = 3.4` *(unchanged).*

**Product alignment (chaining per pair).**  
For each `(w_i, x_i)` with alignments `(a_wi, a_xi)`:
- `a_prod_i := tanh( atanh(a_wi) + atanh(a_xi) )`

**Sum alignment (pooling across products).**  
Use weighted rapidity mean with default `gamma = 1` and product magnitudes as weights:
- `a_c := clamp(a, -1+eps, +1-eps)`  
- `u := atanh(a_c)`  
- `U += w * u` with `w := |m|^gamma` *(here `m` is each product magnitude `|p_i|`)*  
- `W += w`  
- `a_out := tanh( U / max(W, eps) )`

**Interpretation.** We keep the numeric total `3.4` while `a_out` rises if product legs trend in the same fragile direction, revealing MAC-chain posture without changing arithmetic.

**Numbers.**

- **Product alignments (per pair).**  
  `a_p1 = tanh(atanh(+0.20) + atanh(+0.30)) ≈ +0.4717`  
  `a_p2 = tanh(atanh(+0.10) + atanh(+0.70)) ≈ +0.7477`  
  `a_p3 = tanh(atanh(+0.60) + atanh(-0.10)) ≈ +0.5319`

- **Product magnitudes (weights).** `|p1| = 1.0`, `|p2| = 1.2`, `|p3| = 1.2` → `W = 1.0 + 1.2 + 1.2 = 3.4`

- **Weighted rapidity mean.**  
  `U = Σ |p_i| * atanh(a_pi) ≈ 2.3848`  
  `U/W ≈ 2.3848 / 3.4 ≈ 0.7014` *(rapidity average)*

- **Pooled alignment.** `a_out = tanh(U/W) ≈ tanh(0.7014) ≈ +0.6053`

**SSM total.** `m = 3.4`, `a ≈ +0.605` *(rounded; `gamma=1`)*

**4) Tiny script (copy-paste)**

```python
# scenario_07_mac_chain.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def atanh(x):
    x = clamp(x)
    return 0.5 * math.log((1.0 + x) / (1.0 - x))

def a_prod(a_w, a_x):
    # product alignment: a_prod = tanh(atanh(a_w) + atanh(a_x))
    return math.tanh(atanh(a_w) + atanh(a_x))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, magnitude_m); weight w := |m|**gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        u = atanh(a_raw)
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs: (m, a) for weights and inputs separately
w = [(0.5,  +0.20), (-1.2, +0.10), (0.8,  +0.60)]
x = [(2.0,  +0.30), (-1.0, +0.70), (1.5,  -0.10)]

# classical products with product alignment
products = []
for (mw, aw), (mx, ax) in zip(w, x):
    m_prod = mw * mx
    a_prod_ix = a_prod(aw, ax)
    products.append((m_prod, a_prod_ix))  # (m_prod, a_prod)

# classical total magnitude
m_total = sum(m for (m, _) in products)

# pool alignment using product magnitudes as weights
a_total = ssm_align_weighted([(a, abs(m)) for (m, a) in products])

print("Classical:", f"{m_total:.4f}")         # 3.4000
print("SSM:", f"m={m_total:.4f}, a={a_total:+.4f}")  # a ≈ +0.6050

```

**5) What to expect**

- **Classical.** `3.4`
- **SSM.** `m=3.4, a≈+0.605` *(rounded; `gamma=1`)*

**6) Interpretation and benefit**

- **Magnitude agreement.** `phi((m,a)) = m` preserves the classical total `3.4`.
- **Posture warning.** `a ≈ +0.605` is elevated, driven by strongly aligned product legs; this hints at fragile gain or saturation risk.
- **Actionable insight.** Even if the total looks fine, the lane flags a “hot” MAC path—useful for gain control, saturation guards, or re-weighting before downstream stages.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
