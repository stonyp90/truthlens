"""TruthLens — moteur de fusion de signaux (backend, miroir de scoring.js).

IMPORTANT : aucun signal ne prouve un mensonge. Ce module produit un
INDICE DE TENSION / INCONGRUENCE (0-100), pas une probabilité de mensonge.
Voir docs/SCIENCE_AND_LIMITS.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Optional

DEFAULT_WEIGHTS = {
    "blinkDeviation": 0.18,
    "gazeAversion": 0.16,
    "headMovement": 0.16,
    "repetitiveMovement": 0.14,
    "facialTension": 0.20,
    "freeze": 0.16,
    "pulseInstability": 0.12,  # rPPG : pic spectral diffus / pouls qui dérive
}

DEFAULT_THRESHOLD = 55  # indice >= seuil -> prédiction « tension élevée »


def _load_weights() -> tuple[dict, int]:
    """Poids effectifs : packages/weights.json (écrit par tools/selftune.py
    quand la boucle d'auto-amélioration trouve mieux sur données étiquetées),
    sinon les défauts ci-dessus."""
    try:
        data = json.loads((Path(__file__).parent / "weights.json").read_text(encoding="utf-8"))
        weights = {**DEFAULT_WEIGHTS, **(data.get("weights") or {})}
        return weights, int(data.get("threshold", DEFAULT_THRESHOLD))
    except Exception:
        return dict(DEFAULT_WEIGHTS), DEFAULT_THRESHOLD


WEIGHTS, THRESHOLD = _load_weights()


def _clamp01(x: float) -> float:
    return min(1.0, max(0.0, x))


def blink_deviation_score(blinks_per_min: float, baseline_per_min: float = 17.0) -> float:
    return _clamp01(abs(blinks_per_min - baseline_per_min) / baseline_per_min)


def repetition_score(motion_series: list[float]) -> Optional[float]:
    if len(motion_series) < 16:
        return None
    mean = sum(motion_series) / len(motion_series)
    centered = [v - mean for v in motion_series]
    energy = sum(v * v for v in centered)
    if energy == 0:
        return 0.0
    best = 0.0
    for lag in range(2, len(motion_series) // 2 + 1):
        s = sum(centered[i] * centered[i + lag] for i in range(len(centered) - lag))
        best = max(best, s / energy)
    return _clamp01(best)


def freeze_score(motion_series: list[float], window: int = 10) -> Optional[float]:
    if len(motion_series) < window * 2:
        return None
    recent = motion_series[-window:]
    before = motion_series[-window * 2 : -window]
    b = sum(before) / len(before)
    if b == 0:
        return 0.0
    return _clamp01(1 - (sum(recent) / len(recent)) / b)


def fuse_signals(signals: dict[str, Optional[float]], coverage: dict | None = None) -> dict:
    coverage = coverage or {}
    weighted = 0.0
    total = 0.0
    used: dict[str, int] = {}
    for key, weight in WEIGHTS.items():
        v = signals.get(key)
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        weighted += weight * _clamp01(float(v))
        total += weight
        used[key] = round(_clamp01(float(v)) * 100)
    if total == 0:
        return {"index": None, "confidence": 0.0, "signals": used}

    raw = weighted / total
    index = round(5 + raw * 90)  # jamais 0 ni 100 affichés
    face_ratio = coverage.get("faceVisibleRatio", 0.0)
    duration = coverage.get("durationSec", 0.0)
    confidence = _clamp01(0.45 * face_ratio + 0.25 * min(1.0, duration / 60.0) + 0.30 * total)
    return {
        "index": index,
        "confidence": round(confidence, 2),
        "signals": used,
        "disclaimer": "Indice de tension/incongruence observable — pas une preuve de mensonge.",
    }
