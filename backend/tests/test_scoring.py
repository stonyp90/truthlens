import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))
from scoring import blink_deviation_score, freeze_score, fuse_signals, repetition_score


def test_blink_baseline_is_zero():
    assert blink_deviation_score(17) == 0.0
    assert blink_deviation_score(34) == 1.0


def test_fuse_never_extreme_and_has_disclaimer():
    out = fuse_signals({"headMovement": 1.0, "facialTension": 1.0}, {"faceVisibleRatio": 1, "durationSec": 120})
    assert 5 <= out["index"] <= 95
    assert "pas une preuve" in out["disclaimer"]


def test_fuse_no_signal():
    out = fuse_signals({}, {})
    assert out["index"] is None and out["confidence"] == 0.0


def test_repetition_detects_periodic():
    series = [0, 1, 0, 1] * 16
    assert repetition_score(series) > 0.5


def test_freeze_detects_drop():
    series = [1.0] * 30 + [0.0] * 10
    assert freeze_score(series, 10) == 1.0
