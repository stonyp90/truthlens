# Tensivue — Boucle d'amélioration autonome

Directive d'Anthony (7 nov. 2026) : le système doit veiller sur toutes les
technologies qui sortent (open source, police, commercial, universités),
tester en continu et s'améliorer **sans intervention humaine**, en temps
réel quand c'est possible. Ce document décrit la boucle telle qu'elle
roule, ses règles et ses limites honnêtes.

## Les trois boucles

### 1. Veille technologique — quotidienne (07 h, heure de Toronto)
Balayage des sources : arXiv, Hugging Face, GitHub, littérature revue par
les pairs, et technologies déployées (police et commercial : Converus
EyeDetect, AVATAR/iBorderCtrl, analyse thermique, CVSA, polygraphe —
avec leur niveau de preuve réel, pas leur marketing).
- Les nouveautés sont consignées dans `docs/RESEARCH.md` (datées, sourcées).
- Un signal candidat intégrable (ex. pupillométrie, rPPG, prosodie vocale)
  est ajouté à la file « Signaux candidats » ci-dessous avec son exigence
  de porte qualité.
- Anthony est avisé seulement quand quelque chose change vraiment la
  donne : un modèle/dataset ouvert utilisable, un résultat publié qui bat
  l'état de l'art, ou un signal qu'on peut brancher.

### 2. Auto-réglage — nocturne (03 h, heure de Toronto)
`tools/selftune.py` roule sans humain :
1. Lit les données étiquetées consenties (`data/labeled/`, exports de
   l'app de collecte et du Mode Jeu).
2. Extrait les signaux avec le même pipeline que le service.
3. Séparation **sujet-disjointe** entraînement/test (jamais de test sur
   une personne vue à l'entraînement).
4. Recherche de meilleurs poids de fusion + seuil ; adoption seulement si
   le test gagne ≥ 5 points de F1 sans perdre plus de 2 points de justesse.
   Sinon, les poids actuels restent — **la boucle n'a pas le droit de se
   dégrader en silence**.
5. Journalise les chiffres réels dans `docs/AUTOTUNE.md` et pousse au repo.
La même passe rejoue la suite de régression (tests unitaires + vidéos
témoins : parole face caméra, animation, musique) : toute régression est
rapportée, pas cachée.

### 3. Temps réel — en continu, chez l'utilisateur
L'analyse en direct (webcam, extension, flux) roule déjà en temps réel
dans le navigateur et via le WebSocket du backend. La boucle nocturne ne
touche jamais une session en cours : les nouveaux poids s'appliquent au
redémarrage du service / au rechargement de la page.

## Signaux — état et candidats

| Signal | État | Note |
|---|---|---|
| Mouvements de tête, répétition, figement | ✅ actif | Différence d'images + suivi de visage |
| **Pouls à distance (rPPG, POS)** | ✅ actif depuis le 7 nov. 2026 | BPM + instabilité du pouls ; exige visage ≥ 120 px, ≥ 8 s |
| Clignements (EAR), regard/iris, tension faciale | 🔜 phase 2 | MediaPipe Face Landmarker (468 points, iris) |
| Pupille / mouvement rétinien | 🔜 candidat veille | Exige visage ≥ 220 px ; la recherche « eye-tracking » (EyeDetect) est suivie |
| Voix : prosodie, hésitations, contenu vérifiable | 🔜 phase 3 | Whisper + analyse du discours ; recette gagnante SVC 2026 (descripteurs → juge LLM) |
| Thermique, sueur, respiration | 👀 veille | RGB seulement pour l'instant ; aucun papier revu 2024-2026 solide sur la sueur en RGB |
| Multi-personnes + diarisation | 📐 dessiné | `docs/MULTI_PERSON_AND_EDGE_CASES.md` |

## Les limites que la boucle ne peut pas franchir (honnêteté)

- **Le plafond scientifique existe.** En laboratoire, l'état de l'art
  publié tourne autour de 55-75 % de justesse selon les jeux de données ;
  le vainqueur SVC 2026 est à 71,35 % sur DOLOS. Aucune boucle autonome
  ne transforme ça en « 100 % accurate ». Ce que la boucle garantit :
  chaque chiffre affiché est **mesuré** sur des données étiquetées jamais
  vues à l'entraînement, avec le niveau de confiance et l'abstention
  quand la qualité ne permet pas de conclure.
- **Les données sont le goulot.** Les datasets publics sont petits et à
  licences académiques. Le volant de données propriétaire (Mode Jeu +
  collecte consentie, Loi 25) est ce qui fera monter les chiffres pour
  vrai ; la boucle consomme ce qui arrive, elle n'invente pas de données.
- **Aucun achat, aucune publication, aucun envoi** ne sort de la boucle :
  elle lit, teste, règle les poids internes et journalise. Tout le reste
  attend le go d'Anthony.
- Segments exclus inchangés : RH, justice, assurance, éducation
  (AI Act UE, Loi 25). Le produit affiche un **indice de tension +
  confiance**, jamais un verdict de mensonge.
