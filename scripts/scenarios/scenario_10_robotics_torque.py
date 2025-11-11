# scenario_10_robotics_torque.py
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
A = (12.0, +0.05)
B = (11.5, +0.03)
C = (18.0, +0.82)

# classical magnitude (simple mean)
m = (A[0] + B[0] + C[0]) / 3.0

# SSM pooled alignment
a = ssm_align_weighted([(A[1], A[0]), (B[1], B[0]), (C[1], C[0])])

print("Classical:", f"{m:.4f}")             # 13.8333
print("SSM:", f"m={m:.4f}, a={a:+.4f}")     # a ≈ +0.4816
