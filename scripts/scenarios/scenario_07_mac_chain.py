# scenario_07_mac_chain.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def atanh(x):
    x = clamp(x)
    return 0.5 * math.log((1.0 + x) / (1.0 - x))

def a_prod(a_w, a_x):
    # product alignment: a⊗ = tanh(atanh(a_w) + atanh(a_x))
    return math.tanh(atanh(a_w) + atanh(a_x))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, magnitude_m); weight w := |m|^gamma
    U = 0.0
    W = 0.0
    for a_raw, m in pairs:
        u = atanh(a_raw)
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs
w = [(0.5,  +0.20), (-1.2, +0.10), (0.8,  +0.60)]
x = [(2.0,  +0.30), (-1.0, +0.70), (1.5,  -0.10)]

# classical products and total
p = []
for (mw, aw), (mx, ax) in zip(w, x):
    p.append((mw * mx, a_prod(aw, ax)))  # (m_prod, a_prod)

total_m = sum(m for m, _ in p)

# pool alignment across the three products using their magnitudes as weights
a = ssm_align_weighted([(a_p, abs(m_p)) for (m_p, a_p) in p])

print("Classical:", f"{total_m:.4f}")              # 3.4000
print("SSM:", f"m={total_m:.4f}, a={a:+.4f}")      # a ≈ +0.6050
