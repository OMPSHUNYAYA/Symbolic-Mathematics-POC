# **Getting Started — Scenario 06: Chemistry — Activation energy from repeated runs**

**Domain.** Chemistry / Experimental kinetics

**What this shows.** Two runs can share the same headline magnitude while carrying different posture. SSM preserves the classical mean `m` and surfaces the alignment `a` so you can judge trust in that mean.

**1) Setup (inputs)**  
Two independent runs estimate activation energy *(kJ/mol)* and report a bounded alignment `a in (-1,+1)`:
- **Run A:** `m = 51.2`, `a = +0.70`  
- **Run B:** `m = 54.8`, `a = +0.15`  

Bounded lane; collapse parity holds: `phi((m,a)) = m`.

**2) Classical result (arithmetic)**

Mean activation energy: `(51.2 + 54.8) / 2 = 106.0 / 2 = 53.0`  
**Classical result.** `53.0 kJ/mol`

```python
# classical mean only
vals = [51.2, 54.8]
mean = sum(vals) / len(vals)
print(mean)  # 53.0

```

**3) SSM result (same magnitude + alignment lane)**

**Collapse rule.** `phi((m,a)) = m` → **magnitude stays** `53.0`.

**Sum pooling (alignment lane).**
- `a_c := clamp(a, -1+eps, +1-eps)`
- `u := atanh(a_c)`
- `w := |m|^gamma` *(default `gamma = 1`)*
- `U += w * u`
- `W += w`
- `a_out := tanh( U / max(W, eps) )`

**Interpretation.** Value remains `53.0`; `a_out` lifts above zero if one run is unstable, exposing posture without changing the arithmetic.

**Numbers.**

- **Rapidities.** `u_A = atanh(0.70) ≈ 0.8673005277`, `u_B = atanh(0.15) ≈ 0.1511404359`
- **Weights.** `w_A = |51.2| = 51.2`, `w_B = |54.8| = 54.8` → `W = 51.2 + 54.8 = 106.0`
- **Accumulator.** `U ≈ 51.2*0.8673005277 + 54.8*0.1511404359 ≈ 52.6882829073`
- **Average rapidity.** `U/W ≈ 52.6882829073 / 106.0 ≈ 0.4970753114`
- **Alignment.** `a_out = tanh(0.4970753114) ≈ +0.4598`

**SSM result.** `m = 53.0`, `a ≈ +0.4598`

**4) Tiny script (copy-paste)**

```python
# scenario_06_activation_energy.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|**gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh via log: 0.5 * ln((1+a)/(1-a))
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
runA = (51.2, +0.70)
runB = (54.8, +0.15)

# classical magnitude (straight average)
m = 0.5 * (runA[0] + runB[0])

# SSM pooled alignment
a = ssm_align_weighted([(runA[1], runA[0]), (runB[1], runB[0])])

print("Classical:", f"{m:.4f}")         # 53.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}") # a ≈ +0.4598

```

**5) What to expect**

- **Classical.** `53.0 kJ/mol`
- **SSM.** `m=53.0, a≈+0.4598` *(rounded; `gamma=1`)*

**6) Interpretation**

- **Same headline, clearer truth.** The mean stays `53.0`, but `a≈+0.46` flags moderate fragility driven by Run A’s higher drift.
- **When calm, SSM collapses.** If both runs had `a≈0`, then `a_out≈0` and SSM ≡ Classical in both value and posture.

**7) Benefit in practice**

- **Quality-aware merging.** Repeat or down-weight runs with high drift before publishing a final activation energy.  
- **Better lab practice.** Track `a` as a protocol-health hint alongside `m`.  
- **Safer downstream use.** Fits and simulations respond to posture rather than trusting magnitude alone.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
