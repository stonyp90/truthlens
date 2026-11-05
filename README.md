# 🔎 TruthLens

**Analyse vidéo des signaux de tension et d'incongruence** — regard (rétine/iris),
clignements, micro-mouvements répétitifs, figement, tension faciale —
sur vidéo téléversée **et** en temps réel par-dessus les flux du web.

> ⚠️ **Honnêteté d'abord :** TruthLens ne « détecte pas les mensonges à 100 % » —
> personne ne le peut, la science est formelle là-dessus
> ([docs/SCIENCE_AND_LIMITS.md](docs/SCIENCE_AND_LIMITS.md)).
> TruthLens produit un **indice de tension observable (0–100)** avec son niveau
> de confiance, pour aider un humain à mieux regarder. C'est tout — et c'est déjà beaucoup.

## Les deux produits

### 1. Site web — analyse d'upload (**gratuit**)
`apps/web/index.html` : dépose une vidéo (MP4/WebM), l'analyse roule
**dans le navigateur** (la vidéo ne quitte pas l'appareil), timeline
seconde par seconde, signaux détaillés, rapport JSON exportable.

```bash
# aucun build : ouvrir le fichier, ou servir le dossier
npx serve apps/web   # ou : python3 -m http.server -d apps/web
```

### 2. Extension Chrome — calque temps réel
`apps/extension/` (Manifest V3) : s'installe en mode développeur
(*chrome://extensions → Charger l'extension non empaquetée*), détecte les
`<video>` des pages (MP4, lecteurs HLS/DASH, YouTube…) et affiche l'indice
en direct. Le **temps réel hébergé** (flux HLS/SRT via serveur, tous les
signaux, rapports) est la partie **payante** — voir [BUSINESS_PLAN.md](BUSINESS_PLAN.md).

### 3. Backend (API + temps réel serveur)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# GET  /health
# POST /api/analyze   (upload vidéo -> rapport JSON)
# WS   /ws/stream     (frames -> indice en continu)
# POST /api/ingest    (déclarer un flux HLS ou SRT — mode Pro)
```

## Signaux mesurés
Rétine/iris et regard · clignements (écart vs baseline du sujet) ·
mouvements répétitifs (autocorrélation) · figement · mouvements de tête ·
tension faciale (blendshapes) · rPPG et voix (expérimental, phase 3).
Moteur de fusion partagé : `packages/scoring.js` / `packages/scoring.py`.

## Tests
```bash
node packages/scoring.test.mjs
cd backend && python -m pytest tests/ -q
```

## Documentation
- [Science et limites](docs/SCIENCE_AND_LIMITS.md) — ce qui est prouvé, ce qui ne l'est pas
- [Recherche — modèles et datasets existants](docs/RESEARCH.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Plan d'affaires](BUSINESS_PLAN.md)

## Licence
MIT — voir [LICENSE](LICENSE). Les datasets tiers gardent leurs licences propres.
