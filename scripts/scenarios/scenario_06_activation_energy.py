# scenario_06_activation_energy.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh: 0.5 * ln((1+a)/(1-a))
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
runA = (51.2, +0.70)
runB = (54.8, +0.15)

# classical magnitude (straight average)
m = 0.5 * (runA[0] + runB[0])

# SSM pooled alignment
a = ssm_align_weighted([(runA[1], runA[0]), (runB[1], runB[0])])

print("Classical:", f"{m:.4f}")            # 53.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}")    # a ≈ +0.4598
