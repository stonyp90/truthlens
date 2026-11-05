# Plusieurs personnes, qui parle, et les cas où il faut se taire

*Questions d'Anthony (5 nov. 2026) : « S'il y a plusieurs personnes
dans une vidéo, tu vas mettre un petit overlay pour chacun? Comment
tu vas savoir qui parle? Si c'est une chanson, il y a beaucoup de cas
que ça fera pas de sens — des faux positifs. T'as pensé à tout ça? »*

*Réponse courte : oui pour le multi-personnes (c'est conçu pour),
et les cas absurdes se règlent par une règle simple — **quand le
contexte invalide la mesure, le produit s'abstient au lieu de
deviner**. Le faux positif évité vaut plus qu'un score de plus.*

## 1. Plusieurs visages : un overlay par personne

- Détection et suivi multi-visages (MediaPipe Face Landmarker en mode
  multi) : chaque visage reçoit un **identifiant de piste** (P1, P2…)
  stable tant que le suivi tient.
- Chaque personne a **son propre overlay** : indice de tension,
  confiance, état (parle / écoute / hors champ), ancré à son visage.
- Chaque personne a **sa propre baseline** — on compare chacun à
  lui-même, jamais à une moyenne de groupe.
- Si le suivi perd un visage (occlusion, sortie de champ), la piste
  se ferme; à son retour, nouvelle piste, confiance réduite jusqu'à
  re-baseline. On ne fusionne jamais deux personnes par erreur : en
  cas de doute d'identité, on repart à zéro plutôt que d'attribuer
  les signaux de l'un à l'autre.

## 2. Qui parle : diarisation + synchronisation labiale

Deux sources indépendantes, croisées :

1. **Diarisation audio** (type pyannote) : segmente l'audio en
   « qui parle quand » — voix A de 0:03 à 0:11, voix B ensuite.
2. **Locuteur actif visuel** : le visage dont les lèvres bougent en
   synchronie avec le segment audio (corrélation audio-labiale, type
   SyncNet) est le locuteur; les autres sont en mode **écoute**.

Règles qui en découlent :
- Seul le **locuteur actif** reçoit l'analyse complète (ses énoncés
  sont les seuls à pouvoir être évalués).
- Les auditeurs sont affichés en « observation » : leur tension est
  visible mais **jamais interprétée comme un indice sur un énoncé** —
  on peut être tendu en écoutant une vérité qui fait mal.
- Voix hors champ (narrateur, personne au téléphone) : étiquette
  « voix sans visage » — analyse vocale seule, confiance plafonnée.
- Chevauchement de voix (tout le monde parle en même temps) :
  segment marqué **non analysable**.

## 3. Les cas où ça ne fait pas de sens — matrice d'abstention

Le système détecte le contexte et s'abstient (ou plafonne la
confiance) au lieu de produire un faux positif :

| Contexte | Détection | Comportement |
|---|---|---|
| **Chanson / musique** | classifieur audio (musique dominante, chant) | **Scoring suspendu** — chanter transforme visage et voix; rien à mesurer |
| Acteur / rôle / reconstitution | contexte déclaré + absence de variabilité naturelle | mode « performance » : affiché, non scoré |
| Animation / CGI / avatar | pas de micro-variation physiologique, textures synthétiques | **Refus** — pas un visage humain réel |
| Visage masqué, lunettes de soleil, casquette basse | landmarks insuffisants par zone | signaux affectés exclus, confiance réduite; si le regard et la bouche sont cachés : refus |
| Manger, mâcher, rire prolongé, bâiller | activité orale détectée | segments exclus de l'analyse |
| Exercice, douleur, maladie, chaleur | contexte + signaux non spécifiques | confiance plafonnée, mention « causes physiques possibles » |
| Enfant | politique produit | **Exclu** — on ne score pas les mineurs |
| Doublage / lipsync décalé | corrélation audio-labiale faible pour tous | analyse visuelle seule, confiance réduite |
| Stress de base élevé (personne anxieuse) | baseline instable | baseline prolongée; si elle ne se stabilise pas : abstention honnête |

## 4. Le principe qui gouverne tout

Un détecteur qui score tout, tout le temps, finit par « détecter »
des mensonges dans une chanson d'anniversaire. La crédibilité du
produit tient à l'inverse : **couvrir moins, mais ne jamais affirmer
ce que le contexte ne permet pas de savoir**. L'abstention est une
fonctionnalité, affichée comme telle (« non analysable : musique »),
pas un échec caché.
