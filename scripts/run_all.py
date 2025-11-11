# run_all.py
# Purpose: run every scenario script in ./scenarios and append a simple band next to "a".
# Policy: bands are display-only; they do not change m or a or any formulas.
# Semantics: drift-positive display (bigger |a| => worse band), thresholds are tunable.

import importlib.util
import pathlib
import sys
import traceback

# ---------- Tunable band policy ----------
# Three bands: A+ (calm), A0 (noticeable), A- (hot)
# Use absolute(a) thresholds so both positive/negative excursions are treated symmetrically.
T1 = 0.20  # <= 0.20 => A+
T2 = 0.40  # (0.20, 0.40] => A0 ; > 0.40 => A-
def band_of(a: float) -> str:
    aa = abs(float(a))
    if aa <= T1:
        return "A+"
    elif aa <= T2:
        return "A0"
    else:
        return "A-"
# ----------------------------------------

SCEN_DIR = pathlib.Path(__file__).resolve().parents[1] / "scenarios"

def run_scenario(pyfile: pathlib.Path):
    # Import the scenario as a module, letting it print its own lines.
    spec = importlib.util.spec_from_file_location(pyfile.stem, str(pyfile))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # scenario prints "Classical: ..." and "SSM: m=..., a=..."
    except Exception:
        traceback.print_exc()
        return None

    # Try to read m and a from the module namespace to append a band.
    m = getattr(mod, "m", None)
    a = getattr(mod, "a", None)
    if a is None:
        return None

    return {"file": pyfile.name, "m": m, "a": float(a), "band": band_of(a)}

def main():
    print("Running scenarios...\n")
    if not SCEN_DIR.exists():
        print("Could not find 'scenarios' folder.")
        sys.exit(1)

    pyfiles = sorted(SCEN_DIR.glob("*.py"))
    for f in pyfiles:
        print(f"\n--- {f.name} ---")
        summary = run_scenario(f)
        if summary is None:
            continue
        # Append a compact band line for quick triage
        m = summary["m"]
        a = summary["a"]
        band = summary["band"]
        if m is not None:
            print(f"[runner] summary: m={m:.4f}, a={a:+.4f} [{band}]")
        else:
            print(f"[runner] summary: a={a:+.4f} [{band}]")

    print("\nAll scenarios completed.")

if __name__ == "__main__":
    main()
