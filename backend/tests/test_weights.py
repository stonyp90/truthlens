"""Tests des poids externalisés (packages/weights.json)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))
import scoring  # noqa: E402


def test_weights_loaded_with_pulse():
    assert "pulseInstability" in scoring.WEIGHTS
    assert scoring.WEIGHTS["pulseInstability"] > 0
    assert 5 <= scoring.THRESHOLD <= 95


def test_pulse_contributes_to_index():
    calm = scoring.fuse_signals(
        {"headMovement": 0.4, "pulseInstability": 0.0},
        {"faceVisibleRatio": 0.9, "durationSec": 30},
    )
    tense = scoring.fuse_signals(
        {"headMovement": 0.4, "pulseInstability": 1.0},
        {"faceVisibleRatio": 0.9, "durationSec": 30},
    )
    assert tense["index"] > calm["index"]
    assert tense["signals"]["pulseInstability"] == 100
