# **Getting Started — Scenario 03: Three Sensors and Triangulation Drift**

**Domain.** Physical Measurement / Scientific Instrumentation

**What this shows.** When multiple sensors disagree, the classical mean can hide drift. SSM keeps the same magnitude and adds alignment `a` that reveals reliability.

**1) Setup (inputs)**  
Three sensors measuring the same quantity:  
`(9.8,  a = +0.05)`  — stable  
`(10.1, a = +0.12)`  — mildly variable  
`(9.4,  a = +0.72)`  — drifting / noisy  
`a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

```python

# classical illustration (no external packages required)
x1, x2, x3 = 9.8, 10.1, 9.4
mean = (x1 + x2 + x3) / 3
print(mean)  # 9.766666...

```
Classical result. ~9.7667

**3) SSM calculation (same magnitude + alignment lane)**  

**Sum pooling rule (alignment lane)**  
`a_c := clamp(a, -1+eps, +1-eps)`  
`u := atanh(a_c)`  
`U += w * u` with `w := |m|^gamma` (default `gamma = 1`)  
`W += w`  
`a_out := tanh( U / max(W, eps) )`  

**Interpretation.** Magnitude remains `9.7667` (collapse parity).  
Alignment `a_out ≈ +0.336` signals noticeable drift from the unstable sensor.

```python

# scenario_03_three_sensors.py  (ASCII-only, top-level prints)

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
s1 = (9.8,  +0.05)
s2 = (10.1, +0.12)
s3 = (9.4,  +0.72)

# classical magnitude (straight average)
m = (s1[0] + s2[0] + s3[0]) / 3.0

# SSM pooled alignment
a = ssm_align_weighted([(s1[1], s1[0]), (s2[1], s2[0]), (s3[1], s3[0])])

print("Classical:", f"{m:.4f}")                 # ~9.7667
print("SSM:", f"m={m:.4f}, a={a:+.4f}")         # a ≈ +0.336

```

**What to expect.**  
`Classical: ~9.7667`  
`SSM: m=9.7667, a≈+0.336`

**6) Why this helps in the real world**
- Magnitude stays the same (no disruption).
- Alignment reveals drift from a noisy sensor.
- Supports calibration checks, safety monitoring, signal fusion, and control tuning.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.

