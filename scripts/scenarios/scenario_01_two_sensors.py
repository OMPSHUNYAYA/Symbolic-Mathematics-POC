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
