# Tensivue — Journal d'auto-amélioration

Chaque exécution de tools/selftune.py ajoute une section : les chiffres réels mesurés sur données étiquetées, et la décision prise. Voir docs/AUTONOMOUS_LOOP.md pour les règles de la boucle.

## 2026-11-07 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.

## 2026-11-08 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression par lien (backend local, port 8000) :
  - Parole face caméra (M7lc1UVf-VE) : **non rejouée** — téléchargement bloqué par YouTube (« Sign in to confirm you're not a bot », yt-dlp) ; ni indice ni refus observé. Blocage externe, pas une régression du backend.
  - Animation (aqz-KE-bpKQ) : **non rejouée** — même blocage anti-bot YouTube ; le refus de la porte qualité attendu n'a pas pu être vérifié.
  - Musique (dQw4w9WgXcQ) : rejouée — indice 55, confiance 0,62, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Tel quel, comme attendu pour un témoin musique.

## 2026-11-09 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression par lien (backend local, port 8000) :
  - Parole face caméra (M7lc1UVf-VE) : **non rejouée** — le client a abandonné après 900 s : la vidéo récupérée par yt-dlp dure 1 343,6 s (22 min) et le pipeline lit chaque image (détection Haar toutes les 5 images) sur une VM à 1,5 CPU partagé et chargée ; l'analyse tournait encore côté serveur au moment de l'abandon, ni indice ni refus observé. Pas une régression du backend — limite de temps de la passe, pas du code.
  - Animation (aqz-KE-bpKQ) : **non rejouée** — téléchargement bloqué par YouTube (« Sign in to confirm you're not a bot », yt-dlp), comme le 8 nov. ; le refus de la porte qualité attendu n'a pas pu être vérifié.
  - Musique (dQw4w9WgXcQ) : rejouée — indice 55, confiance 0,62, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique au 8 nov. Tel quel, comme attendu pour un témoin musique.

### Correctif miroir — 2026-11-09 (vérifié par Mate)
Les témoins YouTube « parole » et « animation » sont remplacés par des fichiers locaux (YouTube bloque en anti-bot et la vidéo de parole de 22 min dépassait le délai) :
- **Parole** : `tests/witnesses/parole-obama-90s.mp4` (discours face caméra, Wikimedia Commons, domaine public, extrait de 90 s) → **indice 24, confiance 0,87, visage 99 %, qualité excellente** — un locuteur calme score bas avec confiance haute : comportement attendu, vérifié pour la première fois.
- **Animation** : `tests/witnesses/animation-bbb-extract.ogv` (Big Buck Bunny, extrait 33 s, Wikimedia Commons) → **refus de la porte qualité** (canScore=false, qualité insuffisante) : attendu, vérifié pour la première fois.
- La musique reste sur YouTube (dQw4w9WgXcQ, passe de façon stable). La boucle nocturne utilise désormais POST /api/analyze (téléversement) pour les deux témoins locaux.

## 2026-11-10 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, témoins locaux) :
  - Parole face caméra (`tests/witnesses/parole-obama-90s.mp4`) : **indice 24, confiance 0,87, visage 99 %, qualité excellente** — identique à la référence du 2026-11-09.
  - Animation (`tests/witnesses/animation-bbb-extract.ogv`) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage 27 %) — attendu.
  - Musique (YouTube dQw4w9WgXcQ) : **indice 55, confiance 0,62, tier « good », canScore vrai, 213 s, visage 44 %** — identique aux 8 et 9 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-11 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, témoins locaux) :
  - Parole face caméra (`tests/witnesses/parole-obama-90s.mp4`) : **indice 24, confiance 0,87, visage 99 %, qualité excellente** — identique à la référence du 2026-11-09.
  - Animation (`tests/witnesses/animation-bbb-extract.ogv`) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage 27 %) — attendu.
  - Musique (YouTube dQw4w9WgXcQ) : **indice 55, confiance 0,62, tier « good », canScore vrai, 213 s, visage 44 %** — identique aux 8, 9 et 10 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-12 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, témoins locaux) :
  - Parole face caméra (`tests/witnesses/parole-obama-90s.mp4`) : **indice 24, confiance 0,87, visage 99 %, qualité excellente** — identique à la référence du 2026-11-09.
  - Animation (`tests/witnesses/animation-bbb-extract.ogv`) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage 27 %) — attendu.
  - Musique (YouTube dQw4w9WgXcQ) : **indice 55, confiance 0,62, tier « good », canScore vrai, 213 s, visage 44 %** — identique aux 8, 9, 10 et 11 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-13 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, témoins locaux) :
  - Parole face caméra (`tests/witnesses/parole-obama-90s.mp4`) : **indice 24, confiance 0,87, visage 99 %, qualité excellente** — identique à la référence du 2026-11-09.
  - Animation (`tests/witnesses/animation-bbb-extract.ogv`) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage 27 %) — attendu.
  - Musique (YouTube dQw4w9WgXcQ) : **indice 55, confiance 0,62, tier « good », canScore vrai, 213 s, visage 44 %** — identique aux 8, 9, 10, 11 et 12 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-14 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8 et 9 nov. Tel quel, comme attendu pour un témoin musique.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-15 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–14 nov. Première tentative sans réponse dans le délai client de 300 s (téléchargement + analyse d'une vidéo de 213 s : ~294 s au total) ; reprise avec un délai de 900 s, résultat complet.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-16 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–15 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-17 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, témoins locaux) :
  - Parole face caméra (`tests/witnesses/parole-obama-90s.mp4`) : **indice 24, confiance 0,87, visage 99 %, qualité excellente** — identique à la référence du 2026-11-09.
  - Animation (`tests/witnesses/animation-bbb-extract.ogv`) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage 27 %) — attendu.
  - Musique (YouTube dQw4w9WgXcQ) : **indice 55, confiance 0,62, tier « good », canScore vrai, 213 s, visage 44 %** — identique aux 8, 9, 10, 11, 12 et 16 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-18 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–17 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-19 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–18 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-20 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–19 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-21 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–20 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.
