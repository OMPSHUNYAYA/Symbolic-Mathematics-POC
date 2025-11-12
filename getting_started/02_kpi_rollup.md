# **Getting Started — Scenario 02: KPI Roll-Up With Hidden Instability**

**Domain.** Business / Performance Measurement

**What this shows.** Two KPIs can share the same headline magnitude yet carry very different stability. SSM preserves the classical value while surfacing posture via `a`, so planning can reflect where risk actually lives.

**1) Setup (inputs)**  
Quarterly indicators (normalized scale):  
`(102, a = +0.05)` — relatively steady segment  
`(118, a = +0.65)` — highly volatile segment  
`a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

```python

# classical illustration (no external packages required)
x1, x2 = 102, 118
mean = 0.5 * (x1 + x2)
print(mean)  # 110.0

```
Classical result. 110

**3) SSM calculation (same magnitude + alignment lane)**  

**Sum pooling rule (alignment lane)**  
`a_c := clamp(a, -1+eps, +1-eps)`  
`u := atanh(a_c)`  
`U += w * u` with `w := |m|^gamma` (default `gamma = 1`)  
`W += w`  
`a_out := tanh( U / max(W, eps) )`  

**Interpretation.** Magnitude stays `110` (collapse parity), while the pooled `a_out ≈ +0.415` signals noticeable drift due to the volatile segment.

```python

# scenario_02_kpi_rollup.py  (ASCII-only, top-level prints)

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
kpi1 = (102.0, +0.05)
kpi2 = (118.0, +0.65)

# classical magnitude (straight average)
m = 0.5 * (kpi1[0] + kpi2[0])

# SSM pooled alignment
a = ssm_align_weighted([(kpi1[1], kpi1[0]), (kpi2[1], kpi2[0])])

print("Classical:", f"{m:.4f}")                      # 110.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}")              # a ≈ +0.4148

```

**What to expect.**  
`Classical: 110`  
`SSM: m=110, a≈+0.415` (rounded; `gamma = 1`)

**6) Why this helps in the real world**
- The headline KPI remains 110 (no disruption to reports).
- Alignment shows where risk concentrates:
  - Investigate the volatile segment contributing 118.
  - Plan with risk-aware assumptions (avoid assuming stability).
  - Forecasting and capital allocation become more rational.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.

