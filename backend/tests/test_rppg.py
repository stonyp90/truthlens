"""Tests rPPG : un pouls synthétique connu doit être retrouvé."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.rppg import estimate_pulse  # noqa: E402


def _synthetic_series(bpm: float, seconds: float = 20.0, fs: float = 15.0, drift_to: float | None = None):
    series = []
    n = int(seconds * fs)
    for i in range(n):
        t = i / fs
        f = bpm / 60.0
        if drift_to:
            frac = t / seconds
            f = (bpm + (drift_to - bpm) * frac) / 60.0
        phase = 2 * math.pi * f * t
        # Le canal vert porte le pouls le plus fort (absorption hémoglobine).
        g = 120 + 3.0 * math.sin(phase)
        r = 150 + 1.2 * math.sin(phase + 0.4)
        b = 100 + 0.8 * math.sin(phase - 0.3)
        series.append((t, r, g, b))
    return series


def test_recovers_known_pulse():
    res = estimate_pulse(_synthetic_series(72.0))
    assert res is not None
    assert abs(res["bpm"] - 72.0) <= 6.0
    assert res["purity"] > 0.5
    assert res["instability"] < 0.45


def test_drifting_pulse_is_less_stable():
    stable = estimate_pulse(_synthetic_series(70.0))
    drifting = estimate_pulse(_synthetic_series(70.0, drift_to=110.0))
    assert stable is not None and drifting is not None
    assert drifting["instability"] > stable["instability"]


def test_too_short_returns_none():
    assert estimate_pulse(_synthetic_series(72.0, seconds=4.0)) is None
    assert estimate_pulse([]) is None
