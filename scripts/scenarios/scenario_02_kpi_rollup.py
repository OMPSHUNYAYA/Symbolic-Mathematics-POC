# scenario_02_kpi_rollup.py
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
