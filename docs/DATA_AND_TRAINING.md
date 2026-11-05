# Données et entraînement — d'où vient la vérité terrain

*Question d'Anthony (5 nov. 2026) : « Pour savoir si la personne mentait
ou pas, pour t'entraîner, comment tu vas faire? T'as accès à des données?
Y a-t-il des modèles déjà prêts? Sinon on peut créer de quoi — une
application gratuite pour que le monde… » Réponse : les deux. Voici le
plan, sans détour.*

## 1. Ce qui existe déjà (et ses limites)

**Jeux de données étiquetés vérité/mensonge** (la vérité terrain est
connue par construction du protocole) :

| Dataset | Contenu | Accès / licence |
|---|---|---|
| **DOLOS** (ICCV 2023) | 1 675 clips, 213 sujets, jeu télévisé « To Tell the Truth » — chaque clip étiqueté vérité/mensonge | Formulaire de recherche; **non commercial** |
| Bag-of-Lies | 325 vidéos, 35 sujets, mensonge délibéré en labo | Recherche |
| MU3D | 320 vidéos, sujets diversifiés (ethnie, âge, genre) | Recherche |
| Real-Life Trial | 121 clips de procès réels | Recherche, sensible |

Limites franches : petits, tournés en contexte de jeu ou de labo, et
surtout **licences académiques** — on peut s'en servir pour prouver la
science et calibrer, pas pour vendre le produit tel quel.

**Modèles déjà prêts** : aucun « détecteur de mensonge » crédible et
téléchargeable n'existe (vérifié sur Hugging Face). Ce qui existe :
- **PECL** (ICCV 2023) : code d'entraînement audio-visuel, 66,84 % sur
  DOLOS — notre point de départ reproductible.
- **La méthode gagnante SVC 2026** : descripteurs (unités faciales,
  affect) convertis en langage + juge LLM — pas de poids à télécharger,
  c'est une recette, elle est dans notre architecture.

## 2. Le vrai moteur de données : l'application gratuite elle-même

L'idée d'Anthony est la bonne — c'est le volant d'inertie du produit :

**Mode Jeu « Vérité ou mensonge »** (gratuit) :
1. L'utilisateur enregistre deux affirmations — une vraie, une fausse —
   ou joue en direct contre l'IA qui doit deviner.
2. **La vérité terrain est connue par construction** : c'est
   l'utilisateur qui déclare après coup laquelle était fausse.
3. Avec son **consentement exprès** (case dédiée, révocable, suppression
   en un clic — Loi 25), la paire vidéo + étiquette alimente
   l'entraînement. Sans consentement : rien n'est conservé, l'analyse
   reste locale.
4. Chaque manche jouée par le public = des exemples étiquetés réels,
   variés, dans la vraie vie — exactement ce qui manque aux datasets
   académiques.

C'est le même principe que le test d'Anthony le 5 nov. (journal
`tests/calibration-log.md`) — généralisé à tous les joueurs.

## 3. La séquence d'entraînement

| Phase | Données | Objectif |
|---|---|---|
| 0 — Calibration | DOLOS + Bag-of-Lies + MU3D (recherche) | reproduire PECL, mesurer NOTRE fusion (cibles : RESEARCH.md §12) |
| 1 — Baseline perso | les 60 premières secondes de chaque session | comparer chacun à lui-même |
| 2 — Volant gratuit | Mode Jeu consenti | dataset propriétaire étiqueté, réentraînement continu, calibration (ECE) |
| 3 — Juge multimodal | descripteurs → LLM (recette SVC 2026) | fine-tuning léger sur nos données de phase 2 |

## 4. Garde-fous non négociables

- Consentement exprès, révocable, suppression réelle (Loi 25).
- Les étiquettes du Mode Jeu sont déclarées par l'utilisateur — on
  audite par échantillon (cohérence contenu/vérification des faits).
- Jamais de segments RH/justice/assurance/éducation (AI Act, Loi 25) :
  les données du jeu ne changent rien à cette frontière.
- On publie nos mesures (accuracy, ECE, taux d'abstention) — y compris
  quand elles sont mauvaises.
