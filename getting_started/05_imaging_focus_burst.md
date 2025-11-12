# **Getting Started — Scenario 05: Imaging — Focus series with a brief blur burst**

**Domain.** Imaging / Video focus

**What this shows.** The classical average can look acceptable while a short blur burst slips through. SSM keeps the same magnitude and adds alignment `a` so the burst is visible without changing the arithmetic.

**1) Setup (inputs)**  
Per frame `(m, a)`:
- **Frame 1:** `m=82, a=+0.10`  
- **Frame 2:** `m=85, a=+0.10`  
- **Frame 3:** `m=79, a=+0.10`  
- **Frame 4:** `m=60, a=+0.85` *(blur burst)*  
- **Frame 5:** `m=84, a=+0.10`

`a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

**2) Classical result (computer-algebra arithmetic)**

Mean focus: `(82 + 85 + 79 + 60 + 84) / 5 = 390 / 5 = 78.0`  
**Classical result.** `m = 78.0` *(looks fine; the blur burst is hidden).*

```python
# classical mean only (no external packages)
vals = [82, 85, 79, 60, 84]
mean = sum(vals) / len(vals)
print(mean)  # 78.0

```

**3) SSM calculation (same magnitude + alignment lane)**

**Magnitude under collapse.** `m = 78.0` *(unchanged; collapse parity `phi((m,a)) = m`).*

**Alignment pooling (sum rule).**
- `a_c := clamp(a, -1+eps, +1-eps)`
- `u := atanh(a_c)`
- `U += w * u` with `w := |m|^gamma` *(default `gamma = 1`)*
- `W += w`
- `a_out := tanh( U / max(W, eps) )`

**Interpretation.** Magnitude remains `78.0` while `a_out` lifts above zero if any frame is unstable, exposing the brief blur burst without changing the arithmetic.

**Numbers.**

- **Weights.** `w = |m|` → `W = 82 + 85 + 79 + 60 + 84 = 390`
- **Rapidities.** `atanh(0.10) ≈ 0.100335`, `atanh(0.85) ≈ 1.256153`
- **Accumulator `U` (rounded).**  
  `82*0.100335 + 85*0.100335 + 79*0.100335 + 60*1.256153 + 84*0.100335`  
  `≈ 8.226 + 8.528 + 7.926 + 75.369 + 8.427 ≈ 108.480`
- **Average rapidity.** `U/W ≈ 108.480 / 390 ≈ 0.278153`
- **Alignment.** `a_out = tanh(0.278153) ≈ +0.2712`

**SSM result.** `m = 78.0, a ≈ +0.2712`

**4) Tiny script (copy-paste)**

```python
# scenario_05_imaging_focus_burst.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))  # atanh
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a) per frame
frames = [
    (82.0, +0.10),
    (85.0, +0.10),
    (79.0, +0.10),
    (60.0, +0.85),  # blur burst
    (84.0, +0.10),
]

# classical magnitude (mean of m)
m = sum(f[0] for f in frames) / len(frames)

# SSM pooled alignment
a = ssm_align_weighted([(a, m_i) for (m_i, a) in frames])

print("Classical:", f"{m:.4f}")         # 78.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}") # a ≈ +0.2712

```

**5) What to expect.**

- **Classical.** `78.0`
- **SSM.** `m=78.0, a≈+0.2712` *(rounded; `gamma=1`)*

**6) Why this helps**

- **Agreement when calm.** If all frames had `a ≈ 0`, then `a_out ≈ 0` and SSM ≡ Classical (`m = 78.0, a ≈ 0`).
- **Clarity when drifting.** A single blur burst lifts `a_out` to `≈ +0.27`, guiding downstream logic to re-check focus, gate sharpness-dependent features, or annotate for review.

**Bottom line.** Same arithmetic for magnitude; SSM adds a small, bounded posture signal that catches the momentary blur the classical mean ignores.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
