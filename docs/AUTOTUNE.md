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
