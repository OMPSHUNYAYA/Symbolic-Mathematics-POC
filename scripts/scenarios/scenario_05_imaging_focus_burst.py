# scenario_05_imaging_focus_burst.py
import math

def clamp(a, e=1e-6):
    return max(-1+e, min(1-e, float(a)))

def ssm_align_weighted(pairs, gamma=1.0, eps=1e-12):
    # pairs: iterable of (a_raw, m); weight w := |m|^gamma
    U, W = 0.0, 0.0
    for a_raw, m in pairs:
        a = clamp(a_raw)
        u = 0.5 * math.log((1.0 + a) / (1.0 - a))  # atanh
        w = abs(float(m)) ** gamma
        U += w * u
        W += w
    return math.tanh(U / max(W, eps))

# inputs (m, a) per frame
frames = [
    (82.0, +0.10),
    (85.0, +0.10),
    (79.0, +0.10),
    (60.0, +0.85),  # blur burst
    (84.0, +0.10),
]

# classical magnitude (mean of m)
m = sum(f[0] for f in frames) / len(frames)

# SSM pooled alignment
a = ssm_align_weighted([(a, m_i) for (m_i, a) in frames])

print("Classical:", f"{m:.4f}")                  # 78.0000
print("SSM:", f"m={m:.4f}, a={a:+.4f}")          # a ≈ +0.2712
