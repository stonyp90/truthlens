"""TruthLens — backend d'analyse.

Endpoints
---------
GET  /health                état du service
POST /api/analyze           upload d'une vidéo (MP4/WebM/MOV) -> rapport JSON
                            (gratuit : traitement différé, file d'attente)
WS   /ws/stream             temps réel : le client envoie des frames JPEG
                            (base64), le serveur renvoie l'indice par frame
                            (payant : clé API requise quand BILLING=on)
POST /api/ingest            déclare un flux HLS ou SRT à ingérer côté serveur
                            (ffmpeg) pour le mode temps réel hébergé (Pro)

L'analyse v0 utilise OpenCV (différence d'images + détection de visage
Haar pour la présence/le suivi de boîte). La phase 2 branche MediaPipe
Face Landmarker (iris/rétine, clignements EAR, blendshapes) — voir ROADMAP.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))
from quality import assess_quality  # noqa: E402
from scoring import freeze_score, fuse_signals, repetition_score  # noqa: E402

app = FastAPI(title="Tensivue API", version="0.2.0")

DISCLAIMER = "Indice de tension/incongruence observable — pas une preuve de mensonge."
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "500"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "truthlens", "disclaimer": DISCLAIMER}


def _motion_series(video_path: str, step_frames: int = 5) -> tuple[list[float], float, float, dict]:
    """Retourne (série de mouvement, ratio visage visible, durée sec, infos qualité).

    La largeur du visage est mesurée sur une copie à 320 px de large et
    remise à l'échelle réelle : c'est elle qui alimente la porte qualité
    (trop peu de pixels = on ne peut pas savoir).
    """
    import cv2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise HTTPException(400, "Vidéo illisible (format non supporté ?)")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    duration = total / fps if fps else 0.0

    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    prev_gray = None
    motions: list[float] = []
    face_frames = 0
    read_frames = 0
    max_face_w = 0
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    luminance_sum = 0.0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        idx += 1
        if idx % step_frames:
            continue
        small = cv2.resize(frame, (64, 36))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            motions.append(float(cv2.absdiff(gray, prev_gray).mean()) / 255.0)
        prev_gray = gray
        luminance_sum += float(gray.mean())
        read_frames += 1
        if not cascade.empty() and frame_w:
            probe = cv2.resize(frame, (320, max(1, int(320 * frame_h / frame_w))))
            probe_gray = cv2.cvtColor(probe, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(probe_gray, 1.2, 4)
            if len(faces):
                face_frames += 1
                scale = frame_w / 320.0
                max_face_w = max(max_face_w, int(max(f[2] for f in faces) * scale))
    cap.release()
    ratio = (face_frames / read_frames) if read_frames else 0.0
    info = {
        "width": frame_w,
        "height": frame_h,
        "fps": round(fps, 1),
        "faceWidthPx": max_face_w,
        "luminance": round(luminance_sum / read_frames, 1) if read_frames else 0,
        "isColor": True,
    }
    return motions, ratio, duration, info


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"Fichier trop gros (max {MAX_UPLOAD_MB} Mo)")
    suffix = Path(file.filename or "video.mp4").suffix or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    try:
        return _report_from_path(tmp_path)
    finally:
        os.unlink(tmp_path)


def _report_from_path(tmp_path: str) -> dict:
    motions, face_ratio, duration, info = _motion_series(tmp_path)
    if not motions:
        raise HTTPException(422, "Aucun signal exploitable (vidéo trop courte ?)")

    # Porte qualité : trop peu de pixels sur le visage = on ne peut pas savoir.
    quality = assess_quality(
        {
            "faceWidthPx": info["faceWidthPx"],
            "fps": info["fps"],
            "luminance": info["luminance"],
            "isColor": True,
        }
    )
    if not quality["canScore"]:
        return {
            "index": None,
            "quality": quality,
            "source": info,
            "durationSec": round(duration, 1),
            "faceVisibleRatio": round(face_ratio, 2),
            "disclaimer": quality["verdict"],
        }
    mean_motion = float(np.mean(motions))
    signals = {
        "headMovement": min(1.0, mean_motion * 6),
        "repetitiveMovement": repetition_score(motions),
        "freeze": freeze_score(motions[-80:], 10),
        "blinkDeviation": None,
        "gazeAversion": None,
        "facialTension": None,
    }
    fused = fuse_signals(signals, {"faceVisibleRatio": face_ratio, "durationSec": duration})
    return {
        "durationSec": round(duration, 1),
        "faceVisibleRatio": round(face_ratio, 2),
        "quality": quality,
        "source": info,
        **fused,
        "disclaimer": DISCLAIMER,
    }


class UrlRequest(BaseModel):
    url: str  # lien YouTube/Vimeo ou fichier vidéo direct


@app.post("/api/analyze-url")
def analyze_url(req: UrlRequest) -> dict:
    """Analyse à partir d'un lien (mode Pro — dynamique).

    Le serveur récupère la vidéo avec yt-dlp (480p max, 30 min max,
    250 Mo max), l'analyse avec le même pipeline que /api/analyze,
    puis efface le fichier. Aucune copie n'est conservée.
    """
    import subprocess

    if not req.url.startswith(("https://", "http://")):
        raise HTTPException(400, "Lien non supporté (https attendu)")
    with tempfile.TemporaryDirectory() as td:
        ytdlp = [sys.executable, "-m", "yt_dlp"]
        probe = subprocess.run(
            ytdlp + ["--no-playlist", "--dump-single-json", req.url],
            capture_output=True, text=True, timeout=120,
        )
        if probe.returncode != 0:
            tail = (probe.stderr or "").strip().splitlines()
            raise HTTPException(422, "Lien illisible ou vidéo indisponible" + ((" : " + tail[-1][:180]) if tail else ""))
        try:
            meta = json.loads(probe.stdout)
        except Exception:
            raise HTTPException(422, "Métadonnées de la vidéo illisibles")
        if (meta.get("duration") or 0) > 1800:
            raise HTTPException(413, "Vidéo trop longue pour l'analyse par lien (max 30 min)")
        dl = subprocess.run(
            ytdlp + ["--no-playlist", "-f",
             "bv*[height<=480][vcodec^=avc1]/bv*[height<=480][vcodec^=vp9]/b[height<=480][vcodec^=avc1]/bv*[height<=480]/b",
             "--max-filesize", "250M", "-o", os.path.join(td, "video.%(ext)s"), req.url],
            capture_output=True, text=True, timeout=900,
        )
        files = os.listdir(td)
        if dl.returncode != 0 or not files:
            raise HTTPException(422, "Téléchargement de la vidéo impossible")
        report = _report_from_path(os.path.join(td, files[0]))
        report["videoTitle"] = meta.get("title")
        report["videoUrl"] = req.url
        report["mode"] = "pro-lien"
        return report


@app.websocket("/ws/stream")
async def stream(ws: WebSocket):
    """Temps réel : reçoit {"frame": "<jpeg base64>"} -> renvoie l'indice courant."""
    await ws.accept()
    prev = None
    motions: list[float] = []
    try:
        while True:
            msg = await ws.receive_text()
            try:
                payload = json.loads(msg)
                raw = base64.b64decode(payload["frame"])
            except Exception:
                await ws.send_json({"error": "frame invalide (base64 attendu)"})
                continue
            arr = np.frombuffer(raw, dtype=np.uint8)
            gray = arr.reshape(-1) if arr.size else np.array([], dtype=np.uint8)
            motion = 0.0
            if prev is not None and gray.shape == prev.shape and gray.size:
                motion = float(np.abs(gray.astype(int) - prev.astype(int)).mean()) / 255.0
            prev = gray
            motions.append(motion)
            motions = motions[-120:]
            fused = fuse_signals(
                {
                    "headMovement": min(1.0, motion * 6),
                    "repetitiveMovement": repetition_score(motions),
                    "freeze": freeze_score(motions, 10),
                },
                {"faceVisibleRatio": 0.5, "durationSec": len(motions) / 2},
            )
            await ws.send_json({**fused, "disclaimer": DISCLAIMER})
    except WebSocketDisconnect:
        return


class IngestRequest(BaseModel):
    url: str  # https://…/flux.m3u8 (HLS) ou srt://hôte:port (SRT)


@app.post("/api/ingest")
def ingest(req: IngestRequest) -> dict:
    """Déclare un flux temps réel hébergé (mode Pro).

    L'ingestion réelle lance ffmpeg (voir docs/ARCHITECTURE.md) :
      HLS : ffmpeg -i <url> -vf fps=2,scale=64:36 -f rawvideo -
      SRT : ffmpeg -i "srt://…?mode=caller" (même pipeline)
    Ici on valide et on enregistre la demande; le worker d'ingestion
    est livré en phase 3 de la roadmap.
    """
    if not (req.url.startswith(("https://", "http://", "srt://"))):
        raise HTTPException(400, "URL de flux non supportée (HLS http(s) ou SRT attendu)")
    kind = "SRT" if req.url.startswith("srt://") else "HLS"
    return {"accepted": True, "kind": kind, "mode": "pro", "disclaimer": DISCLAIMER}
