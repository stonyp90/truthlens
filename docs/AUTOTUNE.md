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
