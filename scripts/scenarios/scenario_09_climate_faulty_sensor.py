# scenario_09_climate_faulty_sensor.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh in ASCII
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
r1 = (25.0, +0.05)
r2 = (24.8, +0.02)
r3 = (50.0, +0.95)  # suspected fault
r4 = (25.1, +0.04)

# classical magnitude
m = (r1[0] + r2[0] + r3[0] + r4[0]) / 4.0

# SSM pooled alignment
a = ssm_align_weighted([(r1[1], r1[0]), (r2[1], r2[0]), (r3[1], r3[0]), (r4[1], r4[0])])

print("Classical:", f"{m:.3f}")                 # 31.225
print("SSM:", f"m={m:.3f}, a={a:+.4f}")         # a ≈ +0.6383
