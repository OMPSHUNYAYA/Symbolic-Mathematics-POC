# **Getting Started — Scenario 01: Two sensors disagree**

**Domain.** Physics / Instrumentation

**What this shows.** When readings conflict, the Classical mean can hide fragility; SSM adds posture via `a` so you can see risk before acting. When both sensors are steady, SSM collapses to Classical and you get the same answer (`phi((m,a)) = m`).

**POC display policy (simple).** For readability in this POC, larger printed `a` indicates more drift (`a_semantics = "drift-positive"`). You can flip this convention without changing the math or `phi((m,a)) = m`.

**1) Setup (inputs)**  
Two thermometers read the same beaker; one is noisy.  
`x1 = 12.4, a1 = +0.80`  
`x2 = 12.9, a2 = +0.10`  
`a` is bounded in `(-1,+1)`; collapse is `phi((m,a)) = m`.

**2) Classical (computer algebra system) calculation**
```python
# classical illustration (no external packages required)
x1, x2 = 12.4, 12.9
mean = 0.5 * (x1 + x2)
print(mean)  # 12.65

```
Classical result. 12.65

**3) SSM calculation (same magnitude + alignment lane)**

**Sum pooling rule (alignment lane)**  
`a_c := clamp(a, -1+eps, +1-eps)`  
`u := atanh(a_c)`  
`U += w * u` with `w := |m|^gamma` (default `gamma = 1`)  
`W += w`  
`a_out := tanh( U / max(W, eps) )`

**Interpretation.** Magnitude stays `12.65` (collapse parity), while the pooled `a` shows posture. With one unstable sensor, expect a moderate positive `a` indicating drift (under this POC convention). If both sensors had `a ≈ 0`, then `a_out ≈ 0` and SSM ≡ Classical.

```python

# scenario_01_two_sensors.py  (ASCII-only, top-level prints)

import math

def clamp(a, e=1e-6):
    return max(-1 + e, min(1 - e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh(a) = 0.5 * ln((1+a)/(1-a))
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs
x1 = (12.4, +0.80)
x2 = (12.9, +0.10)

# classical magnitude
m = 0.5 * (x1[0] + x2[0])

# SSM pooled alignment
a = ssm_align_weighted([(x1[1], x1[0]), (x2[1], x2[0])], gamma=1.0, eps=1e-12)

print("Classical:", f"{m:.4f}")            # 12.6500
print("SSM:", f"m={m:.4f}, a={a:+.4f}")    # a ~ +0.5296

```        
     
**What to expect.**  
`Classical: 12.65`  
`SSM: m=12.65, a≈+0.53, band=A-` (rounded; `gamma = 1`)

**5) Why this helps in the real world**
- The same headline value can be flagged for a quick re-measure instead of silently passing as “normal.”  
- Dashboards can color identical magnitudes differently using `a` or a simple band, improving trust without changing arithmetic.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
