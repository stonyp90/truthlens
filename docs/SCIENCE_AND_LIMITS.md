# Science et limites — à lire avant tout le reste

## La vérité, blanc noir

**Aucun système au monde ne détecte le mensonge à 100 %.** Ni le polygraphe,
ni l'IA, ni Meta, ni nous. Ce n'est pas un problème d'ingénierie qu'on va
« régler avec plus de données » : c'est un problème de fond.

- Il n'existe **aucun signal physiologique propre au mensonge**. La tension,
  les clignements, le regard fuyant, les micro-mouvements et le figement
  mesurent du **stress, de la charge cognitive ou de l'inconfort** — qu'un
  menteur peut ne pas ressentir, et qu'une personne honnête anxieuse,
  fatiguée, neurodivergente ou intimidée par une caméra ressentira fort.
- Le rapport du **National Research Council (2003)** sur le polygraphe
  conclut que sa précision est insuffisante pour un dépistage fiable, et
  l'**American Psychological Association** rappelle qu'il n'existe pas de
  « nez de Pinocchio » : la plupart des psychologues rejettent l'idée
  qu'un test puisse détecter le mensonge de façon fiable.
- Les meilleurs systèmes publiés sur des datasets étiquetés (DOLOS,
  Bag-of-Lies, entrevues réelles) tournent autour de **60–75 % de précision
  en laboratoire**, sur des protocoles contrôlés — loin du terrain réel,
  et très loin de 100 %.

## Ce que TruthLens fait — honnêtement

TruthLens mesure des **signaux observables** et les fusionne en un
**indice de tension / incongruence (0–100)**, accompagné d'un **niveau de
confiance de mesure** :

| Signal | Ce qu'on mesure | Outil |
|---|---|---|
| Rétine / iris | direction du regard, pupille (éclairage contrôlé seulement) | MediaPipe Iris / Face Landmarker |
| Clignements | taux et écart vs baseline du sujet (EAR) | MediaPipe blendshapes + landmarks paupières |
| Mouvements répétitifs | autocorrélation des micro-mouvements (tics, balancements) | série de mouvement + `repetitionScore` |
| Figement | chute soudaine de mouvement | `freezeScore` |
| Tête | vélocité, instabilité, rotations | suivi de boîte/landmarks |
| Tension faciale | sourcils, mâchoire, lèvres (blendshapes ARKit-like) | MediaPipe Face Landmarker |
| Rythme cardiaque | rPPG (variations de couleur de peau) — signal fragile | méthodes POS/CHROM (phase 3) |
| Voix | jitter, pauses, débit (phase 3) | Whisper + analyse prosodique |

## Règles d'usage non négociables

1. **Jamais** présenter l'indice comme une « probabilité de mensonge »
   dans l'UI, le marketing ou un rapport.
2. **Jamais** d'usage seul pour une décision qui affecte une personne :
   embauche, congédiement, assurance, justice, garde d'enfants, frontière.
   (Certains de ces usages sont d'ailleurs **interdits** — voir le plan
   d'affaires, section risques légaux : AI Act européen, Loi 25 au Québec.)
3. Toujours afficher la confiance de mesure et le disclaimer.
4. Baseline individuelle obligatoire : on compare la personne **à
   elle-même** (ses premières minutes calmes), jamais à une « moyenne
   de menteurs ».
5. Consentement explicite de la personne filmée pour toute analyse
   enregistrée; mode local par défaut (la vidéo ne quitte pas l'appareil
   en mode gratuit).

## La voie vers « le mieux possible » (pas 100 %)

Des milliards d'échantillons non étiquetés ne servent à rien : il faut des
vérités-terrain vérifiées. La stratégie données est donc :

1. Datasets publics/licenciés avec vérité-terrain (DOLOS, Bag-of-Lies,
   MU3D, Real-Life Deception Detection) pour calibrer et **publier nos
   taux d'erreur réels**.
2. Protocoles de collecte consentie (jeux de vérité/mensonge rémunérés)
   pour bâtir un dataset propriétaire propre.
3. Évaluation aveugle continue : chaque version du modèle affiche son
   AUC / taux de faux positifs sur un jeu de test gelé, dans le repo.
