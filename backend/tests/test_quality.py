import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))
from quality import adapt_stream, assess_quality


def test_insufficient_pixels_refuses():
    q = assess_quality({"faceWidthPx": 50, "fps": 30})
    assert q["tier"] == "insufficient" and q["canScore"] is False
    assert "on ne peut pas savoir" in q["verdict"]


def test_microexpression_needs_60fps():
    q = assess_quality({"faceWidthPx": 300, "fps": 30})
    assert any(s["signal"] == "microExpression" for s in q["disabledSignals"])
    q60 = assess_quality({"faceWidthPx": 300, "fps": 60})
    assert any(s["signal"] == "microExpression" for s in q60["enabledSignals"])


def test_srt_needs_server_relay():
    assert adapt_stream({"kind": "srt"})["ingest"] == "server-relay"
    assert adapt_stream({"kind": "mp4"})["ingest"] == "browser-native"
