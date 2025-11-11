# Getting Started — Scenario 01: Two Sensors (Devices)

**Domain:** Devices / Instrumentation  
**Goal:** Show how two sensors can report the same approximate value (`m`) while having very different levels of stability (`a`).  
Classical arithmetic will average the values and hide the fragility; **SSM** adds posture via the alignment lane `a` in `(-1,+1)`.

**POC display policy:** For readability in this Proof of Concept, **higher printed `a` means more drift** (`a_semantics = "drift-positive"`).  
This is only a display choice. You can flip the meaning of `a` without changing the math or `phi((m,a)) = m`.

---

## 1) Setup (inputs)

Two thermometers read the same beaker; one is steady, one is slightly noisy.

x1 = 12.4, a1 = +0.80
x2 = 12.9, a2 = +0.10

- m is the magnitude (the value you're already used to).
- a is the posture lane in (-1,+1), describing how stable that reading is.
- Collapse parity: phi((m,a)) = m ensures classical results are always preserved.

---

## 2) Classical calculation (unchanged by design)

# classical illustration (no external packages required)
x1, x2 = 12.4, 12.9
mean = 0.5 * (x1 + x2)
print(mean)  # 12.65

Classical result: 12.65

The average looks normal — but we still don't know if the readings are steady or if one is wobbling. 

## 3) SSM calculation (same magnitude + alignment lane)

**Sum pooling rule (alignment lane):**
a_c := clamp(a, -1+eps, +1-eps)
u   := 0.5 * ln((1+a_c)/(1-a_c))       # atanh(a_c)
w   := |m|^gamma                       # default gamma = 1
U   := SUM(w * u)                      # accumulate over items
W   := SUM(w)
a_out := tanh( U / max(W, eps) )

**Interpretation.**
- Magnitude stays the same by collapse parity: phi((m,a)) = m, so m = 12.65 here.
- With one unstable sensor, expect a moderate positive a_out indicating drift (under this POC’s "drift-positive" display).
- If both sensors had a ≈ 0 (calm), then a_out ≈ 0 and SSM ≡ Classical.

## 4) Tiny script (copy-paste)

# ASCII-only; top-level prints
import math

def clamp(a, e=1e-6):
    return max(-1 + e, min(1 - e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh(a) := 0.5 * ln((1+a)/(1-a))
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs
x1 = (12.4, +0.80)
x2 = (12.9, +0.10)

# classical magnitude (unchanged by design: phi((m,a)) = m)
m = 0.5 * (x1[0] + x2[0])

# SSM pooled alignment (sum pooling on the lane)
a = ssm_align_weighted([(x1[1], x1[0]), (x2[1], x2[0])], gamma=1.0, eps=1e-12)

print("Classical:", f"{m:.4f}")            # 12.6500
print("SSM:", f"m={m:.4f}, a={a:+.4f}")    # a ~ +0.5296

## What to expect
# Classical: 12.65
# SSM: m=12.65, a≈+0.53, band=A-   (rounded; gamma=1)

## 5) Why this helps in the real world

• The same headline value can be flagged for a quick re-measure instead of silently passing as "normal".  
• Dashboards can color identical magnitudes differently using `a` or a simple band, improving trust **without changing arithmetic**.

## 6) Run it (one line) and expected output

# From the folder containing the file:
python scenario_01_two_sensors.py

# Expected prints (rounded):
Classical: 12.6500
SSM: m=12.6500, a=+0.5296    # band ≈ A-

---

## Bands (display policy for this POC)

# Thresholds used for quick reading (can be flipped without changing the math):
A++ : a >= +0.90
A+  : +0.60 <= a < +0.90
A0  : -0.60 < a < +0.60
A-  : -0.90 < a <= -0.60
A-- : a <= -0.90

# Note: Canonical SSM treats +a as stability and -a as drift; this POC uses a "drift-positive" display for readability.

---

## Safety & license (one screen)

# Observation-only. Not for operational or safety-critical use.
# Reproducible and plain-ASCII; parameters are declared in one place.
# License: CC BY-NC 4.0 (non-commercial, with attribution).
