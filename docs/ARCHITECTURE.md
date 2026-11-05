# Architecture

```
┌──────────────┐   upload (gratuit)    ┌────────────────────┐
│  Site web    │ ────────────────────▶ │  Backend FastAPI   │
│  (analyse    │   ou 100 % local      │  /api/analyze      │
│   locale)    │                       │  /ws/stream        │
└──────────────┘                       │  /api/ingest       │
┌──────────────┐   calque temps réel   └─────────┬──────────┘
│  Extension   │ ────────────────────────────────┘
│  Chrome MV3  │   frames (mode Pro)     ffmpeg : HLS / SRT
└──────────────┘
        │                Moteur partagé
        └──── packages/scoring.(js|py) — fusion de signaux + confiance
```

## Composants

### 1. Site web (`apps/web`)
- Upload drag-and-drop MP4/WebM; analyse **locale par défaut** (la vidéo
  ne quitte pas le navigateur) — échantillonnage de frames, série de
  mouvement, timeline, export JSON du rapport.
- Phase 2 : MediaPipe Face Landmarker (WASM) dans le navigateur pour
  iris/rétine, clignements et blendshapes, sans serveur.

### 2. Extension Chrome (`apps/extension`, Manifest V3)
- Content script : détecte chaque `<video>` (MP4 direct, lecteurs
  HLS/DASH, YouTube/Vimeo), injecte un panneau temps réel.
- Limite navigateur assumée : canvas « tainted » sur flux cross-origin
  protégés → mode métadonnées + renvoi vers l'ingestion serveur (Pro).

### 3. Backend (`backend`, FastAPI)
- `POST /api/analyze` : file d'attente d'uploads, OpenCV (mouvement +
  présence visage). Réponse : signaux, indice, confiance, disclaimer.
- `WS /ws/stream` : frames JPEG → indice en continu (latence cible < 500 ms).
- `POST /api/ingest` : déclare un flux **HLS** (`https://….m3u8`) ou
  **SRT** (`srt://…`). Worker d'ingestion (phase 3) :
  `ffmpeg -i <flux> -vf fps=2,scale=… -f rawvideo -` → même pipeline.

### 4. Moteur de signaux (`packages/`)
- `scoring.js` / `scoring.py` : mêmes formules des deux côtés —
  écart de clignement, aversion du regard, mouvement de tête,
  répétition (autocorrélation), tension faciale, figement.
- Fusion pondérée, renormalisée selon les signaux disponibles;
  indice **borné 5–95** (jamais d'extrêmes affichés) + confiance
  (visibilité du visage, durée, couverture des signaux).

## Données et vie privée
- Mode gratuit : traitement local ou éphémère; aucune conservation
  vidéo par défaut. Les rapports JSON ne contiennent que des métriques.
- Dataset d'entraînement : uniquement sources **consenties/licenciées**
  (voir SCIENCE_AND_LIMITS). Aucun scraping de visages.
- Hébergement cible : Canada (Loi 25), chiffrement au repos, journaux
  d'accès, suppression sur demande.