## 2026-11-22 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,62**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 44 %). Identique aux 8–21 nov.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

## 2026-11-23 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts (avec `-p no:capture` — la capture pytest exige un répertoire temporaire, indisponible ce soir ; voir incident. Aucun échec de code).
- Régression (pipeline exact du backend, rejoué en processus — HTTP bloqué, voir incident) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : **non rejouée** — téléchargement YouTube impossible : yt-dlp exige un répertoire temporaire, indisponible (voir incident). Dernière valeur mesurée : indice 55, confiance 0,62 (stable du 8 au 22 nov.), citée à titre d'historique, pas comme mesure du jour.
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis.

### Incident — panne d'écriture de la VM, 23 nov. 2026 (~01 h 31, toujours active à 03 h 40)
- Les écritures par tout processus lancé du shell sont refusées (« Operation not permitted », fichiers créés à 0 octet) sur tous les systèmes de fichiers ; les outils fichiers directs écrivent normalement. Vérifié : `echo` et écriture Python vers /tmp et ~/workspace échouent ; `tempfile.gettempdir()` ne trouve aucun répertoire utilisable.
- Conséquences sur cette passe : (1) `tools/selftune.py` a calculé son verdict (0 clip) puis s'est interrompu en journalisant — `Path.write_text` ouvre en troncature avant d'écrire, ce qui a **vidé docs/AUTOTUNE.md** ; le journal complet a été **restauré depuis la copie GitHub** (SHA d011e7174d1fbc6d0aa043e139415c5fab7efc7d, sections du 7 au 22 nov. 2026) et la section du jour ajoutée par outil fichier ; (2) pytest ne démarre pas avec sa capture par défaut (`TemporaryFile`) — les 13 tests passent avec `-p no:capture` ; (3) POST /api/analyze échoue au parsing multipart (« There was an error parsing the body », /health OK) — la régression des deux témoins locaux a donc été rejouée **en processus** via `_report_from_path`, exactement le code de l'endpoint ; (4) le témoin musique n'a pas pu être rejoué (ni sur la VM, ni sur le Mac — aucun dépôt truthlens sur le Mac, vérifié par SSH).
- Correctif à apporter à selftune.py (quand les écritures reviendront) : journaliser sans tronquer d'abord (écrire vers un fichier temporaire puis renommer, ou ajouter avant d'écrire) pour que la panne ne puisse plus vider le journal.

