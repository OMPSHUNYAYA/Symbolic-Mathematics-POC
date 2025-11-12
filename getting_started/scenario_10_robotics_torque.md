# **Getting Started — Scenario 10: Robotics — averaged torque load with hidden strain**

**Domain.** Robotics / Control Systems

**What this shows.** When multiple actuators share load, the classical average torque can look safe while one actuator is under hidden strain. SSM keeps the same torque and adds a bounded alignment `a in (-1,+1)` that reflects how stable or fragile that value is. Collapse parity holds: `phi((m,a)) = m`.

**1) Setup (inputs)**  
Torque contributions `(m, a)` for three actuators:
- **Actuator A:** `m = 12.0`, `a = +0.05` *(steady)*
- **Actuator B:** `m = 11.5`, `a = +0.03` *(steady)*
- **Actuator C:** `m = 18.0`, `a = +0.82` *(high strain)*

Notes. `a in (-1,+1)`; collapse parity `phi((m,a)) = m`.

**2) Classical result (arithmetic)**

Operation — simple mean of magnitudes.

```python
# classical illustration (no external packages required)
vals = [12.0, 11.5, 18.0]
mean = sum(vals) / len(vals)
print(mean)  # 13.833333333333334

```

**3) SSM result (same magnitude + alignment lane)**

**Magnitude under collapse.** `m = 13.8333` *(unchanged; `phi((m,a)) = m`).*

**Alignment pooling for sums (order-invariant).**
- `a_c := clamp(a, -1+eps, +1-eps)`
- `u := atanh(a_c)`
- `w := |m|^gamma` *(use `gamma = 1`)*
- `U += w * u`
- `W += w`
- `a_out := tanh( U / max(W, eps) )`

**Interpretation.** The torque average stays `13.8333`, while `a_out` rises if one actuator is strained, making instability visible without changing arithmetic.

**Numbers (rounded).**

- **Rapidities.** `u_A ≈ 0.05004173`, `u_B ≈ 0.03004502`, `u_C ≈ 1.15611952`
- **Weights.** `w_A = 12.0`, `w_B = 11.5`, `w_C = 18.0` → `W = 41.5`
- **Accumulate.** `U = 12.0*0.05004173 + 11.5*0.03004502 + 18.0*1.15611952 ≈ 21.75616985`
- **Alignment.** `a_out = tanh(U/W) = tanh(21.75616985 / 41.5) = tanh(0.524247) ≈ +0.4816`

**SSM output.** `m = 13.8333`, `a ≈ +0.4816`

**4) Tiny script (copy-paste)**

```python
# scenario_10_robotics_torque.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|**gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh in ASCII via log
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
A = (12.0, +0.05)
B = (11.5, +0.03)
C = (18.0, +0.82)

# classical magnitude (simple mean)
m = (A[0] + B[0] + C[0]) / 3.0

# SSM pooled alignment
a = ssm_align_weighted([(A[1], A[0]), (B[1], B[0]), (C[1], C[0])])

print("Classical:", f"{m:.4f}")         # 13.8333
print("SSM:", f"m={m:.4f}, a={a:+.4f}") # a ≈ +0.4816

```

**5) What to expect**

- **Classical.** `13.8333`
- **SSM.** `m=13.8333, a≈+0.4816` *(visible strain due to one actuator)*

**6) Interpretation**

- **Classical view.** “The load is ~13.8. Everything appears normal.”  
- **SSM view.** “The load is ~13.8, but load-sharing is unstable due to strain on one actuator.”  
The number is correct; the alignment gives the trust level.

**7) Real-world operational meaning**

If `a_out` crosses a policy threshold *(example: `a_out > 0.40`)*, a controller could:
- rebalance torque distribution,
- reduce acceleration or motion speed,
- schedule predictive maintenance,
- or flag the actuator for inspection.

**Bottom line.** SSM does not change how torque is calculated — it changes how torque is interpreted and trusted.

**License.** CC BY-NC 4.0 • Observation-only; not for critical use.
