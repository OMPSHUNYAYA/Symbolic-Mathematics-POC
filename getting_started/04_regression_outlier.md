# **Getting Started — Scenario 04: Regression Distorted by a Single Outlier**

**Domain.** Data Analysis / Modeling

**What this shows.** A single abnormal point can skew a classical summary. SSM keeps the same magnitude but adds alignment `a` to reveal whether that value is trustworthy or fragile.

**1) Setup (inputs)**
Repeated measurements in a simple regression-like setting:
`(10.0, a = +0.05)`  — stable
`(11.0, a = +0.08)`  — stable
`(10.5, a = +0.03)`  — stable
`(40.0, a = +0.90)`  — strong outlier / extreme drift
`a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

```python

# classical illustration (no external packages required)
x1, x2, x3, x4 = 10.0, 11.0, 10.5, 40.0
mean = (x1 + x2 + x3 + x4) / 4
print(mean)  # 17.875

```

Classical result. 17.875  
Observed issue. The outlier pushes the model upward, but the number alone gives no warning.

**3) SSM calculation (same magnitude + alignment lane)**

**Sum pooling rule (alignment lane):**
`a_c := clamp(a, -1+eps, +1-eps)`
`u := atanh(a_c)`
`U += w * u`  with `w := |m|^gamma`  (default `gamma = 1`)
`W += w`
`a_out := tanh( U / max(W, eps) )`

**Interpretation.** Magnitude remains `17.875` (collapse parity).
Alignment `a_out ≈ +0.690` exposes instability from the outlier.

```python

# scenario_04_regression_outlier.py  (ASCII-only, top-level prints)

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
r1 = (10.0, +0.05)
r2 = (11.0, +0.08)
r3 = (10.5, +0.03)
r4 = (40.0, +0.90)

# classical magnitude
m = (r1[0] + r2[0] + r3[0] + r4[0]) / 4.0

# SSM pooled alignment
a = ssm_align_weighted([
    (r1[1], r1[0]),
    (r2[1], r2[0]),
    (r3[1], r3[0]),
    (r4[1], r4[0]),
])

print("Classical:", f"{m:.4f}")                 # 17.8750
print("SSM:", f"m={m:.4f}, a={a:+.4f}")         # a ≈ +0.690

```

**What to expect.**  
`Classical: 17.875`  
`SSM: m=17.875, a≈+0.690`

**6) Why this helps in the real world**
- The number stays correct.
- The alignment shows whether the number is stable.
- Prevents silent model distortion when one data point dominates.
- Supports robust regression, forecasting, anomaly detection, and safer model governance.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
