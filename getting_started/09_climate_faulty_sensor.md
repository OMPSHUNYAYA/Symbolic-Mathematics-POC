# **Getting Started — Scenario 09: Climate — pooled temperature with one faulty sensor**

**Domain.** Climate / Environmental sensing

**What this shows.** One spiking sensor can distort the classical mean. SSM keeps the same magnitude *(collapse parity `phi((m,a)) = m`)* and surfaces alignment `a in (-1,+1)` to warn that the roll-up is unreliable.

**1) Inputs**  
Four simultaneous temperature readings for the same location:
- `(m1, a1) = (25.0, +0.05)`
- `(m2, a2) = (24.8, +0.02)`
- `(m3, a3) = (50.0, +0.95)` ← *suspected fault / sun-hit / calibration error*
- `(m4, a4) = (25.1, +0.04)`

Note. `a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

**2) Classical result (arithmetic)**

Operation: simple mean of magnitudes.

```python
# classical illustration (no external packages required)
vals = [25.0, 24.8, 50.0, 25.1]
mean = sum(vals) / len(vals)
print(mean)  # 31.225

```

**3) SSM result (same magnitude + alignment lane)**

**Rule for sums (alignment pooling).**
- `a_c := clamp(a, -1+eps, +1-eps)`
- `u := atanh(a_c)`
- `w := |m|^gamma` *(default `gamma = 1`)*
- `U += w * u`
- `W += w`
- `a_out := tanh( U / max(W, eps) )`

**Numbers (rounded).**
- **Rapidities.** `atanh(+0.05) ≈ 0.05004173`, `atanh(+0.02) ≈ 0.02000267`, `atanh(+0.95) ≈ 1.83178082`, `atanh(+0.04) ≈ 0.04002135`
- **Weights.** `25.0, 24.8, 50.0, 25.1` → `W = 124.9`
- **Accumulator.**  
  `U = 25.0*0.05004173 + 24.8*0.02000267 + 50.0*1.83178082 + 25.1*0.04002135 ≈ 94.34068652`
- **Average rapidity.** `t := U / W ≈ 0.75509`
- **Alignment.** `a_out = tanh(t) ≈ +0.6383`

**SSM result.** `m = 31.225` *(same as classical)*, `a ≈ +0.6383` *(strong drift warning)*

**4) Tiny script (copy-paste)**

```python
# scenario_09_climate_faulty_sensor.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|**gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh in ASCII: 0.5 * ln((1+a)/(1-a))
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
r1 = (25.0, +0.05)
r2 = (24.8, +0.02)
r3 = (50.0, +0.95)  # suspected fault / sun-hit / calibration error
r4 = (25.1, +0.04)

# classical magnitude
m = (r1[0] + r2[0] + r3[0] + r4[0]) / 4.0

# SSM pooled alignment
a = ssm_align_weighted([
    (r1[1], r1[0]),
    (r2[1], r2[0]),
    (r3[1], r3[0]),
    (r4[1], r4[0]),
])

print("Classical:", f"{m:.3f}")          # 31.225
print("SSM:", f"m={m:.3f}, a={a:+.4f}")  # a ≈ +0.6383

```

**5) What to expect.**

- **Classical.** `31.225`
- **SSM.** `m=31.225, a≈+0.6383` *(visible instability due to the spiking sensor)*

**6) Why this helps**

- **Same magnitude, extra truth.** The classical mean is preserved; alignment makes its fragility visible.
- **Immediate actionability.** Down-weight or discard the spiking sensor, re-measure, or switch to a robust estimator; use `a` (or bands) to color dashboards and trigger checks.
- **Clear agreement when calm.** If all sensors were ~25 with small `a`, then `a_out ≈ 0` and SSM ≡ Classical in both value and posture.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
