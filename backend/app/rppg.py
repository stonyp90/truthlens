"""Tensivue — pouls à distance (rPPG) par l'algorithme POS.

Principe (Wang et al., 2017, « Algorithmic Principles of Remote PPG ») :
les variations subtiles de la couleur de la peau, invisibles à l'œil,
portent le signal du pouls. POS projette les séries RGB normalisées sur
un plan orthogonal à la direction de la peau, ce qui supprime une bonne
partie des artefacts de mouvement et d'éclairage.

Ce module prend la série des couleurs moyennes d'une région du visage
(front/joues, échantillonnée par le pipeline vidéo) et retourne :
- bpm          : fréquence cardiaque estimée
- purity       : part de la puissance spectrale concentrée au pic (0..1)
- instability  : score 0..1 — pic diffus et/ou fréquence qui dérive
                 entre la première et la seconde moitié du clip.
                 C'est CE score qui alimente la fusion (le stress fait
                 monter et varier le pouls ; le bpm seul n'est pas un
                 signal de tension interprétable sans baseline du sujet).

Limites honnêtes : exige ≥ 8 s de visage stable, ≥ 120 px de largeur de
visage, un échantillonnage ≥ 8 Hz. Compression vidéo agressive, faible
lumière et mouvements forts détruisent le signal — on retourne None
plutôt qu'un nombre inventé.
"""
from __future__ import annotations

import numpy as np

MIN_SECONDS = 8.0
MIN_SAMPLES = 48
BAND_HZ = (0.7, 3.5)  # 42 à 210 bpm


def estimate_pulse(rgb_series: list[tuple[float, float, float, float]]) -> dict | None:
    """rgb_series : liste de (t_secondes, r, g, b), t croissant."""
    if len(rgb_series) < MIN_SAMPLES:
        return None
    t = np.array([s[0] for s in rgb_series], dtype=float)
    if t[-1] - t[0] < MIN_SECONDS:
        return None
    rgb = np.array([[s[1], s[2], s[3]] for s in rgb_series], dtype=float)

    # Rééchantillonnage uniforme (la cadence réelle varie selon les frames lues).
    fs = (len(t) - 1) / (t[-1] - t[0])
    if fs < 8.0:
        return None
    grid = np.arange(t[0], t[-1], 1.0 / fs)
    cols = [np.interp(grid, t, rgb[:, c]) for c in range(3)]
    sig = np.stack(cols, axis=1)  # (n, 3) R,G,B

    bpm_full, purity = _pos_peak(sig, fs)
    if bpm_full is None:
        return None
    half = len(sig) // 2
    bpm_a, _ = _pos_peak(sig[:half], fs)
    bpm_b, _ = _pos_peak(sig[half:], fs)
    drift = 0.0
    if bpm_a is not None and bpm_b is not None:
        drift = abs(bpm_a - bpm_b)
    instability = float(np.clip(0.6 * (1.0 - purity) + 0.4 * min(1.0, drift / 25.0), 0.0, 1.0))
    return {
        "bpm": round(float(bpm_full), 1),
        "purity": round(float(purity), 3),
        "driftBpm": round(float(drift), 1),
        "instability": round(instability, 3),
    }


def _pos_peak(sig: np.ndarray, fs: float) -> tuple[float | None, float]:
    """Applique POS puis retourne (bpm au pic spectral, pureté du pic)."""
    n = len(sig)
    if n < 32:
        return None, 0.0
    mean = sig.mean(axis=0)
    if np.any(mean <= 0):
        return None, 0.0
    cn = sig / mean  # normalisation temporelle (POS)
    # Fenêtre glissante de 1,6 s (standard POS) — ici : projection globale,
    # suffisante pour une estimation de fréquence sur clip court.
    s1 = cn[:, 1] - cn[:, 2]            # G - B
    s2 = cn[:, 1] + cn[:, 2] - 2 * cn[:, 0]  # G + B - 2R
    alpha = np.std(s1) / (np.std(s2) + 1e-9)
    h = s1 + alpha * s2
    h = h - h.mean()
    h = h * np.hanning(n)
    spec = np.abs(np.fft.rfft(h)) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    band = (freqs >= BAND_HZ[0]) & (freqs <= BAND_HZ[1])
    if not np.any(band):
        return None, 0.0
    band_power = spec[band]
    total = float(band_power.sum())
    if total <= 0:
        return None, 0.0
    k = int(np.argmax(band_power))
    bpm = float(freqs[band][k] * 60.0)
    # Pureté : puissance du pic ± 1 bin sur la puissance totale de la bande.
    lo, hi = max(0, k - 1), min(len(band_power), k + 2)
    purity = float(band_power[lo:hi].sum() / total)
    return bpm, purity
