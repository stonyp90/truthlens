"""TruthLens — porte qualité et adaptation de flux (miroir de quality.js).

Règle : si les pixels ne sont pas là, on ne peut pas savoir — l'engine
refuse ou dégrade honnêtement plutôt que d'inventer un score.
"""
from __future__ import annotations

SIGNAL_REQUIREMENTS = {
    "headMovement": {"faceWidthPx": 60, "fps": 10, "label": "Mouvements de tête"},
    "repetitiveMovement": {"faceWidthPx": 60, "fps": 15, "label": "Tics / mouvements répétitifs"},
    "freeze": {"faceWidthPx": 40, "fps": 10, "label": "Figement"},
    "blinkDeviation": {"faceWidthPx": 90, "fps": 15, "label": "Clignements (EAR)"},
    "facialTension": {"faceWidthPx": 110, "fps": 15, "label": "Tension faciale (blendshapes / AU)"},
    "gazeAversion": {"faceWidthPx": 140, "fps": 15, "label": "Regard / iris"},
    "pupil": {"faceWidthPx": 220, "fps": 15, "label": "Dilatation pupillaire"},
    "sweatSpecular": {"faceWidthPx": 160, "fps": 10, "label": "Sueur — brillance spéculaire"},
    "skinColor": {"faceWidthPx": 120, "fps": 20, "label": "Rougeur / pâleur (chrominance peau)"},
    "rppg": {"faceWidthPx": 120, "fps": 20, "label": "Fréquence cardiaque à distance (rPPG)"},
    "swallowing": {"faceWidthPx": 130, "fps": 15, "label": "Déglutition"},
    "microExpression": {"faceWidthPx": 200, "fps": 60, "label": "Micro-expressions"},
}


def assess_quality(inp: dict) -> dict:
    face = inp.get("faceWidthPx", 0) or 0
    fps = inp.get("fps", 0) or 0
    sharpness = inp.get("sharpness", 1)
    luminance = inp.get("luminance", 128)
    is_color = inp.get("isColor", True)

    enabled, disabled = [], []
    for key, req in SIGNAL_REQUIREMENTS.items():
        reasons = []
        if face < req["faceWidthPx"]:
            reasons.append(f"visage {face}px < {req['faceWidthPx']}px requis")
        if fps < req["fps"]:
            reasons.append(f"{fps} ips < {req['fps']} ips requises")
        if key in ("sweatSpecular", "skinColor", "rppg") and not is_color:
            reasons.append("vidéo couleur requise")
        if key in ("sweatSpecular", "skinColor") and (luminance < 40 or luminance > 225):
            reasons.append("éclairage hors plage (sous/surexposé)")
        if key in ("gazeAversion", "pupil") and sharpness < 0.4:
            reasons.append("image trop floue")
        (disabled if reasons else enabled).append(
            {"signal": key, "label": req["label"], **({"reasons": reasons} if reasons else {})}
        )

    tier = "insufficient"
    if face >= 200 and fps >= 30:
        tier = "excellent"
    elif face >= 130 and fps >= 20:
        tier = "good"
    elif face >= 80 and fps >= 15:
        tier = "basic"

    return {
        "tier": tier,
        "canScore": tier != "insufficient",
        "verdict": (
            "Qualité insuffisante : on ne peut pas savoir. Augmente la résolution, "
            "rapproche le visage ou améliore l'éclairage."
            if tier == "insufficient"
            else None
        ),
        "enabledSignals": enabled,
        "disabledSignals": disabled,
        "input": {"faceWidthPx": face, "fps": fps, "sharpness": sharpness,
                  "luminance": luminance, "isColor": is_color},
    }


def adapt_stream(profile: dict) -> dict:
    kind = str(profile.get("kind", "")).lower()
    plan = {"kind": kind, "ingest": None, "adaptations": [], "notes": []}
    if kind in ("mp4", "webm"):
        plan["ingest"] = "browser-native"
        plan["notes"].append("Fichier lu par le navigateur : analyse locale directe.")
    elif kind in ("webcam", "webrtc"):
        plan["ingest"] = "browser-native"
        plan["notes"].append("Flux vivant du navigateur : MediaPipe en temps réel.")
    elif kind == "hls":
        plan["ingest"] = "browser-or-server"
        plan["notes"].append("HLS : navigateur si décodable, sinon relais serveur ffmpeg.")
    elif kind in ("youtube", "vimeo"):
        plan["ingest"] = "browser-overlay"
        plan["notes"].append("Calque sur le <video>; pixels protégés (CORS) = mode métadonnées + ingestion serveur.")
    elif kind in ("srt", "rtmp"):
        plan["ingest"] = "server-relay"
        plan["adaptations"].append("ffmpeg : extraction 2-10 ips, échelle adaptée au visage")
        plan["notes"].append("SRT/RTMP non lisible par un navigateur : relais serveur obligatoire (Pro).")
    else:
        plan["ingest"] = "unknown"
        plan["notes"].append("Flux non reconnu : MP4/WebM, URL HLS ou flux SRT attendu.")
    if (profile.get("fps") or 30) > 30:
        plan["adaptations"].append("Sous-échantillonnage 30 ips (signaux lents); pleine cadence si micro-expressions (≥60 ips).")
    if (profile.get("width") or 1920) < 640:
        plan["adaptations"].append("Résolution faible : signaux fins désactivés par la porte qualité.")
    return plan
