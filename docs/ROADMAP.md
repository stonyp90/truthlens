# Roadmap

## Phase 0 — Fondation (ce dépôt, v0.1) ✅
- [x] Extension Chrome MV3 avec calque temps réel (mouvement)
- [x] Site d'upload avec analyse locale + timeline + export JSON
- [x] Backend FastAPI : upload, WebSocket temps réel, ingestion HLS/SRT (déclaration)
- [x] Moteur de fusion partagé JS/Python + tests
- [x] Docs science/limites, architecture, plan d'affaires

## Phase 1 — Visage réel (v0.2)
- [ ] MediaPipe Face Landmarker dans le site et l'extension :
      iris/rétine (regard), EAR (clignements), blendshapes (tension)
- [ ] Baseline individuelle : 60 premières secondes = référence du sujet
- [ ] Rapport PDF/HTML partageable (avec disclaimer intégré, non retirable)

## Phase 2 — Validation scientifique (v0.3)
- [ ] Calibration sur DOLOS + Bag-of-Lies (licences à confirmer)
- [ ] Page publique « Résultats » : précision, faux positifs, par version
- [ ] Revue externe (chercheur en psychologie) avant tout claim marketing

## Phase 3 — Temps réel hébergé / Pro (v1.0)
- [ ] Worker ffmpeg : ingestion HLS + SRT, latence < 1 s
- [ ] Clés API, quotas, facturation Stripe (voir BUSINESS_PLAN)
- [ ] Voix : Whisper + prosodie (pauses, jitter) comme signal secondaire
- [ ] rPPG expérimental (POS/CHROM), désactivé par défaut tant que fragile

## Phase 4 — Échelle
- [ ] GPU workers (file d'attente), CDN, hébergement CA
- [ ] Dataset consenti propriétaire (protocole rémunéré, comité d'éthique)
- [ ] Publication Chrome Web Store + vérification des politiques Google
