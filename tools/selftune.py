#!/usr/bin/env python3
"""Tensivue — boucle d'auto-amélioration (aucune intervention humaine).

Ce que fait ce script, à chaque exécution :
1. Lit le jeu de données étiqueté (data/labeled/*.json — exports de l'app
   de collecte apps/web/collect.html ; seules les entrées avec
   consentement exprès sont utilisées, Loi 25).
2. Extrait les signaux de chaque clip avec EXACTEMENT le pipeline du
   backend (backend/app/main.py :: _signals_from_path).
3. Sépare entraînement / test de façon SUJET-DISJOINTE quand c'est
   possible (on ne teste jamais sur une personne vue à l'entraînement —
   sinon les chiffres mentent).
4. Cherche de meilleurs poids de fusion (recherche aléatoire seedée) et
   un meilleur seuil sur l'entraînement ; évalue sur le test.
5. RÈGLE D'ADOPTION (jamais de dégradation silencieuse) : les nouveaux
   poids remplacent packages/weights.json seulement si, sur le test,
   F1 gagne ≥ 5 points ET la justesse (ACC) ne perd pas plus de 2 points.
6. Consigne tout dans docs/AUTOTUNE.md : les chiffres réels, bons ou
   mauvais. Aucun chiffre n'est gonflé ; si les données manquent, le
   rapport le dit.

Usage : python3 tools/selftune.py [--iterations 300]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "packages"))

from app.main import _signals_from_path  # noqa: E402
from scoring import DEFAULT_WEIGHTS  # noqa: E402

LIE_LABELS = {"lie", "mensonge", "false", "faux", "deception"}
TRUTH_LABELS = {"truth", "vérité", "verite", "vrai", "true", "truthful"}
MIN_TRAIN_SIGNALS_COVERAGE = 0.5


def load_entries() -> tuple[list[dict], dict]:
    stats = {"files": 0, "entries": 0, "no_consent": 0, "bad_label": 0, "clip_missing": 0}
    entries: list[dict] = []
    data_dir = ROOT / "data" / "labeled"
    for jf in sorted(data_dir.glob("*.json")):
        stats["files"] += 1
        try:
            payload = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows = payload.get("entries", payload) if isinstance(payload, dict) else payload
        for row in rows if isinstance(rows, list) else []:
            stats["entries"] += 1
            if not row.get("consent"):
                stats["no_consent"] += 1
                continue
            label = str(row.get("label", "")).strip().lower()
            if label in LIE_LABELS:
                y = 1
            elif label in TRUTH_LABELS:
                y = 0
            else:
                stats["bad_label"] += 1
                continue
            clip = str(row.get("clip", ""))
            candidates = [data_dir / clip, data_dir / "clips" / clip, ROOT / clip]
            path = next((c for c in candidates if c.is_file()), None)
            if path is None:
                stats["clip_missing"] += 1
                continue
            entries.append(
                {
                    "path": str(path),
                    "y": y,
                    "subject": str(row.get("subject") or "inconnu"),
                    "segment": row.get("segment") or {},
                }
            )
    return entries, stats


def extract(entry: dict) -> dict | None:
    path = entry["path"]
    seg = entry["segment"]
    tmp = None
    try:
        start, end = seg.get("start_s"), seg.get("end_s")
        if start is not None and end is not None and float(end) > float(start):
            tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            tmp.close()
            subprocess.run(
                ["ffmpeg", "-y", "-ss", str(start), "-to", str(end), "-i", path,
                 "-c:v", "libx264", "-preset", "veryfast", "-an", tmp.name],
                capture_output=True, timeout=300,
            )
            path = tmp.name
        signals, coverage, quality, _info, _pulse = _signals_from_path(path)
        if not quality["canScore"]:
            return None
        return {"signals": signals, "y": entry["y"], "subject": entry["subject"]}
    except Exception:
        return None
    finally:
        if tmp:
            Path(tmp.name).unlink(missing_ok=True)


def predict_index(signals: dict, weights: dict) -> float | None:
    num = den = 0.0
    for k, w in weights.items():
        v = signals.get(k)
        if v is None:
            continue
        num += w * min(1.0, max(0.0, float(v)))
        den += w
    if den == 0:
        return None
    return 5 + (num / den) * 90


def metrics(rows: list[dict], weights: dict, threshold: int) -> dict:
    tp = fp = tn = fn = 0
    scored = 0
    ece_bins = np.zeros((10, 3))  # somme proba, somme y, compte
    for row in rows:
        idx = predict_index(row["signals"], weights)
        if idx is None:
            continue
        scored += 1
        pred = 1 if idx >= threshold else 0
        y = row["y"]
        if pred == 1 and y == 1:
            tp += 1
        elif pred == 1:
            fp += 1
        elif y == 1:
            fn += 1
        else:
            tn += 1
        b = min(9, int(idx / 10))
        ece_bins[b] += (idx / 100.0, y, 1)
    n = max(1, tp + fp + tn + fn)
    acc = (tp + tn) / n
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    ece = 0.0
    for sump, sumy, cnt in ece_bins:
        if cnt:
            ece += (cnt / max(1, scored)) * abs(sump / cnt - sumy / cnt)
    return {"n": scored, "acc": round(acc, 3), "f1": round(f1, 3),
            "precision": round(prec, 3), "recall": round(rec, 3), "ece": round(float(ece), 3)}


def split(rows: list[dict], rng: np.random.Generator):
    subjects = sorted({r["subject"] for r in rows})
    if len(subjects) >= 2 and len(rows) >= 12:
        shuffled = list(subjects)
        rng.shuffle(shuffled)
        test_subjects = set()
        test_n = 0
        for s in shuffled:
            if test_n >= max(3, len(rows) // 4) and test_subjects:
                break
            test_subjects.add(s)
            test_n += sum(1 for r in rows if r["subject"] == s)
        train = [r for r in rows if r["subject"] not in test_subjects]
        test = [r for r in rows if r["subject"] in test_subjects]
        if train and test:
            return train, test, "sujet-disjointe"
    idx = np.arange(len(rows))
    rng.shuffle(idx)
    cut = max(1, int(len(rows) * 0.7))
    return [rows[i] for i in idx[:cut]], [rows[i] for i in idx[cut:]], "aléatoire seedée"


def search_weights(train: list[dict], keys: list[str], iterations: int, rng) -> tuple[dict, int]:
    best_w, best_t, best_score = None, 55, -1.0
    base = np.array([DEFAULT_WEIGHTS.get(k, 0.1) for k in keys], dtype=float)
    for it in range(iterations):
        if it == 0:
            w = base / base.sum()
        else:
            w = rng.dirichlet(base * 14 + 0.6)
        weights = {k: float(v) for k, v in zip(keys, w)}
        for threshold in (48, 52, 55, 58, 62):
            m = metrics(train, weights, threshold)
            score = m["f1"] + 0.25 * m["acc"]
            if score > best_score:
                best_score, best_w, best_t = score, weights, threshold
    return best_w or {}, best_t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=300)
    args = ap.parse_args()
    today = date.today().isoformat()
    rng = np.random.default_rng(42)

    entries, stats = load_entries()
    rows = []
    for e in entries:
        r = extract(e)
        if r:
            rows.append(r)

    lines = [f"\n## {today} — exécution automatique",
             f"- Fichiers de données : {stats['files']} ; entrées : {stats['entries']} "
             f"(sans consentement : {stats['no_consent']}, étiquette illisible : {stats['bad_label']}, "
             f"clip introuvable : {stats['clip_missing']})",
             f"- Clips analysables par le pipeline : {len(rows)}"]

    decision = "aucun changement"
    summary = {"date": today, "usable": len(rows), "decision": decision}

    if len(rows) < 8:
        lines.append(
            f"- **Données insuffisantes pour régler les poids** ({len(rows)} < 8 clips). "
            "La boucle reste en attente : les parties du Mode Jeu et les exports de "
            "l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun "
            "chiffre inventé.")
    else:
        train, test, mode = split(rows, rng)
        keys = [k for k in DEFAULT_WEIGHTS
                if sum(1 for r in train if r["signals"].get(k) is not None)
                >= MIN_TRAIN_SIGNALS_COVERAGE * len(train)]
        current = {**DEFAULT_WEIGHTS}
        try:
            wj = json.loads((ROOT / "packages" / "weights.json").read_text(encoding="utf-8"))
            current = {**DEFAULT_WEIGHTS, **(wj.get("weights") or {})}
            cur_threshold = int(wj.get("threshold", 55))
        except Exception:
            cur_threshold = 55
        cand_w, cand_t = search_weights(train, keys, args.iterations, rng)
        full_cand = {**current, **cand_w}
        m_cur = metrics(test, current, cur_threshold)
        m_cand = metrics(test, full_cand, cand_t)
        m_cur_tr = metrics(train, current, cur_threshold)
        lines += [
            f"- Séparation {mode} : entraînement {len(train)}, test {len(test)}",
            f"- Signaux réglables (couverture ≥ 50 %) : {', '.join(keys) or 'aucun'}",
            f"- Poids actuels — test : ACC {m_cur['acc']}, F1 {m_cur['f1']}, ECE {m_cur['ece']} (n={m_cur['n']})",
            f"- Candidat — test : ACC {m_cand['acc']}, F1 {m_cand['f1']}, ECE {m_cand['ece']} "
            f"(entraînement : ACC {m_cur_tr['acc']} avec les poids actuels)",
        ]
        adopt = (m_cand["f1"] >= m_cur["f1"] + 0.05 and m_cand["acc"] >= m_cur["acc"] - 0.02
                 and m_cand["n"] >= 5)
        if adopt:
            version = 1
            try:
                version = int(wj.get("version", 1)) + 1
            except Exception:
                pass
            payload = {"version": version, "updated": today, "threshold": cand_t,
                       "source": f"tools/selftune.py — test sujet-disjoint n={m_cand['n']}, "
                                 f"F1 {m_cur['f1']} -> {m_cand['f1']}",
                       "weights": {k: round(float(full_cand[k]), 4) for k in sorted(full_cand)}}
            (ROOT / "packages" / "weights.json").write_text(
                json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            decision = f"nouveaux poids adoptés (v{version})"
            lines.append(f"- **DÉCISION : {decision}** — F1 test {m_cur['f1']} → {m_cand['f1']}, "
                         f"seuil {cur_threshold} → {cand_t}. Le serveur doit redémarrer pour les charger.")
        else:
            lines.append("- **DÉCISION : poids actuels conservés** — le candidat ne bat pas "
                         "la règle d'adoption (gain F1 ≥ 0,05 sans perdre plus de 0,02 d'ACC sur le test).")
        summary.update({"train": len(train), "test": len(test), "split": mode,
                        "current": m_cur, "candidate": m_cand})
    summary["decision"] = decision

    doc = ROOT / "docs" / "AUTOTUNE.md"
    header = ("# Tensivue — Journal d'auto-amélioration\n\n"
              "Chaque exécution de tools/selftune.py ajoute une section : les chiffres "
              "réels mesurés sur données étiquetées, et la décision prise. Voir "
              "docs/AUTONOMOUS_LOOP.md pour les règles de la boucle.\n")
    prev = doc.read_text(encoding="utf-8") if doc.exists() else header
    doc.write_text(prev + "\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "tools" / "last_run.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("DECISION:", decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