## 2026-11-24 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000, HTTP — la panne d'écriture du 23 nov. est résolue : écritures shell et `tempfile` fonctionnent de nouveau) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,63**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 45 %). Identique à l'historique du 8 au 22 nov. (indice 55, confiance 0,62 — écart 0,01, bruit de mesure).
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis (weights.json inchangé, version 1 du 2026-11-07).

### Incident — environnement Python effacé, réparé ce soir (24 nov. 2026, ~03 h 40)
- Constat : `python3 -m pytest` introuvable ; fastapi, uvicorn, cv2, pydantic, python-multipart, httpx absents du Python système (restait numpy 1.26.4) — effacement probable lors du nettoyage disque / remplacement de VM du 23 nov. `pip install --break-system-packages` a échoué (typing_extensions 4.10.0 installé par Debian, RECORD manquant).
- Correctif appliqué : venv dédié créé à `.venv/` (déjà couvert par `.gitignore`), `backend/requirements.txt` + pytest + httpx + yt-dlp installés dedans. **Les prochaines passes doivent utiliser `.venv/bin/python`** (pytest, selftune, uvicorn) tant que le Python système n'est pas restauré.
- Deuxième accroc : pip a installé opencv-python-headless 5.1.0, où `cv2.CascadeClassifier` n'existe plus — /api/analyze rendait HTTP 500. Épinglé `opencv-python-headless>=4.9,<5` dans le venv (4.14.0, CascadeClassifier présent). Recommandation : ajouter `<5` à `backend/requirements.txt` pour qu'une installation fraîche ne retombe pas dans le même piège.
- Troisième accroc : yt-dlp refusait le TLS de YouTube (« self-signed certificate in certificate chain ») — le proxy d'egress de la VM intercepte le TLS et yt-dlp utilise le bundle certifi du venv, pas le CA système. Correctif : CA d'egress (`/run/hatch/egress-tls/ca-bundle.pem`) ajouté au `cacert.pem` de certifi dans le venv. Le témoin musique a ensuite rejoué normalement (indice 55).

## 2026-11-25 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,63**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 45 %). Identique à l'historique du 8 au 24 nov. (indice 55, confiance 0,62–0,63).
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis (weights.json inchangé, version 1 du 2026-11-07).

