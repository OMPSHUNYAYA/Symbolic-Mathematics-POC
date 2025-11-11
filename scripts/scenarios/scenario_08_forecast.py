# scenario_08_forecast.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        # atanh without external libs
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a)
model_A = (100.0, +0.75)
model_B = ( 96.0, +0.15)
model_C = (104.0, +0.10)

# classical magnitude
m = (model_A[0] + model_B[0] + model_C[0]) / 3.0

# SSM pooled alignment
a = ssm_align_weighted([
    (model_A[1], model_A[0]),
    (model_B[1], model_B[0]),
    (model_C[1], model_C[0]),
])

print("Classical:", f"{m:.4f}")            # 100.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}")    # a ≈ +0.3863
