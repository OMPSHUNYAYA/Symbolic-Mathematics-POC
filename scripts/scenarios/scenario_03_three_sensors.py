# scenario_03_three_sensors.py
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