### Incident — CA d'egress tournée, témoin musique bloqué puis réparé (25 nov. 2026, ~03 h 40)
- Premier essai du témoin musique : échec TLS yt-dlp (« self-signed certificate in certificate chain »), HTTP 422 « Lien illisible ou vidéo indisponible ». Cause : le CA d'egress « Hatch Sandbox Egress CA » a tourné — le bundle `/run/hatch/egress-tls/ca-bundle.pem` a été régénéré le 25 nov. 07 h 00 (nouvelle empreinte SHA256 B6:0D:FD:D5…E2:EE) ; le `cacert.pem` du venv contenait encore l'ancien CA (empreinte 52:52:16:D2…92:6D, ajouté le 24 nov.), plus ses 121 certificats en double (234 blocs pour 121 uniques — le correctif du 24 nov. avait ajouté tout le bundle d'egress au fichier certifi).
- Correctif appliqué : le CA actuel a été extrait du bundle d'egress et ajouté au `cacert.pem` du venv, **vérifié par empreinte SHA256** (présent, 235 blocs). yt-dlp en CLI a ensuite titré la vidéo normalement, et le témoin musique a rejoué (indice 55, confiance 0,63).
- Leçon pour les prochaines passes : le CA d'egress peut tourner à chaque redémarrage de VM — si le témoin musique échoue en TLS, comparer l'empreinte du CA « Hatch Sandbox Egress CA » du bundle `/run/hatch/egress-tls/ca-bundle.pem` avec celle présente dans `.venv/lib/python3.12/site-packages/certifi/cacert.pem`, et ajouter le CA actuel (vérification par empreinte, pas par comparaison de blocs, les doublons faussent le comptage).

## 2026-11-26 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,63**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 45 %). Identique à l'historique du 8 au 24 nov. (indice 55, confiance 0,62–0,63).
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis (weights.json inchangé, version 1 du 2026-11-07).

### Incident — CA d'egress tourné de nouveau, témoin musique bloqué puis réparé (26 nov. 2026, ~03 h 45)
- Premier essai du témoin musique : échec TLS yt-dlp (« self-signed certificate in certificate chain »), HTTP 422 « Lien illisible ou vidéo indisponible ». Même cause que le 25 nov. : le CA d'egress « Hatch Sandbox Egress CA » a tourné — nouvelle empreinte SHA256 5dc2ef9e…76b82 (remplace B6:0D:FD:D5…E2:EE du 25 nov.) ; c'était le seul des 121 certificats du bundle `/run/hatch/egress-tls/ca-bundle.pem` absent du `cacert.pem` du venv.
- Correctif appliqué (même procédure que le 25 nov.) : le CA actuel a été ajouté au `cacert.pem` du venv, **vérifié par empreinte SHA256** (présent, 236 blocs). Le témoin musique a ensuite rejoué normalement (indice 55, confiance 0,63).
- Leçon confirmée : le CA d'egress tourne à chaque redémarrage de VM — la vérification d'empreinte fait partie de la passe de régression tant que le témoin musique passe par YouTube.

## 2026-11-27 — exécution automatique
- Fichiers de données : 0 ; entrées : 0 (sans consentement : 0, étiquette illisible : 0, clip introuvable : 0)
- Clips analysables par le pipeline : 0
- **Données insuffisantes pour régler les poids** (0 < 8 clips). La boucle reste en attente : les parties du Mode Jeu et les exports de l'app de collecte alimenteront data/labeled/. Aucun poids touché, aucun chiffre inventé.
- Tests unitaires : 13/13 verts.
- Régression (backend local, port 8000) :
  - Parole face caméra (fichier local parole-obama-90s.mp4) : indice **24**, confiance **0,87**, visage visible 99 %, tier « excellent », canScore vrai. Identique à la référence du 2026-11-09.
  - Animation (fichier local animation-bbb-extract.ogv) : **refus de la porte qualité** (canScore=false, tier « insufficient », visage visible 27 %, indice/confiance null). Refus attendu, vérifié.
  - Musique (dQw4w9WgXcQ, via /api/analyze-url) : indice **55**, confiance **0,63**, aucun refus (tier « good », canScore vrai, 213 s, visage visible 45 %). Identique à l'historique du 8 au 26 nov. (indice 55, confiance 0,62–0,63).
- Poids conservés (données insuffisantes : 0 clip utilisable) ; aucun redémarrage de serveur requis (weights.json inchangé, version 1 du 2026-11-07).

### Incident — CA d'egress tourné une troisième fois, témoin musique bloqué puis réparé (27 nov. 2026, ~03 h 45)
- Premier essai du témoin musique : échec TLS yt-dlp (« self-signed certificate in certificate chain »), HTTP 422 « Lien illisible ou vidéo indisponible ». Même cause que les 25 et 26 nov. : le CA d'egress « Hatch Sandbox Egress CA » a tourné — nouvelle empreinte SHA256 3E:7E:89:CB:89:09:1A:6D:E3:21:C9:4F:4D:56:D9:F6:36:F6:9B:83:7E:B6:A1:CB:A7:20:24:26:2B:2D:21:B6 (remplace 5dc2ef9e…76b82 du 26 nov.).
- Correctif appliqué (même procédure que les 25 et 26 nov.) : le CA actuel a été ajouté au `cacert.pem` du venv, **vérifié par empreinte SHA256** (présent, 237 blocs). Le témoin musique a ensuite rejoué normalement (indice 55, confiance 0,63).
- Leçon confirmée pour la troisième fois : le CA d'egress tourne à chaque redémarrage de VM — la vérification d'empreinte fait partie de la passe de régression tant que le témoin musique passe par YouTube.
