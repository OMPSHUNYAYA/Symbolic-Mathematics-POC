# **Getting Started — Scenario 08: Forecast — three models disagree**

**Domain.** Planning / Forecasting / AI operations

**What this shows.** When multiple forecasters disagree, the classical mean can hide instability. SSM preserves the same magnitude and adds a bounded alignment `a in (-1,+1)` so teams can see posture *(trust, double-check, or defer)* without changing arithmetic.

**1) Setup (inputs)**  
Three forecast models for next-day demand:
- **Model_A:** `m = 100.0`, `a = +0.75`  
- **Model_B:** `m = 96.0`,  `a = +0.15`  
- **Model_C:** `m = 104.0`, `a = +0.10`

Note. `a` is a bounded alignment dial; collapse parity `phi((m,a)) = m`.

**2) Classical arithmetic (computer-algebra arithmetic)**

Operation — mean of three point estimates.

```python
# classical illustration (no external packages required)
x1, x2, x3 = 100.0, 96.0, 104.0
mean = (x1 + x2 + x3) / 3.0
print(mean)  # 100.0

```

**Classical result.** `100.0`  
**Reading.** Looks “perfectly normal.” Says nothing about disagreement or reliability.

**3) SSM arithmetic (same magnitude + alignment lane)**

**Magnitude (collapse parity).** Keep the same mean: `m = 100.0`.

**Alignment pooling (sum rule, order-invariant).**
- `a_c := clamp(a, -1+eps, +1-eps)`
- `u := atanh(a_c)`
- `w := |m|^gamma` *(default `gamma = 1`)*
- `U += w * u`
- `W += w`
- `a_out := tanh( U / max(W, eps) )`

**Numbers (rounded).**
- `atanh(0.75) ≈ 0.9729551`, `w = 100.0` → contributes `97.2955`
- `atanh(0.15) ≈ 0.1511404`, `w = 96.0`  → contributes `14.5043`
- `atanh(0.10) ≈ 0.1003353`, `w = 104.0` → contributes `10.4349`  
  `U = 97.2955 + 14.5043 + 10.4349 ≈ 122.2347`  
  `W = 100.0 + 96.0 + 104.0 = 300.0`  
  `t = U / W ≈ 0.4074`  
  `a_out = tanh(t) ≈ +0.3863`

**SSM result.** `m = 100.0`, `a ≈ +0.3863`

**4) Tiny script (copy-paste)**

```python
# scenario_08_forecast.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))  # atanh
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
model_A = (100.0, +0.75)
model_B = (96.0,  +0.15)
model_C = (104.0, +0.10)

# classical magnitude
m = (model_A[0] + model_B[0] + model_C[0]) / 3.0

# SSM pooled alignment
a = ssm_align_weighted([
    (model_A[1], model_A[0]),
    (model_B[1], model_B[0]),
    (model_C[1], model_C[0]),
])

print("Classical:", f"{m:.4f}")         # 100.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}") # a ≈ +0.3863

```

**5) What to expect.**

- **Classical.** `100.0`
- **SSM.** `m=100.0, a≈+0.386` *(rounded; `gamma=1`)*

**6) Why this helps in the real world**

- **Plan confidence.** Same headline magnitude, now with a visible stability dial.  
- **Action gating.** Use `a` to choose between ship, double-check, or defer.  
- **Explains variance.** The high-drift model doesn’t silently dominate the average; its influence is surfaced.

**When calm (agreement).** If each forecaster had `a ≈ 0`, pooling yields `a ≈ 0` and SSM ≡ Classical (`phi((m,a)) = m`).

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.

